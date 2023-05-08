import atexit
import os
import time
from django.conf import settings
from django.core.management import call_command
import importlib
import environ
from neomodel import config, db
from datasets.get_datasets import get_datasets

'''
 This file contains functions that are run when the Django application starts up. It is imported in
 backend/search/apps.py and the run_startup_tasks function is called from the ready function in that file.
'''

# Initialize environment variables
env = environ.Env()

# Read environment variables from .env file
environ.Env.read_env()


NEO4J_DOCKER_USERNAME = os.getenv("NEO4J_DOCKER_USERNAME", default=None)
NEO4J_DOCKER_PASSWORD = os.getenv("NEO4J_DOCKER_PASSWORD", default=None)
NEO4J_DOCKER_URL = os.getenv("NEO4J_DOCKER_URL", default=None)
NEO4J_USERNAME = env("NEO4J_USERNAME", default=NEO4J_DOCKER_USERNAME)
NEO4J_PASSWORD = env("NEO4J_PASSWORD", default=NEO4J_DOCKER_PASSWORD)
NEO4J_BOLT_URL = env("NEO4J_BOLT_URL", default=None)



# Function to close Neo4j driver when the application exits
def close_driver():
    if db.driver:
        db.driver.close()

# Register the close_driver function to be called when the application exits
atexit.register(close_driver)

def check_neo4j_connection():
    # Function to check Neo4j connection by executing a simple Cypher query.
    try:
        # Execute a simple Cypher query to check the connection
        query = "MATCH (n) RETURN COUNT(n) AS node_count"
        results, meta = db.cypher_query(query)

        # Check if the query was successful
        if results is not None:
            return True
        else:
            return False
    except Exception as e:
        #print(f"Neo4j connection error: {e}")
        return False

def wait_for_neo4j_connection():
    # Function to wait for Neo4j connection to be established. It will retry the connection 10 times with a 5 second
    # delay between each attempt.
    retry = 0
    max_retries = 10

    # Use NEO4J_DOCKER_URL environment variable if available
    if NEO4J_DOCKER_URL:
        neo4j_url = NEO4J_DOCKER_URL
    else:
        neo4j_url = NEO4J_BOLT_URL
    
    config.DATABASE_URL = neo4j_url
    config.MAX_CONNECTION_LIFETIME = 3600 * 3 # 3 hours
    
    while retry < max_retries:
        try:
            if check_neo4j_connection():
                print("Neo4j connection established.")
                break
            else:
                retry += 1
                print(f"Waiting for Neo4j connection... ({retry}/{max_retries})")
                time.sleep(5)
        except Exception as e:
            retry += 1
            print(f"Waiting for Neo4j connection... ({retry}/{max_retries})")
            time.sleep(5)



def run_startup_tasks():
    # Function to run startup tasks
    get_datasets()
    wait_for_neo4j_connection()

    # Dynamically import parse_datasets module, this is done to better manage the neo4j connections
    parse_datasets_module = importlib.import_module('datasets.parse_datasets', package='datasets')
    parse_datasets_module.parse_datasets()

    print("Saving similarity results to Django db...")
    search_datasets_module = importlib.import_module('search.queries.node_similarity', package='search')
    search_datasets_module.save_to_db()
