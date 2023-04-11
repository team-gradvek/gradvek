from neomodel import db


countries = db.cypher_query(
    '''
    MATCH (n)
    WHERE NOT n.countries CONTAINS ';'
    RETURN DISTINCT n.countries AS countries
    '''
)[0]