import os
import time
import pyarrow.parquet as pq
from neomodel import config, db
from neo4j import GraphDatabase
from graphdatascience import GraphDataScience

"""
Open Targets Neo4j Importer

This script imports Open Targets data into a Neo4j database. It processes various types of data, including targets,
pathways, FDA adverse events, molecules, mechanisms of action, mouse phenotypes, diseases, interactions, and
baseline expressions, and imports them as nodes and edges into the database.

How this file uses the data retrieved by the 'get_datasets.py' file:

1. The script reads data from parquet files stored in the 'opentarget' folder. Parquet files are a columnar storage file
   format optimized for use with big data processing frameworks. Each data type is stored in its own subfolder.

2. The data in the parquet files is converted to tables using the PyArrow library. These tables are then converted
   to pandas DataFrames for easier manipulation.

3. The script processes the data using node and edge query generator functions defined for each data type. These
   generator functions take the DataFrames as input, extract the required properties, and create Cypher queries to
   create or update nodes and edges in the Neo4j database.

4. The script uses the APOC library for parallelized batch processing of Neo4j Cypher queries. Make sure to have the
   APOC plugin installed in your Neo4j instance before running the script.

Main function overview:

- The script first sets the dataset name and checks if the data files are up-to-date.
- It then defines a dictionary called 'data_type_query_generators', which maps data types to lists of node and edge
  query generator functions.
- It creates indexes for nodes to improve query performance.
- The script iterates over each data type for the node query generators, and then does the same for edge query
  generators, executing them in two separate loops to ensure all node generators are run before the edge generators.

Adding a new data type to the 'data_type_query_generators' dictionary:

1. Define the node and edge query generator functions for the new data type.
2. Add the data type name as the key and a tuple containing the node and edge query generator functions as the value.

Creating query generator functions (for nodes and relationships):

1. Define a function that takes a 'table' as its argument. This table is obtained by converting a parquet file to a
   table using PyArrow (handled in main you don't need to define this) and then the function converts that table to a pandas DataFrame.
2. Extract the required properties from the DataFrame and prepare the data for the Cypher query.
3. Create an APOC query for creating or merging nodes or relationships in batch, using the prepared data.
4. Return a list of queries to be executed, including the dataset creation query and the node/relationship creation query.

As long at the function is defined and added to the 'data_type_query_generators' dictionary, the script will run it.

"""



def ensure_neo4j_connection():
    NEO4J_BOLT_URL = os.getenv('NEO4J_DOCKER_URL', 'bolt://neo4j:gradvek1@localhost:7687')
    config.DATABASE_URL = NEO4J_BOLT_URL

    def establish_neo4j_connection():
        db.set_connection(NEO4J_BOLT_URL)

    def check_neo4j_connection():
        try:
            query = "MATCH (n) RETURN COUNT(n) AS node_count"
            results, meta = db.cypher_query(query)

            # Check if the query was successful
            if results is not None:
                return True
            else:
                return False
        except Exception as e:
            # print(f"Neo4j connection error: {e}")
            return False
    
    if not check_neo4j_connection():
        establish_neo4j_connection()


# Dataset name
data_version = None

def set_dataset_name():
    global data_version

    # Get the current script's directory instead of the working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the platform.conf file
    conf_file = os.path.join(current_dir, "platform.conf")

    with open(conf_file, "r") as file:
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
    try:
        # Query the first entry in Neo4j
        results, _ = db.cypher_query("MATCH (n) RETURN n LIMIT 1")
        
        # Check if there is any result
        if results and len(results) > 0:
            # Get the dataset from the first entry if it exists
            node = results[0][0]
            dataset = node.get('dataset', None)
            
            if dataset is not None:
                # Get the dataset version from that entry
                first_7_digits = dataset[:7]
                print("Neo4J Dataset version:", first_7_digits)

                # If the dataset version from the entry in neo4j matches that from our conf file, there's no need to update the neo4j db
                if first_7_digits == data_version:
                    return False
                else:
                    print("Data version in neo4j doesnt match the data version in conf file. Clearing neo4j db and reloading db")
                    return True
            else:
                # Node does not have a dataset property
                print("Node does not have a dataset property")
                return True
        else:
            # No nodes found in neo4j
            print("No nodes found in neo4j. Reloading data")
            return True
        
    except Exception as e:
        # Error occurred while querying neo4j
        print("Error occurred while querying neo4j: {}".format(str(e)))
        print("Reloading data")
        return True


def parse_datasets():
    # Check and set the neo4j connection
    ensure_neo4j_connection()
    # Set the dataset name
    set_dataset_name()
    # Get the current script's directory instead of the working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the input directory for the opentarget data
    input_dir = os.path.join(current_dir, "opentarget")

    #Check if data files are updated via platform.conf file data version. If so, clear the neo4j db and reload data from files
    if update_check(): # change this to 'if True:' when doing dev work
        # clear_neo4j_database()

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
            "baseExpressions":([create_cypher_query_baseline_expression],[create_cypher_query_hgene, create_cypher_query_hprotein]),
            "pathways":([create_cypher_query_pathway_types],[create_cypher_query_pathways_relation]),
            # "gwasTraitProfile":([create_cypher_query_gwas],[create_cypher_query_gwas_relation])
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

    for n, file in enumerate(files):
        print(f"Processing {query_generator.__name__} file {n+1}/{len(files)}")
        file_path = os.path.join(data_type_path, file)
        try:
            table = pq.read_table(file_path)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            continue

        # Generate queries for the current table
        queries = query_generator(table)

        # Execute the queries concurrently within a single transaction
        with db.transaction:
            for query, params in queries:
                db.cypher_query(query, params=params)


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

# From legacy code -- not sure function or data that corresponds to this
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

# Generate Cypher queries for Disease nodes
def create_cypher_query_pathway_types(table):
    df = table.to_pandas()
    node_label = 'TargetPathway'

    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = []
    for _, row in df.iterrows():
        if row['pathways'] is None:
            continue
        for pathway in row['pathways']:
            data.append({
                'id': pathway['id'],
                'name': pathway['name']
            })

    # APOC query for creating Evidence nodes in batch
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:TargetPathway {id: prop.id, name: prop.name, dataset: $dataset})',
        {params: {props: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

# Generate Cypher queries for GWAS nodes
def create_cypher_query_gwas(table):
    df = table.to_pandas()
    # large data volume, filter to speed it up
    df = df['trait_efos'].explode('trait_efos').drop_duplicates()

    node_label = 'Gwas'
    dataset = f"{data_version} {node_label}"
    # Prepare data for the Cypher query
    data = [{'id': x} for x in df]

    # APOC query for creating Evidence nodes in batch
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $props as prop RETURN prop',
        'MERGE (:Gwas {id: prop.id, dataset: $dataset})',
        {params: {props: $data, dataset: $dataset}, batchSize: 1000, parallel: true}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]


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
    db.cypher_query("CREATE INDEX chemblId_index IF NOT EXISTS FOR (d:Drug) ON (d.chemblId)")
    db.cypher_query("CREATE INDEX ensembleId_index IF NOT EXISTS FOR (t:Target) ON (t.ensembleId)")
    db.cypher_query("CREATE INDEX pathwayId_index IF NOT EXISTS FOR (p:Pathway) ON (p.pathwayId)")
    db.cypher_query("CREATE INDEX meddraId_index IF NOT EXISTS FOR (a:AdverseEvent) ON (a.meddraId)")
    db.cypher_query("CREATE INDEX mousePhenotypeId_index IF NOT EXISTS FOR (a:MousePhenotype) ON (a.mousePhenotypeId)")
    db.cypher_query("CREATE INDEX diseaseId_index IF NOT EXISTS FOR (a:Disease) ON (a.diseaseId)")
    db.cypher_query("CREATE INDEX dataset_index IF NOT EXISTS FOR (a:Dataset) ON (a.dataset)")
    db.cypher_query("CREATE INDEX baseline_expression_index IF NOT EXISTS FOR (a:Baseline_Expression) ON (a.efo_code)")
    db.cypher_query("CREATE INDEX targetpathway_index IF NOT EXISTS FOR (a:TargetPathway) ON (a.id)")
    db.cypher_query("CREATE INDEX gwas_index IF NOT EXISTS FOR (a:Gwas) ON (a.id)")



# Parse the Gwas data and create a list of Cypher queries to insert the data into the database
def create_cypher_query_gwas_relation(table):
    df = table.to_pandas()
    df = df[['gene_id','trait_efos']].explode('trait_efos').drop_duplicates()
    node_label = 'GwasRelation'
    dataset = f"{data_version} {node_label}"
    data = []
    for _, row in df.iterrows():
        data.append({
            'gwas': row['trait_efos'],
            'ensembleId': row['gene_id'],
        })
    # APOC query for merging relationships between Drug and Target nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Target {ensembleId: item.ensembleId}), (to:Gwas {id: item.gwas})
         MERGE (from)-[:GWAS_RELATION {dataset: $dataset}]->(to)',
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
    )
    """
    # Include the dataset creation query
    dataset_query = create_dataset_cypher_query(node_label)
    # Return a list of queries to be executed
    return [(dataset_query, {}), (query, {'data': data, 'dataset': dataset})]

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
    # Delete all nodes and relationships in the database
    db.cypher_query("MATCH (n) DETACH DELETE n")

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
        {params: {data: $data, dataset: $dataset}, batchSize: 1000, parallel: false}
    )
    """
    return [(query, {'data': data, 'dataset': dataset})]

def create_cypher_query_pathways_relation(table):
    df = table.to_pandas()
    node_label = 'Pathways'
    dataset = f"{data_version} {node_label}"
    data = []
    for _, row in df.iterrows():
        if row['targetId'] is None or row['pathways'] is None:
            continue
        # Append data for each combination of chembl_id and meddraCode
        for j in row['pathways']:
            data.append({
                'targetId': row['targetId'],
                'pathway': j['id'],
                'weight': 1
        })
    # APOC query for creating relationships between Target and Pathway nodes
    query = """
    CALL apoc.periodic.iterate(
        'UNWIND $data as item RETURN item',
        'MATCH (from:Target {ensembleId: item.targetId}), (to:TargetPathway {id: item.pathway})
         MERGE (from)-[:PATHWAY {dataset: $dataset, weight: item.weight}]->(to)',
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
    parse_datasets()

