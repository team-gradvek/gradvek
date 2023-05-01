from neomodel import db
from search.models import (
    MousePheno,
    Hgene,
    Hprotein,
    Intact,
    Pathway,
    Reactome,
    Signor,
    Gwas,
    )


descriptors = {
    "mousepheno": ["MousePhenotype","MOUSE_PHENOTYPE", MousePheno],
    "hgene": ["Baseline_Expression", "HGENE", Hgene],
    "hprotein": ["Baseline_Expression", "HPROTEIN", Hprotein],
    "intact": ["Target", "INTACT", Intact],
    "pathway": ["TargetPathway", "PATHWAY", Pathway],
    "reactome": ["Target", "REACTOME", Reactome],
    "signor": ["Target", "SIGNOR", Signor],
    "gwas": ["Gwas","GWAS_RELATION", Gwas],
}


def get_node_similarity_results(descriptor):

    type_name = descriptors.get(descriptor)[0]
    edge_name = descriptors.get(descriptor)[1]
    model_class = descriptors.get(descriptor)[2]

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

    create_objects_to_db(descriptor, results, model_class)
    print(f"{descriptor} objects done!")


def create_objects_to_db(descriptor, results, model_class):
    
    print(f"Creating {descriptor} objects...")

    for row in results:
        model_class.objects.create(
            target1=row[0],
            target2=row[1],
            similarity=row[2]
        )