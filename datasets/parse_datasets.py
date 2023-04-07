import os
import pyarrow.parquet as pq
import neo4j

dataset = "opentarget 23.02"

def main():
    # use the opentarget directory for the input files
    current_dir = os.getcwd()
    input_dir = f"{current_dir}/opentarget"

    # iterate over each data type directory
    for data_type in os.listdir(input_dir):
        data_type_path = os.path.join(input_dir, data_type)
        if not os.path.isdir(data_type_path):
            continue

        # get the list of parquet files in the data type directory
        files = [file for file in os.listdir(data_type_path) if file.endswith(".parquet")]

        # iterate over each parquet file in the data type directory
        for n, file in enumerate(files):
            if not file.endswith(".parquet"):
                continue
            file_path = os.path.join(data_type_path, file)

            # read the parquet file as a pyarrow Table
            table = pq.read_table(file_path)

            # print progress and first 5 rows of the file
            print(f"{data_type} {n+1} of {len(files)}")
            #print(table.to_pandas().head())

            # generate cypher queries based on the data type
            # each data type has a different parsing function
            cypher_generator_functions_from_data = {
                "targets": create_cypher_query_targets,
                "fda": create_cypher_query_adverse_events,
                "molecule": create_cypher_query_drugs,
                "mechanismOfAction": create_cypher_query_mechanism_of_action,
                "mousePhenotypes": create_cypher_query_mouse_phenotypes,
                "diseases": create_cypher_query_diseases
            }

            # execute the appropriate parsing function for the data type
            if data_type in cypher_generator_functions_from_data:
                func = cypher_generator_functions_from_data[data_type]
                queries = func(table)
                for query in queries:
                    print(query)
                    # execute the query in Neo4j

    # a second pass is used to create the relationships between the nodes
    # this include creating
    # AssociatedWith relationships using the fda data
    # Participates relationships using the targets data
    # Action relationships that do not require additional data
    # Pathway relationships that do not require additional data


# parse the targets data and create a list of cypher queries to insert the data into the database
def create_cypher_query_targets(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        query = f"CREATE (:Target {{name: '{row['approvedName']}', ensembleId: '{row['id']}', dataset: '{dataset}', symbol: '{row['approvedSymbol']}'}})"
        queries.append(query)
    return queries

# parse the adverse events data and create a list of cypher queries to insert the data into the database
def create_cypher_query_adverse_events(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        query = f"CREATE (:AdverseEvent {{meddraId: '{row['meddraCode']}', dataset: '{dataset}', adverseEventId: '{row['event']}'}})"
        queries.append(query)
    return queries

# parse the drugs data and create a list of cypher queries to insert the data into the database
def create_cypher_query_drugs(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        query = f"CREATE (:Drug {{drugId: '{row['name']}', dataset: '{dataset}', chemblId: '{row['id']}'}})"
        queries.append(query)
    return queries

# parse the mechanism of action data and create a list of cypher queries to insert the data into the database
def create_cypher_query_mechanism_of_action(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        if row['chemblIds'] is None or row['targets'] is None:
            continue
        for chemblId in row['chemblIds']:
            for target in row['targets']:
                query = f"MATCH (from:Drug), (to:Target)\nWHERE from.chemblId='{chemblId}'\nAND to.ensembleId='{target}'\nCREATE (from)-[:TARGETS {{dataset: '{dataset}'}}]->(to)"
                queries.append(query)
    return queries

# parse the mouse phenotypes data and create a list of cypher queries to insert the data into the database
def create_cypher_query_mouse_phenotypes(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        query = f"CREATE (:MousePhenotype {{mousePhenotypeLabel: '{row['modelPhenotypeLabel']}', dataset: '{dataset}', mousePhenotypeId: '{row['modelPhenotypeId']}'}})"
        queries.append(query)
    return queries

# parse the diseases data and create a list of cypher queries to insert the data into the database
def create_cypher_query_diseases(table):
    df = table.to_pandas()
    queries = []
    for _, row in df.iterrows():
        query = f"CREATE (:Disease {{name: '{row['name']}', dataset: '{dataset}', diseaseId: '{row['id']}'}})"
        queries.append(query)
    return queries

if __name__ == "__main__":
    main()
