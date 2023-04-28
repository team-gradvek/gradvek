import atexit
import time
from django.conf import settings
from django.core.management import call_command
import importlib
import environ
from neomodel import config, db
from datasets.get_datasets import get_datasets

# Initialize environment variables
env = environ.Env()

# Read environment variables from .env file
environ.Env.read_env()

NEO4J_USERNAME = env("NEO4J_USERNAME")
NEO4J_PASSWORD = env("NEO4J_PASSWORD")


# Function to close Neo4j driver when the application exits
def close_driver():
    if db.driver:
        db.driver.close()

# Register the close_driver function to be called when the application exits
atexit.register(close_driver)

def check_neo4j_connection():
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
    retry = 0
    max_retries = 10
    while retry < max_retries:
        try:
            # Set up Neo4j database connection using environment variables
            config.DATABASE_URL = env("NEO4J_BOLT_URL")
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
    get_datasets()
    wait_for_neo4j_connection()

    # Dynamically import parse_datasets module
    parse_datasets_module = importlib.import_module('datasets.parse_datasets', package='datasets')
    parse_datasets_module.parse_datasets()
