from neomodel import db
from search.models import MousePheno

def node_similarity(descriptor):

    descriptors = {
        "mousepheno": ["MousePhenotype","MOUSE_PHENOTYPE"],
        "hgene": ["Baseline_Expression", "HGENE"],
        "hprotein": ["Baseline_Expression", "HPROTEIN"],
        "intact": ["Target", "INTACT"],
        "pathway": ["TargetPathway", "PATHWAY"],
        "reactome": ["Target", "REACTOME"],
        "signor": ["Target", "SIGNOR"],
        "gwas": ["Gwas","GWAS_RELATION"],
    }
 
    type_name = descriptors.get(descriptor)[0]
    edge_name = descriptors.get(descriptor)[1]

    # Check if the graph already exists in the database
    exists = db.cypher_query(
        f'''
        CALL gds.graph.exists("{descriptor}")
        YIELD graphName, exists
        RETURN exists
        '''
    )

    # If the graph does not exist, create it using gds.graph.project
    if exists[0][0][0] == False:
        db.cypher_query(
            f'''
            CALL gds.graph.project(
                '{descriptor}',
                ['Target', '{type_name}'],
                {{
                    {edge_name}: {{}}
                }});
            '''
        )

    # Run similarity calculations using the gds.nodeSimilarity.stream algorithm
    results = db.cypher_query(
        f'''
        CALL gds.nodeSimilarity.stream(
            "{descriptor}"
        ) YIELD
            node1,
            node2,
            similarity
        WITH gds.util.asNode(node1) AS n1, gds.util.asNode(node2) AS n2, similarity
        RETURN n1.symbol, n2.symbol, similarity
        '''
    )[0]

    # TODO HARD CODED TO REFACTOR
    if descriptor == "mousepheno":
        print(f"Creating {descriptor} objects...")

        for row in results:
            MousePheno.objects.create(
                target1=row[0],
                target2=row[1],
                similarity=row[2]
            )
        print(f"{descriptor} objects done!")