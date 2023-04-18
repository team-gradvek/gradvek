import re
import string
from django.urls import URLPattern, URLResolver
from neomodel import db, config
from neomodel import NodeSet
from neomodel.core import NodeMeta
from neomodel.relationship import RelationshipMeta
from .queries.actions import get_actions
from .queries.datasets import DATASETS
from neo4j import GraphDatabase
import json




# # For easily access each of the model classes programmatically, create a key-value map.
# MODEL_ENTITIES = {
#     'Drug': Drug,

# }

def fetch_actions(target):
    ACTIONS = get_actions(target)
    return ACTIONS


def fetch_datasets():
    return DATASETS


def update_dataset_status(dataset_name, enabled):
    query = f"MATCH (d:Dataset {{ dataset: '{dataset_name}' }}) SET d.enabled={enabled}"
    db.cypher_query(query)

def get_all_routes(urlpatterns, prefix=''):
    # Function to return all api routes from the URL patterns
    routes = []
    for entry in urlpatterns:
        if isinstance(entry, URLResolver):
            new_prefix = prefix + entry.pattern.describe().lstrip('^')
            routes.extend(get_all_routes(entry.url_patterns, new_prefix))
        elif isinstance(entry, URLPattern):
            pattern = prefix + entry.pattern.describe().lstrip('^')
            pattern = pattern.replace('\\\\', '\\')
            pattern = pattern.rstrip('\\Z')
            # Replace regex patterns with more readable path format
            pattern = re.sub(r'\(\?P<([^>]+)>([^<]+)\)', r'<\1:\2>', pattern)
            # Remove the extra triple quotes if present
            pattern = pattern.strip("'''")
            # Remove the `[name=...]` part from the path
            pattern = re.sub(r"\[name='[^']+']", '', pattern).strip()
            # Remove the extra single quotes
            pattern = re.sub(r"''", '', pattern)
            # Remove the single quote at the end of the path
            pattern = pattern.rstrip("'")
            routes.append({
                'path': pattern,
                'name': entry.name
            })
    return routes

def get_entity_count(entity_type):
    # Check if the entity_type is a relationship type or a node label, case-insensitively
    rel_query = f"MATCH ()-[r]->() WHERE type(r) =~ '(?i){entity_type}' RETURN COUNT(r)"
    node_query = f"MATCH (n) WHERE any(label in labels(n) WHERE label =~ '(?i){entity_type}') RETURN COUNT(n)"

    rel_count, _ = db.cypher_query(rel_query)
    node_count, _ = db.cypher_query(node_query)

    if rel_count[0][0] > 0:  # The entity_type is a relationship type
        count = rel_count
    elif node_count[0][0] > 0:  # The entity_type is a node label
        count = node_count
    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

    return count[0][0]

def count_all_entities():
    # Get all unique node labels
    node_labels_query = "CALL db.labels()"

    # Get all unique relationship types
    rel_types_query = "CALL db.relationshipTypes()"

    # Execute the Cypher queries and retrieve the results
    node_labels, _ = db.cypher_query(node_labels_query)
    rel_types, _ = db.cypher_query(rel_types_query)

    entity_counts = []

    # Count instances for each node label
    for label in node_labels:
        count_query = f"MATCH (n:{label[0]}) RETURN COUNT(n)"
        count, _ = db.cypher_query(count_query)
        entity_counts.append((label[0], count[0][0]))

    # Count instances for each relationship type
    for rel_type in rel_types:
        count_query = f"MATCH ()-[r:{rel_type[0]}]->() RETURN COUNT(r)"
        count, _ = db.cypher_query(count_query)
        entity_counts.append((rel_type[0], count[0][0]))

    return entity_counts

# Define the get_weights_by_target function, which retrieves a list of adverse events
# and their associated log likelihood ratios (llr) for a given protein target.
def get_weights_by_target(target, adverse_event=None, action_types=None, drug=None, count=None):
    # Find active datasets and store them in the enabledSets variable.
    enabled_datasets_query = "MATCH (nd:Dataset {enabled: true}) WITH COLLECT(nd.dataset) AS enabledSets"

    # Construct the TARGETS segment of the query to find drugs that target the specified protein.
    target_query = f"""
        MATCH (nd:Drug)-[rt:TARGETS]-(nt:Target)
        WHERE nd.dataset IN enabledSets
            AND rt.dataset IN enabledSets
            AND nt.dataset IN enabledSets
            AND toUpper(nt.symbol) = '{target.upper()}'
    """

    # Filter the results based on the drug parameter, if provided.
    if drug:
        target_query += f" AND nd.drug_id = '{drug}'"

    # Filter the results based on the action_types parameter, if provided.
    if action_types:
        action_types_str = ", ".join([f"'{action_type}'" for action_type in action_types])
        target_query += f" AND rt.actionType IN [{action_types_str}]"

    # Collect the drugs that target the specified protein and store them in the targetingDrugs variable.
    target_query += " WITH enabledSets, COLLECT(nd) AS targetingDrugs"

    # Construct the ASSOCIATED_WITH segment of the query to find adverse events associated with the targeting drugs.
    associated_query = f"""
        MATCH (nae:AdverseEvent)-[raw:ASSOCIATED_WITH]-(nd:Drug)
        WHERE nae.dataset IN enabledSets
            AND raw.dataset IN enabledSets
            AND nd.dataset IN enabledSets
            AND nd in targetingDrugs
    """

    # Filter the results based on the adverse_event parameter, if provided.
    if adverse_event:
        associated_query += f" AND nae.adverse_event_id = '{adverse_event}'"

    # Filter the results based on the drug parameter, if provided.
    if drug:
        associated_query += f" AND nd.drug_id = '{drug}'"

    # Define the return clause based on whether an adverse event is provided.
    # Calculate the sum of the llr values for each adverse event.
    if adverse_event:
        return_query = " RETURN nd, sum(toFloat(raw.llr))"
    else:
        return_query = " RETURN nae, sum(toFloat(raw.llr))"

    # Sort the results by the summed llr values in descending order.
    return_query += " ORDER BY sum(toFloat(raw.llr)) desc"

    # Limit the number of results returned based on the count parameter, if provided.
    if count:
        return_query += f" LIMIT {count}"

    # Combine all query segments to form the final Cypher query.
    cypher_query = f"{enabled_datasets_query}{target_query}{associated_query}{return_query}"

    # Run the Cypher query and retrieve the results.
    results, _ = db.cypher_query(cypher_query)

    # Format the results to match the Java version
    formatted_results = []

    # Loop through the results
    for res in results:
        # Create an entry as a dictionary for each result
        entry = {
            "llr": res[1],  # Store the log likelihood ratio (llr) value
            "id": res[0]["meddraId"],  # Store the MedDRA ID of the adverse event
            "type": "AdverseEvent",  # Specify the result type as AdverseEvent
            "meddraId": res[0]["meddraId"],  # Store the MedDRA ID again (for compatibility)
            "name": res[0]["adverseEventId"],  # Store the name of the adverse event
            "dataset": res[0]["dataset"].replace(" ", ""),  # Store the dataset name with spaces removed
            "datasetCommandString": f"dataset: '{res[0]['dataset']}'"  # Store the dataset command string
        }
        # Add the formatted entry to the list of formatted results
        formatted_results.append(entry)

    # Return the list of formatted results
    return formatted_results

def clear_neo4j_database():
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "gradvek1")
    # Connect to Neo4j database
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # Delete all nodes and relationships in the database
        session.run("MATCH (n) DETACH DELETE n")

    # Close the Neo4j driver
    driver.close()

def suggestion_by_hint_for_target(hint):
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "gradvek1")


    driver = GraphDatabase.driver(URI, auth=AUTH)
    # Define the Cypher query to search for target entries
    cypher_query = """
        MATCH (t:Target)
        WHERE
            toLower(t.name) CONTAINS toLower($hint) OR
            toLower(t.symbol) CONTAINS toLower($hint) OR
            toLower(t.ensembleId) CONTAINS toLower($hint)
        RETURN t.name AS name, t.symbol AS symbol, t.ensembleId AS ensembleId
        LIMIT 12
    """

    # Execute the Cypher query with the hint as a parameter
    with driver.session() as session:
        result = session.run(cypher_query, {"hint": hint})
    
        # Extract the name, symbol, and ensembleId properties from the results
        results_list = []
        for record in result:
            result_dict = {
                "name": record["name"],
                "symbol": record["symbol"],
                "ensembleId": record["ensembleId"]
            }
            results_list.append(result_dict)

    # Close the Neo4j driver
    driver.close()

    print(json.dumps(results_list))
    # Return the results_list as a JSON string
    return json.dumps(results_list)