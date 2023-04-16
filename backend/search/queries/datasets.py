from neomodel import db

# This Cypher query retrieves distinct dataset values from all nodes in the Neo4j database
unique_datasets = db.cypher_query(
    '''
    MATCH (n)
    RETURN DISTINCT n.dataset     
    '''
)[0]

# Create a list of dictionaries containing unique dataset values
DATASETS = [dataset for subset in unique_datasets for dataset in subset]