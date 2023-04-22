from neomodel import db


def get_pheno(target):

    # Check if the mouse graph already exists, create if not
    exists = db.cypher_query(
        '''
        CALL gds.graph.exists("mousePheno")
        YIELD graphName, exists
        RETURN exists
        ''')
  
    if not exists:
        db.cypher_query(
            '''
            CALL gds.graph.project(
                'mousePheno',
                ['Target', 'MousePhenotype'],
                {
                    MOUSE_PHENOTYPE: {}
                });
            ''')
    
    # Run similarity calcs
    results = db.cypher_query(
        f'''
        CALL gds.nodeSimilarity.stream(
            "mousePheno"
        ) YIELD
            node1,
            node2,
            similarity
        WITH gds.util.asNode(node1) AS n1, gds.util.asNode(node2)AS n2, similarity
        WHERE n1.symbol = "{target}"
        RETURN n1.symbol, n2.symbol, similarity
        ORDER BY similarity DESC
        '''
    )[0]

    # Flat list out of list of lists
    flat_list = [pair for res in results for pair in res]
    # Convert list to dictionary 
    lst_to_dict = [{'target1':flat_list[i], 'target2':flat_list[i+1], 'similarity':flat_list[i+2]} for i in range(0,len(flat_list),3)]
    PHENO = lst_to_dict

    return PHENO