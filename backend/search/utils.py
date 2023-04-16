import re
import string
from django.urls import URLPattern, URLResolver
from neomodel import db
from .queries import ACTIONS, DATASETS
from neo4j import GraphDatabase


# from .models import (
#     Drug,

# )

# # For easily access each of the model classes programmatically, create a key-value map.
# MODEL_ENTITIES = {
#     'Drug': Drug,

# }

def fetch_actions():
    return ACTIONS


def fetch_datasets():
    return DATASETS


def update_dataset_status(dataset_name, enabled):
    query = f"MATCH (d:Dataset {{ dataset: '{dataset_name}' }}) SET d.enabled={enabled}"
    db.cypher_query(query)

# Function to return all api routes from the URL patterns
def get_all_routes(urlpatterns, prefix=''):
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
    # Convert the input entity_type to lowercase for comparison
    entity_type = entity_type.lower()

    # Define a mapping from lowercase entity types to their correct formats
    entity_type_mapping = {
        'adverseevent': 'AdverseEvent',
        'drug': 'Drug',
        'gene': 'Gene',
        'target': 'Target',
        'mousephenotype': 'MousePhenotype',
        'pathway': 'Pathway',
        'dataset': 'Dataset',
        'associatedwith': 'AssociatedWith',
        'mechanismofaction': 'MechanismOfAction',
        'action': 'Action',
        'involves': 'Involves',
        'participates': 'Participates',
    }

    # Map the user input to the correct entity_type format
    entity_type = entity_type_mapping.get(entity_type)
    if entity_type is None:
        raise ValueError(f"Invalid entity type: {entity_type}")

    # Define a set of simple entity types
    simple_entities = {
        'AdverseEvent', 'Drug', 'Gene', 'Target', 'MousePhenotype', 'Pathway', 'Dataset'
    }

    # Define a dictionary of relation entity types with the related node labels
    relation_entities = {
        'AssociatedWith': ("Drug", "AdverseEvent"),
        'MechanismOfAction': ("Drug", "Target"),
        'Action': ("Drug", "Target"),
        'Involves': ("Target", "Gene"),
        'Participates': ("Target", "Pathway"),
    }

    # Check if the entity_type is a simple entity or a relation entity, and build the corresponding Cypher query
    if entity_type in simple_entities:
        query = f"MATCH (n:{entity_type}) RETURN COUNT(n)"
    elif entity_type in relation_entities:
        node1, node2 = relation_entities[entity_type]
        query = f"MATCH (:{node1})-[n]->(:{node2}) RETURN COUNT(n)"
    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

    # Execute the Cypher query and return the count of the requested entity type
    results, _ = db.cypher_query(query)
    return results[0][0]


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




