# Parse the parquet files extracting the data, saving it to a json file on the local machine.

import os
import pyarrow.parquet as pq

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
        print(table.to_pandas().head())
