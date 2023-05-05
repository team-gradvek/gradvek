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
    AverageSimilarity,
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
    "averagesimilarity": ["AverageSimilarity", "AVERAGE_SIMILARITY", AverageSimilarity],
}

def save_average_similarity_to_db(similarity_results):
    """
    Calculate and save average similarity scores to the Django db
    """
    if AverageSimilarity.objects.exists():
        print("AverageSimilarity objects already exist in database, skipping...")
        return

    print("Creating AverageSimilarity objects...")

    # Combine all similarity results into a single dictionary
    combined_results = {}
    for descriptor, results in similarity_results.items():
        for row in results:
            pair = tuple(sorted((row[0], row[1])))
            if pair not in combined_results:
                combined_results[pair] = []
            combined_results[pair].append(row[2])

    # Calculate average similarity scores and save to database
    for pair, similarities in combined_results.items():
        average_similarity = sum(similarities) / len(similarities)
        AverageSimilarity.objects.create(
            target1=pair[0],
            target2=pair[1],
            average_similarity=average_similarity
        )

    print("AverageSimilarity objects done!")


def save_to_db():
    """
    Save Neo4j similarity results to Django db and calculate average similarity
    """

    # Dictionary to store similarity results for each descriptor
    similarity_results = {}

    for descriptor, (type_name, edge_name, model_class) in descriptors.items():
        if(descriptor == "averagesimilarity"):
            continue
        # Check if the objects already exist in the database
        if model_class.objects.exists():
            print(f"{descriptor} objects already exist in database, skipping...")
            continue

        # Get similarity results and save to database
        results = get_node_similarity_results(descriptor)
        similarity_results[descriptor] = results

    # Calculate and save average similarity scores to database
    save_average_similarity_to_db(similarity_results)


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
    """"
    Save the results to the Django db based on the Descriptor Model
    """
    print(f"Creating {descriptor} objects...")

    for row in results:
        # Fields need to match Django model
        model_class.objects.create(
            target1=row[0],
            target2=row[1],
            similarity=row[2]
        )

if __name__ == "__main__":
    save_to_db()