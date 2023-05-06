from neomodel import db
from django.db import transaction
from datetime import datetime
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
    # "gwas": ["Gwas","GWAS_RELATION", Gwas],
}


def save_to_db():
    """
    Save Neo4j similarity results to Django db
    """
    for descriptor, (type_name, edge_name, model_class) in descriptors.items():
        # Check if the objects already exist in the database
        if model_class.objects.exists():
            print(f"{descriptor} objects already exist in database, skipping...")
            continue
        
        # Get similarity results and save to database
        get_node_similarity_results(descriptor)



def get_node_similarity_results(descriptor):
    """
    Get all node similarity results associated to descriptor from Neo4j db
    Use the Neo4j Graph Data Science library - stream mode
    """

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

    print(f"{descriptor} Running node similarity query...")
    # Run similarity calculations using the gds.nodeSimilarity.stream algorithm
    results = db.cypher_query(
        f'''
        CALL gds.nodeSimilarity.stream(
            "{descriptor}",
            {{topK: 200}}
        ) YIELD
            node1,
            node2,
            similarity
        WITH gds.util.asNode(node1) AS n1, gds.util.asNode(node2) AS n2, similarity
        RETURN n1.symbol, n2.symbol, similarity
        '''
    )[0]

    print(f"{descriptor} Node similarity query completed. Processing results...")

    create_objects_to_db(descriptor, results, model_class)


def create_objects_to_db(descriptor, results, model_class):
    """
    Save the results to the Django db based on the Descriptor Model
    """
    print(f"Creating {descriptor} objects...")

    try:
        start_time = datetime.now()
        print(f"Start time: {start_time}")
        
        with transaction.atomic():

            for row in results:
                # Fields need to match Django model
                model_class.objects.create(
                    target1=row[0],
                    target2=row[1],
                    similarity=row[2]
                )

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(f"End time: {end_time}")
        print(f"Elapsed time: {elapsed_time}")

        print(f"{descriptor} objects done!")

    except Exception as e:
        print(f"Error creating {descriptor} objects: {e}")


if __name__ == "__main__":
    save_to_db()