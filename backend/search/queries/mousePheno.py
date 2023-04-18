from neomodel import db


def get_actions(target):

    # Change cyper query if target symbol
    if target == "":
        cmd_filter = ""
    else:
        cmd_filter = f'WHERE toUpper(nt.symbol) = "{target}"'

    # Check if the mouse graph already exists, create if not
    exists = db.cypher_query('''
        CALL gds.graph.exists("mousePheno")
        YIELD graphName, exists
        RETURN exists
        ''')[0]
    if not exists:
        db.cypher_query('''
            CALL gds.graph.project(
                'mousePheno',
                ['Target', 'MousePhenotype'],
                {
                    MOUSE_PHENOTYPE: {}
                });
        ''')

    # run similarity calcs
    #TODO: add filter in this query or afterwards to just searched target
    results = db.cypher_query(
        f'''
        CALL gds.nodeSimilarity.stream(
            "mousePheno"
        ) YIELD
            node1,
            node2,
            similarity
        Return 
            gds.util.asNode(node1).ensembleId, 
            gds.util.asNode(node2).ensembleId, 
            similarity
        '''
    )

    return results