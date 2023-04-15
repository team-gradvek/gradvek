import re
import string
from django.urls import URLPattern, URLResolver
from neomodel import db, config
from neomodel import NodeSet
from neomodel.core import NodeMeta
from neomodel.relationship import RelationshipMeta
from .queries import ACTIONS, DATASETS


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
    # Check if the entity_type is a relationship type or a node label, case-insensitively
    rel_query = f"MATCH ()-[r]->() WHERE type(r) =~ '(?i){entity_type}' RETURN COUNT(r) LIMIT 1"
    node_query = f"MATCH (n) WHERE any(label in labels(n) WHERE label =~ '(?i){entity_type}') RETURN COUNT(n) LIMIT 1"

    rel_count, _ = db.cypher_query(rel_query)
    node_count, _ = db.cypher_query(node_query)

    if rel_count[0][0] > 0:  # The entity_type is a relationship type
        count_query = f"MATCH ()-[r]->() WHERE type(r) =~ '(?i){entity_type}' RETURN COUNT(r)"
    elif node_count[0][0] > 0:  # The entity_type is a node label
        count_query = f"MATCH (n) WHERE any(label in labels(n) WHERE label =~ '(?i){entity_type}') RETURN COUNT(n)"
    else:
        raise ValueError(f"Invalid entity type: {entity_type}")

    count, _ = db.cypher_query(count_query)
    return count[0][0]
