from neomodel import db


actions = db.cypher_query(
    '''
    MATCH (:Drug)-[rt:TARGETS]-(:Target) 
    WITH DISTINCT rt.actionType AS actType 
    OPTIONAL MATCH (:Drug)-[rt2:TARGETS {actionType: actType}]-(nt:Target) 
    RETURN actType, COUNT(rt2) 
    ORDER BY actType
    '''
)[0]


ACTIONS = sorted([action for action in actions])
# ACTIONS = {key: value for key, value in zip(key, value)}


# This Cypher query retrieves distinct dataset values from all nodes in the Neo4j database
unique_datasets = db.cypher_query(
    '''
    MATCH (n)
    RETURN DISTINCT n.dataset     
    '''
)[0]

# Create a list of dictionaries containing unique dataset values
DATASETS = [dataset for subset in unique_datasets for dataset in subset]