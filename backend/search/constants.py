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


ACTIONS = sorted([action[0] for action in actions])


    # MATCH (n) WHERE (n.actionType) IS NOT NULL 
    # RETURN DISTINCT "node" as entity, n.actionType AS actionType 
    # UNION ALL 
    # MATCH ()-[r]-() WHERE (r.actionType) IS NOT NULL 
    # RETURN DISTINCT "relationship" AS entity, r.actionType AS actionType 