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
