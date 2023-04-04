# Parse the parquet files extracting the data, saving it to a json file on the local machine.

import os
import pyarrow.parquet as pq
import neo4j


def main():
    # use the opentarget directory for the input files
    current_dir = os.getcwd()
    input_dir = f"{current_dir}/opentarget"

    # each data type is in a different directory
    for data_type in os.listdir(input_dir):
        # get the path to the directory
        data_type_path = os.path.join(input_dir, data_type)
        # check if the data_type_path is a directory
        if not os.path.isdir(data_type_path):
            continue
        # create the list of files in the directory, filter out non-parquet files
        files = [file for file in os.listdir(data_type_path) if file.endswith(".parquet")]
        # each file in the directory is a parquet file
        for n, file in enumerate(files):
            # only run on parquet files
            if not file.endswith(".parquet"):
                continue
            # get the path to the file
            file_path = os.path.join(data_type_path, file)
            # read the file
            table = pq.read_table(file_path)
            # print the current folder and file and enumerate of files in the folder
            print(f"{data_type} {n+1} of {len(files)}")
            # print the first 5 rows of the file
            # Sprint(table.to_pandas().head())

            # parse the file and create a neo4j cypher query to insert the data into the database
            # each type will have a different parsing function
            # for example, the disease file will have a different parsing function than the gene file
            # the parsing function will return a list of cypher queries
            # the list of cypher queries will be executed to insert the data into the database

            # this if statement is for testing while more cypher functions are being created
            if(data_type == "targets"):
                # dictionary to choose the correct function foq the data type
                cypher_generator_functions = {
                    "targets": create_cypher_query_targets
                }
                # get the function from switcher dictionary
                func = cypher_generator_functions.get(data_type, lambda: "Invalid data type")
                # execute the function
                queries = func(table)
                # execute the queries
                for query in queries:
                    print(query)
                    # execute the query

# parse a target file and create a cypher query to insert the data into the database
# This is from the query constructor for targets in gradvek 1.0
""" ("CREATE (:Target" 
    + " {" + "name:\'" + StringEscapeUtils.escapeEcmaScript (super.toString ()) + "\', "
    + TARGET_ID_STRING + ":\'" + StringEscapeUtils.escapeEcmaScript (mEnsembleId) + "\', "
    + dataset: StringEscapeUtils.escapeEcmaScript (mFromDatase) + ", "
    + "symbol:\'" + StringEscapeUtils.escapeEcmaScript (mSymbol) + "\'"
    + "})"); """
def create_cypher_query_targets(table):
    # get the data from the table
    df = table.to_pandas()
    # create a list to store the cypher queries
    queries = []
    # iterate over the rows in the table
    for _, row in df.iterrows():
        # print(row)
        # create a cypher query
        query = f"CREATE (:Target {{name: '{row['approvedName']}', ensembleId: '{row['id']}', dataset: 'targert_23.04', symbol: '{row['approvedSymbol']}'}})"
        # add the cypher query to the list of queries
        queries.append(query)
    # return the list of cypher queries
    return queries


if __name__ == "__main__":
    main()