from django.urls import URLPattern, URLResolver
from neomodel import db
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
            # Combine the current prefix with the entry's pattern, removing the '^' at the beginning
            new_prefix = prefix + entry.pattern.regex.pattern.lstrip('^')
            # Recursively process the nested URL patterns
            routes.extend(get_all_routes(entry.url_patterns, new_prefix))
        elif isinstance(entry, URLPattern):
            # Combine the current prefix with the entry's pattern, removing the '^' at the beginning
            pattern = prefix + entry.pattern.regex.pattern.lstrip('^')
            # Replace double backslashes with single ones
            pattern = pattern.replace('\\\\', '\\')
            # Remove the '\\Z' at the end of the pattern
            pattern = pattern.rstrip('\\Z')
            routes.append({
                'path': pattern,
                'name': entry.name
            })
    return routes
