import re
import string
from django.urls import URLPattern, URLResolver
from neomodel import db, config
from neomodel import NodeSet
from neomodel.core import NodeMeta
from neomodel.relationship import RelationshipMeta
from .queries.actions import get_actions
from .queries.datasets import DATASETS



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
