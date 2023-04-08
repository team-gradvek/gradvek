import os
import pyarrow.parquet as pq

# Set dataset name
dataset = "opentarget 23.02"

def main():
    # Get the current working directory
    current_dir = os.getcwd()
    # Set the input directory for the opentarget data
    input_dir = f"{current_dir}/opentarget"

    # TODO:
    # Action (edge), Pathway (entity) - appears to not use any data source?
    # Gene (entity), Involves (edge) - these seem to only come from csv
    # mechanismOfAction (edge) is missing entry data, needs to be updates

    # Define data_type_query_generators, a dictionary that maps data types to tuples (node_query_generator, edge_query_generator)
    data_type_query_generators = {
        "targets": (create_cypher_query_targets, create_cypher_query_participates),
        "fda": (create_cypher_query_adverse_events, create_cypher_query_associated_with),
        "molecule": (create_cypher_query_drugs, None),
        "mechanismOfAction": (None, create_cypher_query_mechanism_of_action),
        "mousePhenotypes": (create_cypher_query_mouse_phenotypes, None),
        "diseases": (create_cypher_query_diseases, None)
    }

    # Iterate over each data type in the input directory for node query generators
    for data_type in os.listdir(input_dir):
        # Set the data_type_path
        data_type_path = os.path.join(input_dir, data_type)
        # Check if the path is a directory
        if not os.path.isdir(data_type_path):
            continue

        # Run the node query generator for the current data type
        node_query_generator = data_type_query_generators[data_type][0]
        if node_query_generator is not None:
            generate_queries(data_type, data_type_path, node_query_generator)

    # Iterate over each data type in the input directory for edge query generators
    for data_type in os.listdir(input_dir):
        # Set the data_type_path
        data_type_path = os.path.join(input_dir, data_type)
        # Check if the path is a directory
        if not os.path.isdir(data_type_path):
            continue

        # Run the edge query generator for the current data type
        edge_query_generator = data_type_query_generators[data_type][1]
        if edge_query_generator is not None:
            generate_queries(data_type, data_type_path, edge_query_generator)


def generate_queries(data_type, data_type_path, query_generator):
    if query_generator is None:
        return

    # List all parquet files in the data_type_path
    files = [file for file in os.listdir(data_type_path) if file.endswith(".parquet")]

    # Iterate over each file and read its content
    for n, file in enumerate(files):
        print(f"Processing {data_type} file {n+1}/{len(files)}")
        file_path = os.path.join(data_type_path, file)
        try:
            table = pq.read_table(file_path)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        try:
            # Generate queries for the current table
            queries = query_generator(table)

            # Print queries for the current file
            # TODO Replace this with neo4j function to evaluate the cypher queries
            for query in queries:
                print(query)

        except Exception as e:
            print(f"Error generating queries for file {file}: {e}")

# Generate Cypher queries for node creation based on a given table, node_label, and properties to columns mapping
def create_cypher_query_nodes(table, node_label, props_to_columns):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()
    queries = []
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Generate properties string for the Cypher query
        props = ', '.join([f"{prop}: '{row[column]}'" for prop, column in props_to_columns.items()])
        props += f", dataset: '{dataset}'"  # Add the dataset constant value here
        # Create a Cypher query for the current node
        query = f"CREATE (:{node_label} {{{props}}})"
        queries.append(query)
    return queries

# Generate Cypher queries for Target nodes
def create_cypher_query_targets(table):
       return create_cypher_query_nodes(table, 'Target', {
        'name': 'approvedName',
        'ensembleId': 'id',
        'symbol': 'approvedSymbol'
    })

# Generate Cypher queries for AdverseEvent nodes
def create_cypher_query_adverse_events(table):
    return create_cypher_query_nodes(table, 'AdverseEvent', {
        'meddraId': 'meddraCode',
        'adverseEventId': 'event'
    })

# Generate Cypher queries for Drug nodes
def create_cypher_query_drugs(table):
    return create_cypher_query_nodes(table, 'Drug', {
        'drugId': 'name',
        'chemblId': 'id'
    })

# Generate Cypher queries for MousePhenotype nodes
def create_cypher_query_mouse_phenotypes(table):
    return create_cypher_query_nodes(table, 'MousePhenotype', {
        'mousePhenotypeLabel': 'modelPhenotypeLabel',
        'mousePhenotypeId': 'modelPhenotypeId'
    })

# Generate Cypher queries for Disease nodes
def create_cypher_query_diseases(table):
    return create_cypher_query_nodes(table, 'Disease', {
        'name': 'name',
        'diseaseId': 'id'
    })

# <TODO> Add function to handle generation of Cypher queries for edge creation similar to how nodes are handled

# Parse the mechanism of action data and create a list of Cypher queries to insert the data into the database
def create_cypher_query_mechanism_of_action(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()
    queries = []
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        if row['chemblIds'] is None or row['targets'] is None:
            continue
        for chemblId in row['chemblIds']:
            for target in row['targets']:
                # Generate a Cypher query for the current mechanism of action relationship
                query = f"MATCH (from:Drug), (to:Target)\nWHERE from.chemblId='{chemblId}'\nAND to.ensembleId='{target}'\nCREATE (from)-[:TARGETS {{dataset: '{dataset}'}}]->(to)"
                queries.append(query)
    return queries

# Parse the targets data and create a list of Cypher queries to add participates relationships to the database
def create_cypher_query_participates(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()
    queries = []
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # If either 'id' or 'pathways' fields are missing, skip this row
        if row['id'] is None or row['pathways'] is None:
            continue
        # Iterate over each pathway in the 'pathways' field of the row
        for pathway in row['pathways']:
            # Generate a Cypher query for the current Target-Pathway relationship
            query = f"MATCH (from:Target), (to:Pathway)\nWHERE from.ensembleId='{row['id']}'\nAND to.pathwayId='{pathway['pathwayId']}'\nCREATE (from)-[:PARTICIPATES_IN {{dataset: '{dataset}', pathwayCode: '{pathway['pathway']}', pathwayId: '{pathway['pathwayId']}', topLevelTerm: '{pathway['topLevelTerm']}'}}]->(to)"
            # Add the generated query to the list of queries
            queries.append(query)
    # Return the list of generated queries
    return queries

# Parse the targets data and create a list of Cypher queries to add associatedWith relationships to the database
def create_cypher_query_associated_with(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()
    queries = []
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # If either 'id' or 'pathways' fields are missing, skip this row
        if row['chembl_id'] is None or row['meddraCode'] is None:
            continue
        # Generate a Cypher query for the current Target-Pathway relationship
        query = f"MATCH (from:Drug), (to:AdverseEvent)\nWHERE from.chemblId='{row['chembl_id']}'\nAND to.meddraId='{row['meddraCode']}'\nCREATE (from)-[:ASSOCIATED_WITH {{dataset: '{dataset}', critval: '{row['critval']}', llr: '{row['llr']}'}}]->(to)"
        # Add the generated query to the list of queries
        queries.append(query)
    # Return the list of generated queries
    return queries

# Main function call
if __name__ == "__main__":
    main()

