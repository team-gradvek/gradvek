import os
import pyarrow.parquet as pq
from neo4j import GraphDatabase

"""
Open Targets Neo4j Importer

This script imports Open Targets data into a Neo4j database. It processes various types of data, including targets,
FDA adverse events, molecules, mechanisms of action, mouse phenotypes, and diseases, and imports them as nodes and
edges into the database.

The script is designed to read parquet data from the 'opentarget' folder, where each data type should be stored in its own
subfolder. To add a new data type, create a subfolder with the appropriate name and add the necessary node and edge
query generators to the 'data_type_query_generators' dictionary.

Neo4j queries are generated and executed for each data type. Nodes are first imported into the database, followed by the
edges. Queries use the APOC library for parallelized batch processing, which significantly improves performance.

How the script works:

1. Iterates over each data type in the input directory for node query generators
2. Creates indexes for nodes to improve performance in edge query generation
3. Iterates over each data type in the input directory for edge query generators

To update the script for new data types:

1. Create a folder for the new data type in the 'opentarget' folder - the folder name will be the data type name
2. Add the data type name to the 'data_type_query_generators' dictionary - the key will be the data type name and the
value will be a tuple containing the node query generator and edge query generator for that data type
3. Add 'create_cypher_query_<data_type_name>' functions for the node and edge query generators as needed for the new type

Important note: This script uses the APOC library for parallelized batch processing of Neo4j queries. Make sure to have
the APOC plugin installed in your Neo4j instance before running the script.
"""

# Set dataset name
# TODO use config file to set this and append data type to this when generating queries
dataset = "opentarget 23.02"

# Set the URI and AUTH for the neo4j database
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "gradvek1")

def main():
    # Get the current working directory
    current_dir = os.getcwd()
    # Set the input directory for the opentarget data
    input_dir = f"{current_dir}/opentarget"

    # TODO:
    # Action (edge) - appears to not use any data source?
    # Gene (entity), Involves (edge) - these seem to only come from csv

    # Define data_type_query_generators, a dictionary that maps data types to lists of query generators.
    # Each list contains multiple node or edge query generator functions for the respective data type.
    data_type_query_generators = {
        # Key: data type name, Value: tuple([node query generators], [edge query generators])
        "targets": ([create_cypher_query_targets, create_cypher_query_pathways], [create_cypher_query_participates]),
        "fda": ([create_cypher_query_adverse_events], [create_cypher_query_associated_with]),
        "molecule": ([create_cypher_query_drugs], []),
        "mechanismOfAction": ([], [create_cypher_query_mechanism_of_action]),
        "mousePhenotypes": ([create_cypher_query_mouse_phenotypes], []),
        "diseases": ([create_cypher_query_diseases], [])
    }


    # Create indexes for nodes - this significantly improves performance in edge query generation
    create_indexes()

    # Iterate over each data type in the input directory for node query generators
    for data_type in os.listdir(input_dir):
        # Set the data_type_path
        data_type_path = os.path.join(input_dir, data_type)
        # Check if the path is a directory
        if not os.path.isdir(data_type_path):
            continue

         # Run the node query generators for the current data type
        for node_query_generator in data_type_query_generators[data_type][0]:
            if node_query_generator is not None:
                generate_queries(data_type, data_type_path, node_query_generator)
    

    # Iterate over each data type in the input directory for edge query generators
    for data_type in os.listdir(input_dir):
        # Set the data_type_path
        data_type_path = os.path.join(input_dir, data_type)
        # Check if the path is a directory
        if not os.path.isdir(data_type_path):
            continue

        # Run the edge query generators for the current data type
        for edge_query_generator in data_type_query_generators[data_type][1]:
            if edge_query_generator is not None:
                generate_queries(data_type, data_type_path, edge_query_generator)

# Generate queries for the given data type and path
# This function takes a data_type, data_type_path, and a query_generator function
# It iterates through all parquet files in the given path and applies the query_generator function to generate
# Cypher queries for each file.
def generate_queries(data_type, data_type_path, query_generator):
    if query_generator is None:
        return

    # List all parquet files in the data_type_path
    files = [file for file in os.listdir(data_type_path) if file.endswith(".parquet")]

    # Connect to the neo4j database
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

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

                # Create a function to execute multiple queries within a single transaction
                def execute_queries(tx, queries):
                    for query, params in queries:
                        tx.run(query, params)

                # Execute the queries concurrently within a single transaction
                with driver.session() as session:
                    session.execute_write(execute_queries, queries)

            except Exception as e:
                print(f"Error generating queries for file {file}: {e}")


# Generate Cypher queries for node creation based on a given table, node_label, and properties to columns mapping
def create_cypher_query_nodes(table, node_label, props_to_columns):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        data.append({column: row[column] for _, column in props_to_columns.items()})

    # APOC query for creating or merging nodes in batch
    query = f"""
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:{node_label} {{{', '.join([f"{prop}: prop.{column}" for prop, column in props_to_columns.items()])}, dataset: $dataset}})',
        {{params: {{props: $data, dataset: $dataset}}, batchSize: 1000, parallel: true}}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

# Generate Cypher queries for Target nodes
def create_cypher_query_targets(table):
    return create_cypher_query_nodes(table, 'Target', {
        'name': 'approvedName',
        'ensembleId': 'id',
        'symbol': 'approvedSymbol'
    })

def create_cypher_query_pathways(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        if row['pathways'] is None:
            continue
        for pathway in row['pathways']:
            data.append({
                'pathwayCode': pathway['pathway'],
                'pathwayId': pathway['pathwayId'],
                'topLevelTerm': pathway['topLevelTerm']
            })

    # APOC query for creating Pathway nodes in batch
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:Pathway {pathwayCode: prop.pathwayCode, pathwayId: prop.pathwayId, topLevelTerm: prop.topLevelTerm, dataset: $dataset})',
        {params: {props: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

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


# Create indexes in the database for the nodes before running edge queries
def create_indexes():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        with driver.session() as session:
            session.run("CREATE INDEX chemblId_index IF NOT EXISTS FOR (d:Drug) ON (d.chemblId)")
            session.run("CREATE INDEX ensembleId_index IF NOT EXISTS FOR (t:Target) ON (t.ensembleId)")
            session.run("CREATE INDEX pathwayId_index IF NOT EXISTS FOR (p:Pathway) ON (p.pathwayId)")
            session.run("CREATE INDEX meddraId_index IF NOT EXISTS FOR (a:AdverseEvent) ON (a.meddraId)")
            session.run("CREATE INDEX mousePhenotypeId_index IF NOT EXISTS FOR (a:MousePhenotype) ON (a.mousePhenotypeId)")
            session.run("CREATE INDEX diseaseId_index IF NOT EXISTS FOR (a:Disease) ON (a.diseaseId)")


# TODO Add function to handle generation of Cypher queries for edge creation similar to how nodes are handled

# Parse the mechanism of action data and create a list of Cypher queries to insert the data into the database
def create_cypher_query_mechanism_of_action(table):
    df = table.to_pandas()
    data = []
    for _, row in df.iterrows():
        if row['chemblIds'] is None or row['targets'] is None:
            continue
        for chemblId in row['chemblIds']:
            for target in row['targets']:
                 # Append data for each combination of chemblId and target
                 data.append({
                    'chemblId': chemblId,
                    'ensembleId': target,
                    'actionType': row['actionType']
                })
    # APOC query for merging relationships between Drug and Target nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Drug {chemblId: item.chemblId}), (to:Target {ensembleId: item.ensembleId})
         MERGE (from)-[:TARGETS {dataset: $dataset, actionType: item.actionType}]->(to)',
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

# Parse the targets data and create a list of Cypher queries to add participates relationships to the database
def create_cypher_query_participates(table):
    df = table.to_pandas()
    data = []
    for _, row in df.iterrows():
        if row['id'] is None or row['pathways'] is None:
            continue
        for pathway in row['pathways']:
            # Append data for each combination of target and pathway
            data.append({
                'ensembleId': row['id'],
                'pathwayId': pathway['pathwayId'],
                'id': pathway['pathwayId']
            })
    # APOC query for creating relationships between Target and Pathway nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Target {ensembleId: item.ensembleId}), (to:Pathway {pathwayId: item.pathwayId})
         MERGE (from)-[:PARTICIPATES_IN {dataset: $dataset, id: item.pathwayId}]->(to)',
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

# Parse the targets data and create a list of Cypher queries to add associatedWith relationships to the database
def create_cypher_query_associated_with(table):
    df = table.to_pandas()
    data = []
    for _, row in df.iterrows():
        if row['chembl_id'] is None or row['meddraCode'] is None:
            continue
        # Append data for each combination of chembl_id and meddraCode
        data.append({
            'chembl_id': row['chembl_id'],
            'meddraCode': row['meddraCode'],
            'critval': row['critval'],
            'llr': row['llr']
        })
    # APOC query for creating relationships between Target and Pathway nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Drug {chemblId: item.chembl_id}), (to:AdverseEvent {meddraId: item.meddraCode})
         MERGE (from)-[:ASSOCIATED_WITH {dataset: $dataset, critval: item.critval, llr: item.llr}]->(to)',
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

# Main function call
if __name__ == "__main__":
    main()

