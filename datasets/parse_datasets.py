import os
import time
import pyarrow.parquet as pq
from neo4j import GraphDatabase
from graphdatascience import GraphDataScience

# Set the URI and AUTH for the neo4j database
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "gradvek1")

# Use Neo4j URI and credentials according to your setup
gds = GraphDataScience(URI, auth=AUTH)

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

# Dataset name
data_version = None

def set_dataset_name():
    global data_version
    with open("platform.conf", "r") as file:
        for line in file:
            # Remove whitespace from the beginning and end of the line
            stripped_line = line.strip()

            # Check if the line starts with "data_version ="
            if stripped_line.startswith("data_version ="):
                # Split the line at the equals sign and take the second part (the value)
                data_version = stripped_line.split("=")[1].strip().replace('"', '')

    # Check if the dataset variable was set
    if data_version is None:
        raise ValueError("data_version not found in platform.conf.")
    else:
        print("Dataset version in platform.conf file:", data_version)

def update_check():
    #Find first entry in neo4j and get the dataset version from it
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            with driver.session() as session:
                result = session.run("MATCH (n) RETURN n LIMIT 1")

                # Check if there is any result
                if result.peek():
                    # Get the dataset from the first entry
                    dataset = result.peek()['n']['dataset']
                    # Get the dataset version from that entry
                    first_7_digits = dataset[:7]
                    print("Neo4J Dataset version:", first_7_digits)

        #close neo4j driver
        driver.close()

        #If the dataset version from the entry in neo4j matches that from our conf file, there's no need to update the neo4j db
        if first_7_digits == data_version:
            print("Data in neo4j is already up to date")
            return False
        else:
            print("Data version in neo4j doesnt match the data version in conf file. Clearing neo4j db and reloading db")
            return True
        
    except Exception as e:
       print("Didnt find neo4j entry or dataset version. Reloading data")
       return True


def main():
    # Set the dataset name
    set_dataset_name()
    # Get the current working directory
    current_dir = os.getcwd()
    # Set the input directory for the opentarget data
    input_dir = f"{current_dir}/opentarget"

    #Check if data files are updated via platform.conf file data version. If so, clear the neo4j db and reload data from files
    if True or update_check(): # change this to 'if True:' when doing dev work
        # clear_neo4j_database()
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
            "mousePhenotypes": ([create_cypher_query_mouse_phenotypes], [create_cypher_query_associated_mouse_phenotypes]),
            "diseases": ([create_cypher_query_diseases], []),
            "interactions":([],[create_cypher_query_interactions]),
            "baseExpressions":([create_cypher_query_baseline_expression],[create_cypher_query_hgene, create_cypher_query_hprotein])
            # "targets": ([], []),
            # "fda": ([], []),
            # "molecule": ([], []),
            # "mechanismOfAction": ([], []),
            # "mousePhenotypes": ([], []),
            # "diseases": ([], []),
            # "interactions":([],[]),
            # "baseExpressions":([],[create_cypher_query_hgene, create_cypher_query_hprotein])
        }


        # Create indexes for nodes - this significantly improves performance in edge query generation
        create_indexes()

        # Iterate over each data type in the input directory for node query generators
        for data_type in os.listdir(input_dir):
            # Check if the data_type is in the data_type_query_generators dictionary
            if data_type not in data_type_query_generators:
                print(f"Ignoring '{data_type}' folder. No matching function found.")
                continue

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
            # Check if the data_type is in the data_type_query_generators dictionary
            if data_type not in data_type_query_generators:
                print(f"Ignoring '{data_type}' folder. No matching function found.")
                continue

            # Set the data_type_path
            data_type_path = os.path.join(input_dir, data_type)
            # Check if the path is a directory
            if not os.path.isdir(data_type_path):
                continue

            # Run the edge query generators for the current data type
            for edge_query_generator in data_type_query_generators[data_type][1]:
                if edge_query_generator is not None:
                    generate_queries(data_type, data_type_path, edge_query_generator)

    else:
        print("Data up to date. Will not update neo4j db")  

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
            print(f"Processing {query_generator.__name__} file {n+1}/{len(files)}")
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

                # Execute the queries concurrently within a single transaction, uses the execute_write method if available
                with driver.session() as session:
                    if hasattr(session, 'execute_write'):
                        session.execute_write(execute_queries, queries)
                    else:
                        session.write_transaction(execute_queries, queries)

            except Exception as e:
                print(f"Error generating queries for file {file}: {e}")


# Generate Cypher query for Dataset nodes
def create_dataset_cypher_query(node_label):
    dataset_name = f"{data_version} {node_label}"
    enabled = True
    source = node_label
    timestamp = round(time.time() * 1000)

    query = f"""
    MERGE (d:Dataset {{ dataset: '{dataset_name}' }})
    ON CREATE SET d.enabled = {enabled},
                  d.source = '{source}',
                  d.timestamp = {timestamp}
    RETURN d
    """
    return query



# Generate Cypher queries for node creation based on a given table, node_label, and properties to columns mapping
def create_cypher_query_nodes(table, node_label, props_to_columns):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        entry_data = {column: row[column] for _, column in props_to_columns.items()}
        # Skip the entry if any of the values are null
        if any(value is None for value in entry_data.values()):
            continue
        data.append(entry_data)

    # APOC query for creating or merging nodes in batch
    query = f"""
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:{node_label} {{{', '.join([f"{prop}: prop.{column}" for prop, column in props_to_columns.items()])}, dataset: $dataset}})',
        {{params: {{props: $data, dataset: $dataset}}, batchSize: 1000, parallel: true}}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

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
    node_label = 'Pathway'
    dataset = f"{data_version} {node_label}"
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
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

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


# Generate Cypher queries for hGene nodes
def create_cypher_query_baseline_expression(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    node_label = 'baseline_expression'
    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        for i in row['tissues']:
            data.append({
                'efo_code': i['efo_code'],
                'label': i['label']
            })

    # APOC query for creating Pathway nodes in batch
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:Baseline_Expression {efo_code: prop.efo_code, label: prop.label, dataset: $dataset})',
        {params: {props: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]



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
            session.run("CREATE INDEX dataset_index IF NOT EXISTS FOR (a:Dataset) ON (a.dataset)")
            session.run("CREATE INDEX efo_code_index IF NOT EXISTS FOR (a:Baseline_Expression) ON (a.efo_code)")


# TODO Add function to handle generation of Cypher queries for edge creation similar to how nodes are handled

# Parse the mechanism of action data and create a list of Cypher queries to insert the data into the database
def create_cypher_query_mechanism_of_action(table):
    df = table.to_pandas()
    node_label = 'MechanismOfAction'
    dataset = f"{data_version} {node_label}"
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
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

# Parse the targets data and create a list of Cypher queries to add participates relationships to the database
def create_cypher_query_participates(table):
    df = table.to_pandas()
    node_label = 'Participates'
    dataset = f"{data_version} {node_label}"
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
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

# Parse the targets data and create a list of Cypher queries to add associatedWith relationships to the database
def create_cypher_query_associated_with(table):
    df = table.to_pandas()
    node_label = 'AssociatedWith'
    dataset = f"{data_version} {node_label}"
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
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

def clear_neo4j_database():
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "gradvek1")
    # Connect to Neo4j database
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # Delete all nodes and relationships in the database
        session.run("MATCH (n) DETACH DELETE n")

    # Close the Neo4j driver
    driver.close()

# Parse the mouse phenotypes data and create a list of Cypher queries to add associatedWith relationships to the database
def create_cypher_query_associated_mouse_phenotypes(table):
    df = table.to_pandas()
    node_label = 'mousePhenotypes'
    dataset = f"{data_version} {node_label}"
    data = []
    for _, row in df.iterrows():
        if row['targetFromSourceId'] is None or row['modelPhenotypeId'] is None:
            continue
        # Append data for each combination of chembl_id and meddraCode
        data.append({
            'targetFromSourceId': row['targetFromSourceId'],
            'modelPhenotypeId': row['modelPhenotypeId'],
            'weight': 1
        })
    # APOC query for creating relationships between Target and Pathway nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Target {ensembleId: item.targetFromSourceId}), (to:MousePhenotype {mousePhenotypeId: item.modelPhenotypeId})
         MERGE (from)-[:MOUSE_PHENOTYPE {dataset: $dataset, weight: item.weight}]->(to)',
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

# Parse the molecular interaction data and create a list of Cypher queries
# to add interaction relationships to the database.
def create_cypher_query_interactions(table):
    # Convert the input table to a Pandas DataFrame.
    df = table.to_pandas()

    # Set the node_label and dataset string.
    node_label = 'interactions'
    dataset = f"{data_version} {node_label}"

    # Initialize an empty dictionary to group the data by sourceDatabase.
    data_dict = {}

    # Iterate through the rows of the DataFrame.
    for _, row in df.iterrows():
        # Skip the row if targetB is None or sourceDatabase is 'string'.
        if row['targetB'] is None or row['sourceDatabase'].lower() == 'string':
            continue

        # Group data by sourceDatabase.
        source_database = row['sourceDatabase']
        if source_database not in data_dict:
            data_dict[source_database] = []

        # Append targetA and targetB to the corresponding sourceDatabase list.
        data_dict[source_database].append({
            'targetA': row['targetA'],
            'targetB': row['targetB']
        })

    # Initialize an empty list to store the APOC queries.
    queries = []

    # Iterate through the data_dict items.
    for source_database, data in data_dict.items():
        # Convert the source_database string to uppercase and replace spaces with underscores.
        relationship_type = source_database.upper().replace(" ", "_")

        # Define the Cypher query for creating relationships between Target nodes.
        query = f"""
        CALL apoc.periodic.iterate(
            'UNWIND $data as item RETURN item',
            'MATCH (from:Target {{ensembleId: item.targetA}}), (to:Target {{ensembleId: item.targetB}})
             MERGE (from)-[rel:{relationship_type} {{dataset: $dataset}}]->(to)
             RETURN rel',
            {{params: {{data: $data, dataset: $dataset}}, batchSize: 1000, parallel: false}}
        )
        """
        # Append the query and its parameters to the queries list.
        queries.append((query, {'data': data, 'dataset': dataset}))

    # Return the list of queries.
    return queries

def create_cypher_query_hgene(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    node_label = 'hgene'
    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        for i in row['tissues']:
            if i['rna']['value'] == 0:
                continue
            data.append({
                'ensembleId': row['id'],
                'efo_code': i['efo_code'],
                'rna_value': i['rna']['value']
            })

    # APOC query for creating Pathway nodes in batch
    query = """
        CALL apoc.periodic.iterate(
            'UNWIND $data as item RETURN item',
            'MATCH (from:Target {ensembleId: item.ensembleId}), (to:Baseline_Expression {efo_code: item.efo_code})
            MERGE (from)-[:HGENE {dataset: $dataset, rna_value: item.rna_value}]->(to)',
            {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
        )
        """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

def create_cypher_query_hprotein(table):
    # Convert the table to a pandas DataFrame
    df = table.to_pandas()

    node_label = 'hprotein'
    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        for i in row['tissues']:
            if i['protein']['level'] == -1:
                continue
            data.append({
                'ensembleId': row['id'],
                'efo_code': i['efo_code'],
                'protein_level': i['protein']['level']
            })

    # APOC query for creating Pathway nodes in batch
    query = """
        CALL apoc.periodic.iterate(
            'UNWIND $data as item RETURN item',
            'MATCH (from:Target {ensembleId: item.ensembleId}), (to:Baseline_Expression {efo_code: item.efo_code})
            MERGE (from)-[:HPROTEIN {dataset: $dataset, protein_level: item.protein_level}]->(to)',
            {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
        )
        """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

# Main function call
if __name__ == "__main__":
    main()

