from neomodel import db


def get_hprotein(target):
    # Check if the mouse graph already exists in the database
    exists = db.cypher_query(
        '''
        CALL gds.graph.exists("hprotein")
        YIELD graphName, exists
        RETURN exists
        '''
    )

    # If the graph does not exist, create it using gds.graph.project
    if exists[0][0][0] == False:
        db.cypher_query(
            '''
            CALL gds.graph.project(
                'hprotein',
                ['Target', 'Baseline_Expression'],
                {
                    HPROTEIN: {}
                });
            '''
        )

    # Run similarity calculations using the gds.nodeSimilarity.stream algorithm
    results = db.cypher_query(
        f'''
        CALL gds.nodeSimilarity.stream(
            "hprotein"
        ) YIELD
            node1,
            node2,
            similarity
        WITH gds.util.asNode(node1) AS n1, gds.util.asNode(node2) AS n2, similarity
        WHERE toLower(n1.symbol) = toLower("{target}")
        RETURN n1.symbol, n2.symbol, similarity
        ORDER BY similarity DESC
        '''
    )[0]

    # Flatten the list of lists returned from the query results
    flat_list = [pair for res in results for pair in res]

    # Convert the flat list into a list of dictionaries
    lst_to_dict = [{'target1': flat_list[i], 'target2': flat_list[i + 1], 'similarity': flat_list[i + 2]} for i in range(0, len(flat_list), 3)]

    # Assign the list of dictionaries to the PHENO variable and return it
    PHENO = lst_to_dict
    return PHENO
