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
    "mousepheno": ["MousePhenotype", "MOUSE_PHENOTYPE", MousePheno, "SIMILAR_MOUSEPHENO"],
    "hgene": ["Baseline_Expression", "HGENE", Hgene, "SIMILAR_HGENE"],
    "hprotein": ["Baseline_Expression", "HPROTEIN", Hprotein, "SIMILAR_HPROTEIN"],
    "intact": ["Target", "INTACT", Intact, "SIMILAR_INTACT"],
    "pathway": ["TargetPathway", "PATHWAY", Pathway, "SIMILAR_PATHWAY"],
    "reactome": ["Target", "REACTOME", Reactome, "SIMILAR_REACTOME"],
    "signor": ["Target", "SIGNOR", Signor, "SIMILAR_SIGNOR"],
    # "gwas": ["Gwas","GWAS_RELATION", Gwas, "SIMILAR_GWAS"],
}



def save_to_db():
    """
    Save Neo4j similarity results to Django db
    """
    for descriptor, (type_name, edge_name, model_class, similarity_edge) in descriptors.items():
        # Get similarity results and save to database
        get_node_similarity_results(descriptor)



def get_node_similarity_results(descriptor):
    """
    Get all node similarity results associated with the descriptor from Neo4j db
    Use the Neo4j Graph Data Science library - write mode
    """

    type_name = descriptors.get(descriptor)[0]
    edge_name = descriptors.get(descriptor)[1]
    relationship_type = descriptors.get(descriptor)[3]

    try:
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

        # Check if the relationship already exists
        relationship_exists, _ = db.cypher_query(
            f'''
            MATCH ()-[r:{relationship_type}]-() 
            RETURN count(r) > 0 as exists
            '''
        )

        # If the relationship does not exist, run similarity calculations
        if not relationship_exists[0][0]:
            print(f"{descriptor} Running node similarity query...")
            # Run similarity calculations using the gds.nodeSimilarity.write algorithm
            result, _ = db.cypher_query(
                f'''
                CALL gds.nodeSimilarity.write(
                    "{descriptor}",
                    {{
                        writeRelationshipType: "{relationship_type}",
                        writeProperty: "score",
                        topK: 500
                    }}
                )
                YIELD nodesCompared, relationshipsWritten
                '''
            )

            nodes_compared = result[0][0]
            relationships_written = result[0][1]

            print(f"{descriptor} Node similarity query completed. Nodes compared: {nodes_compared}, relationships written: {relationships_written}")

        else:
            print(f"{descriptor} Relationship {relationship_type} already exists. Skipping node similarity query.")

    except Exception as e:
        print(f"Error in {descriptor} node similarity query: {e}")



if __name__ == "__main__":
    save_to_db()