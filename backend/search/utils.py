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
from neo4j import GraphDatabase
import json
from typing import List, Dict, Tuple, Union

# Import local modules
from .Cytoscape import Node, Relationship

# Import query functions
from .queries.actions import get_actions
from .queries.datasets import DATASETS
from .queries.node_similarity import node_similarity
# from .queries.gwas import get_gwas
# from .queries.hgene import get_hgene
# from .queries.hprotein import get_hprotein
# from .queries.intact import get_intact
# from .queries.pathway import get_pathway
# from .queries.reactome import get_reactome
# from .queries.signor import get_signor


def fetch_actions(target):
    ACTIONS = get_actions(target)
    return ACTIONS


def fetch_datasets():
    return DATASETS

# TODO ADD to startup instead
def fetch_similarity(descriptor):
    node_similarity(descriptor)
    return print("DONE !")


# def fetch_pheno():
#     RESULTS = get_pheno()
#     return RESULTS

# def fetch_gwas(target):
#     RESULTS = get_gwas(target)
#     return RESULTS

# def fetch_hgene(target):
#     RESULTS = get_hgene(target)
#     return RESULTS

# def fetch_hprotein(target):
#     RESULTS = get_hprotein(target)
#     return RESULTS

# def fetch_intact(target):
#     RESULTS = get_intact(target)
#     return RESULTS

# def fetch_pathway(target):
#     RESULTS = get_pathway(target)
#     return RESULTS

# def fetch_reactome(target):
#     RESULTS = get_reactome(target)
#     return RESULTS

# def fetch_signor(target):
#     RESULTS = get_signor(target)
#     return RESULTS

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

def get_paths_target_ae_drug(target, action_types=None, adverse_event=None, drug=None, count=None):
    """
    This function finds paths between the given target, adverse events, and drugs. 
    It returns the results as a list of paths.
    Args:
        target (str): The symbol of the protein target.
        action_types (list, optional): A list of action types to filter the results by.
        adverse_event (str, optional): The ID (meddraId) of a specific adverse event.
        drug (str, optional): The ID of a specific drug to filter the results by.
        count (int, optional): The maximum number of results to return.
    Returns:
        list: A list of paths between the given target, adverse events, and drugs.
    """
    # Find active datasets and store them in the enabledSets variable.
    enabled_datasets_query = "MATCH (nd:Dataset {enabled: true}) WITH COLLECT(nd.dataset) AS enabledSets"

    # Construct the TARGETS segment of the query to find drugs that target the specified protein.
    # This part of the query searches for paths between adverse events, drugs, and the given target.
    target_query = f"""
        {enabled_datasets_query}
        MATCH path=(nae:AdverseEvent)-[raw:ASSOCIATED_WITH]-(nd:Drug)-[rt:TARGETS]-(nt:Target)
        WHERE nae.dataset IN enabledSets
            AND raw.dataset IN enabledSets
            AND nd.dataset IN enabledSets
            AND rt.dataset IN enabledSets
            AND nt.dataset IN enabledSets
            AND toUpper(nt.symbol) = '{target.upper()}'
    """

    # Filter the results based on the adverse_event parameter, if provided.
    if adverse_event:
        target_query += f" AND nae.adverse_event_id = '{adverse_event}'"

    # Filter the results based on the drug parameter, if provided.
    if drug:
        target_query += f" AND nd.drug_id = '{drug}'"

    # Add RETURN clause for target_query
    target_query += " RETURN path"

    # Construct the PART_OF segment of the query to find pathways related to the specified target.
    # This part of the query searches for paths between the given target and related pathways.
    path_query = f"""
        {enabled_datasets_query}
        MATCH path=(nt:Target)-[rpi:PARTICIPATES_IN]-(np:Pathway)
        WHERE nt.dataset IN enabledSets
            AND rpi.dataset IN enabledSets
            AND np.dataset IN enabledSets
            AND toUpper(nt.symbol) = '{target.upper()}'
        RETURN path
    """

    # Construct the DRUG_TARGETS segment of the query to find targets of drugs related to the specified target.
    # This part of the query searches for paths between drugs and the given target.
    drug_target_query = f"""
        {enabled_datasets_query}
        MATCH path=(nd:Drug)-[rt:TARGETS]-(nt:Target)
        WHERE nd.dataset IN enabledSets
            AND rt.dataset IN enabledSets
            AND nt.dataset IN enabledSets
            AND toUpper(nt.symbol) = '{target.upper()}'
    """

    # Filter the results based on the drug parameter, if provided.
    if drug:
        drug_target_query += f" AND nd.drug_id = '{drug}'"
        
    # Add RETURN clause for drug_target_query
    drug_target_query += " RETURN path"

    # Construct a query to find the target itself, in case no other paths are found.
    single_target_query = f"""
        {enabled_datasets_query}
        MATCH path=(nt:Target)
        WHERE nt.dataset IN enabledSets
            AND toUpper(nt.symbol) = '{target.upper()}'
        RETURN path
    """

    # Combine all segments of the Cypher query.
    cypher_query = f"{target_query} UNION {path_query} UNION {drug_target_query} UNION {single_target_query}"

    # Run the Cypher query and retrieve the results.
    results, _ = db.cypher_query(cypher_query)

    # Return the list of paths found.
    return results

def get_cytoscape_entities_as_json(paths):
    """
    This function processes the list of paths and converts them to a format that is
    compatible with the Cytoscape library, which is used for visualizing the graph.
    Args:
        paths (list): A list of paths between the given target, adverse events, and drugs.
    Returns:
        list: A list of dictionaries containing the entities involved in the paths formatted for Cytoscape.
    """
    # Initialize a dictionary to store the entities involved in the paths.
    entities_involved = {}

    # Helper function to process nodes in the graph. It checks if the node is already
    # in the entities_involved dictionary, and if not, adds it with the appropriate properties.
    def process_node(node):
        # Each entity for Cytoscape must have a unique id. Map node IDs to even numbers to ensure uniqueness.
        node_id = node.id * 2

        # If the node_id is not already in entities_involved, process the node.
        if node_id not in entities_involved:
            # Set the primary label for the node.
            primary_label = next(iter(node.labels), "Unknown")

            # Set the node_class based on the primary_label.
            node_class = primary_label.lower()
            if primary_label == "AdverseEvent":
                node_class = "adverse-event"

            # Convert node properties to a dictionary with appropriate keys.
            data_map = {key: str(node._properties.get(source, ''))
                        for key, source in Node.NODE_PROPERTY_MAP.get(primary_label, [])}
            data_map['id'] = str(node_id)
            if 'targetId' in data_map:
                data_map['ensembleId'] = data_map.pop('targetId')

            # Add the processed node to the entities_involved dictionary.
            entities_involved[node_id] = Node(node_id, node_class, data_map)


    # Helper function to process relationships in the graph. It checks if the relationship is already
    # in the entities_involved dictionary, and if not, adds it with the appropriate properties.
    def process_relationship(relationship):
        # Map relationship IDs to odd numbers to ensure uniqueness.
        relationship_id = relationship.id * 2 + 1

        # If the relationship_id is not already in entities_involved, process the relationship.
        if relationship_id not in entities_involved:
            # Set start and end node IDs as even numbers.
            start_node_id = relationship.start_node.id * 2
            end_node_id = relationship.end_node.id * 2

            # Convert relationship properties to a dictionary with appropriate keys.
            data_map = {key: str(value)
                        for key, value in relationship._properties.items()}
            data_map.update({
                "id": str(relationship_id),
                "source": str(start_node_id),
                "target": str(end_node_id),
                "arrow": "vee",
                "action": relationship.type.replace("_", " ")
            })

            # Set the relationship_class based on the relationship type.
            relationship_class = relationship.type.lower().replace("_", "-")

            # Add the processed relationship to the entities_involved dictionary.
            entities_involved[relationship_id] = Relationship(
                relationship_id, relationship_class, data_map)

    # Process all nodes and relationships in the paths.
    for row in paths:
        path = row[0]
        # Process all nodes in the path.
        for node in path.nodes:
            process_node(node)
        # Process all relationships in the path.
        for relationship in path.relationships:
            process_relationship(relationship)

    # Convert the entities_involved values to a list of dictionaries and return the result.
    return [entity.to_dict() for entity in entities_involved.values()]

def clear_neo4j_database():
    # Cypher query to detach and delete all nodes in the database
    query = "MATCH (n) DETACH DELETE n"
    # Execute the query
    db.cypher_query(query)

def suggestion_by_hint_for_target(hint):
    # Define the Cypher query to search for target nodes that match the hint
    cypher_query = """
        MATCH (t:Target)
        WHERE
            toLower(t.name) CONTAINS toLower($hint) OR
            toLower(t.symbol) CONTAINS toLower($hint) OR
            toLower(t.ensembleId) CONTAINS toLower($hint)
        RETURN t.name AS name, t.symbol AS symbol, t.ensembleId AS ensembleId
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"name": r[0], "symbol": r[1], "ensembleId": r[2]} for r in result]
    # Return the list
    return results_list

def suggestion_by_hint_for_adverse_event(hint):
    # Define the Cypher query to search for adverse event nodes that match the hint
    cypher_query = """
        MATCH (t:AdverseEvent)
        WHERE
            toLower(t.meddraId) CONTAINS toLower($hint) OR
            toLower(t.adverseEventId) CONTAINS toLower($hint)
        RETURN t.meddraId AS meddraId, t.adverseEventId AS adverseEventId
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"meddraId": r[0], "adverseEventId": r[1]} for r in result]
    # Return the list
    return results_list

def suggestion_by_hint_for_disease(hint):
    # Define the Cypher query to search for disease nodes that match the hint
    cypher_query = """
        MATCH (t:Disease)
        WHERE
            toLower(t.name) CONTAINS toLower($hint) OR
            toLower(t.diseaseId) CONTAINS toLower($hint)
        RETURN t.name AS name, t.diseaseId AS diseaseId
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"name": r[0], "diseaseId": r[1]} for r in result]
    # Return the list
    return results_list

def suggestion_by_hint_for_drug(hint):
    # Define the Cypher query to search for drug nodes that match the hint
    cypher_query = """
        MATCH (t:Drug)
        WHERE
            toLower(t.chemblId) CONTAINS toLower($hint) OR
            toLower(t.drugId) CONTAINS toLower($hint)
        RETURN t.chemblId AS chemblId, t.drugId AS drugId
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"chemblId": r[0], "drugId": r[1]} for r in result]
    # Return the list
    return results_list


def suggestion_by_hint_for_mouse_phenotype(hint):
    # Define the Cypher query to search for mouse phenotype nodes that match the hint
    cypher_query = """
        MATCH (t:MousePhenotype)
        WHERE
            toLower(t.mousePhenotypeLabel) CONTAINS toLower($hint) OR
            toLower(t.mousePhenotypeId) CONTAINS toLower($hint)
        RETURN t.mousePhenotypeLabel AS mousePhenotypeLabel, t.mousePhenotypeId AS mousePhenotypeId
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"mousePhenotypeLabel": r[0], "mousePhenotypeId": r[1]} for r in result]
    # Return the list
    return results_list

def suggestion_by_hint_for_pathway(hint):
    # Define the Cypher query to search for pathway nodes that match the hint
    cypher_query = """
        MATCH (t:Pathway)
        WHERE
            toLower(t.pathwayCode) CONTAINS toLower($hint) OR
            toLower(t.pathwayId) CONTAINS toLower($hint) OR
            toLower(t.topLevelTerm) CONTAINS toLower($hint)
        RETURN t.pathwayCode AS pathwayCode, t.pathwayId AS pathwayId, t.topLevelTerm AS topLevelTerm
        LIMIT 12
    """
    # Execute the query with the hint as a parameter
    result, _ = db.cypher_query(cypher_query, {"hint": hint})
    # Transform the result into a list of dictionaries
    results_list = [{"pathwayCode": r[0], "pathwayId": r[1], "topLevelTerm": r[2]} for r in result]
    # Return the list
    return results_list
