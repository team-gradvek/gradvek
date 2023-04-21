import locale
import re
import string
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver
from neomodel import db, config
from neomodel import NodeSet
from neomodel.core import NodeMeta
from neomodel.relationship import RelationshipMeta
from py2neo import Path

# Import local modules
from .Cytoscape import Node, Relationship
from .queries.actions import get_actions
from .queries.datasets import DATASETS
from neo4j import GraphDatabase
import json
from typing import List, Dict, Tuple, Union




# # For easily access each of the model classes programmatically, create a key-value map.
# MODEL_ENTITIES = {
#     'Drug': Drug,

# }

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "gradvek1")

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


def get_weights_by_target(target, adverse_event=None, action_types=None, drug=None, count=None):
    """
    Retrieve a list of adverse events and their associated log likelihood ratios (llr) for a given protein target.

    Args:
        target (str): The symbol of the protein target.
        adverse_event (str, optional): The ID (meddraId) of a specific adverse event.
        action_types (list, optional): A list of action types to filter the results by.
        drug (str, optional): The ID of a specific drug to filter the results by.
        count (int, optional): The maximum number of results to return.

    Returns:
        list: A list of formatted results containing either adverse events or drugs and their associated llr.
    """

    # Find active datasets and store them in the enabledSets variable.
    # This query will search for nodes labeled 'Dataset' with a property 'enabled' set to true.
    enabled_datasets_query = "MATCH (nd:Dataset {enabled: true}) WITH COLLECT(nd.dataset) AS enabledSets"

    # Construct the TARGETS segment of the query to find drugs that target the specified protein.
    # This part of the query searches for relationships labeled 'TARGETS' between Drug nodes and Target nodes.
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
        action_types_str = ", ".join(
            [f"'{action_type}'" for action_type in action_types])
        target_query += f" AND rt.actionType IN [{action_types_str}]"

    # Collect the drugs that target the specified protein and store them in the targetingDrugs variable.
    target_query += " WITH enabledSets, COLLECT(nd) AS targetingDrugs"

    # Construct the ASSOCIATED_WITH segment of the query to find adverse events associated with the targeting drugs.
    # This part of the query searches for relationships labeled 'ASSOCIATED_WITH' between AdverseEvent nodes and Drug nodes.
    associated_query = f"""
        MATCH (nae:AdverseEvent)-[raw:ASSOCIATED_WITH]-(nd:Drug)
        WHERE nae.dataset IN enabledSets
            AND raw.dataset IN enabledSets
            AND nd.dataset IN enabledSets
            AND nd in targetingDrugs"""

    # Filter the results based on the adverse_event parameter, if provided.
    if adverse_event:
        associated_query += f" AND nae.meddraId = '{adverse_event}'"

    # Define the return clause based on whether an adverse event is provided.
    # Calculate the sum of the llr values for each adverse event or drug.
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

    # print(cypher_query)

    # Format the results to match the Java version
    formatted_results = []

    # Loop through the results obtained from the Cypher query to format the data for output.
    # Each entry in the results is a tuple with the first item being a node (either a drug or adverse event)
    # and the second item being the summed Log Likelihood Ratio (LLR) value.
    for res in results:
        # If an adverse_event parameter was provided, the output should include information on the drugs.
        if adverse_event:
            entry = {
                "drugId": res[0]["chemblId"],  # The Chembl ID of the drug node.
                "weight": res[1],             # The summed LLR value for the association.
                "drugName": res[0]["drugId"]  # The internal drug ID of the drug node.
            }
        # If an adverse_event parameter was not provided, the output should include information on the adverse events.
        else:
            entry = {
                "llr": res[1],                                 # The summed LLR value for the association.
                "id": res[0]["meddraId"],                      # The MedDRA ID of the adverse event node.
                "type": "AdverseEvent",                        # The type of node (in this case, AdverseEvent).
                "meddraId": res[0]["meddraId"],                # The MedDRA ID of the adverse event node.
                "name": res[0]["adverseEventId"],             # The internal adverse event ID of the node.
                "dataset": res[0]["dataset"].replace(" ", ""),# The dataset the adverse event node belongs to (whitespace removed).
                "datasetCommandString": f"dataset: '{res[0]['dataset']}'"  # The dataset string in command format.
            }
    
    # Append the formatted entry to the list of formatted results.
    formatted_results.append(entry)

    # Return the list of formatted results
    return formatted_results


def clear_neo4j_database():

    # Connect to Neo4j database
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # Delete all nodes and relationships in the database
        session.run("MATCH (n) DETACH DELETE n")

    # Close the Neo4j driver
    driver.close()