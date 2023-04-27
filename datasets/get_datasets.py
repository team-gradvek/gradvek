import math
from bs4 import BeautifulSoup
import requests
import os
import time
from urllib.parse import urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
This script downloads Open Target datasets from the Open Target FTP server.
The datasets include information about diseases, FDA significant adverse drug reactions,
mechanism of action, molecules, mouse phenotypes, and targets.

Steps to add a new data type:

1. Add a new key-value pair to the 'paths' dictionary.
The key is the name of the new data type and the value is a list containing the local directory path and the Open Target FTP server path.
2. Ensure the URL and local directory are correct and have the appropriate read and write permissions.

The script downloads files in parallel to try and speed up the process, particularly when there are retries.
The ThreadPoolExecutor class from the concurrent.futures module is used to manage threads for parallel downloads.
The 'max_workers' parameter determines the maximum number of threads used concurrently.

The script has a retry mechanism, enabling it to retry a download if it fails.
The 'max_retries' parameter determines the maximum number of retries allowed for each download.
The 'delay' parameter specifies the time (in seconds) to wait before attempting the next retry.

The 'paths' dictionary stores the local directory paths and corresponding Open Target FTP server paths for each dataset.
"""

# Define a dictionary containing the project paths and Open Target paths for different data types
paths = {
    # Key: data type name, Value: [local directory path, Open Target URL path]
    "diseases": ["opentarget/diseases", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/diseases/"],
    "fda": ["opentarget/fda", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/fda/significantAdverseDrugReactions/"],
    "mechanismOfAction": ["opentarget/mechanismOfAction", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/mechanismOfAction/"],
    "molecules": ["opentarget/molecule", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/molecule/"],
    "mousePhenotypes": ["opentarget/mousePhenotypes", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/mousePhenotypes/"],
    "targets": ["opentarget/targets","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/targets/"],
    "interactions": ["opentarget/interactions","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/interaction/"],
    "baseExpressions": ["opentarget/baseExpressions","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/baselineExpression/"],
    # "gwasTraitProfile": ["opentarget/gwasTraitProfile","https://ftp.ebi.ac.uk/pub/databases/opentargets/genetics/latest/d2v2g/"]
}

def main():
    # Print the initial message when the program starts
    print("Starting the program...")

    # Create necessary directories for storing data
    create_required_directories()

    try:
        # Get the current data version from the existing platform.conf file
        current_data_date = get_open_targets_version_from_file("platform.conf")
        print(f"Current data version: {current_data_date}")

        # Download the latest platform.conf file
        download_latest_conf_file()
        # Get the latest data version from the downloaded newplatform.conf file
        latest_data_date = get_open_targets_version_from_file("newplatform.conf")
        print(f"Latest data version: {latest_data_date}")

        # If the latest data is newer than the current data, or the current data version is unknown, update the data
        if current_data_date is None or latest_data_date > current_data_date:
            print("Files being updated")

            # Delete existing parquet files before downloading new ones
            delete_existing_file()

            # Download new data for each data type sequentially using a requests.Session
            with requests.Session() as session:
                for key, values in paths.items():
                    get_datasets(session, key, values[0], values[1])

        # If the current open targets files are already up to date, validate the existing files
        else:
            # Remove the newplatform.conf file, as it is not needed
            if os.path.exists('newplatform.conf'):
                os.remove('newplatform.conf')
            print("Files are already up to date")

            # Validate the existing files using a requests.Session
            with requests.Session() as session:
                for key, values in paths.items():
                    get_datasets(session, key, values[0], values[1])

    # Handle any exceptions that occur while validating and updating data
    except Exception as e:
        print("Couldn't validate latest open targets version and update data." + str(e))


def download_chunk(session, link, start, end, retries=3, delay=5, progress_callback=None):
    # Set headers for the range of bytes to be downloaded. This allows downloading a specific part of the file
    headers = {"Range": f"bytes={start}-{end}"}

    # Attempt to download the chunk 'retries' number of times. This provides a retry mechanism for failed downloads
    for _ in range(retries):
        try:
            # Send a GET request to download the specified range of bytes from the file. The 'stream=True' argument allows for handling large files
            response = session.get(link, headers=headers, stream=True)

            # Extract the downloaded chunk from the response. This is the actual data of the requested byte range
            chunk = response.content

            # If a progress_callback function is provided, call it with the length of the downloaded chunk. This allows for updating the download progress
            if progress_callback:
                progress_callback(len(chunk))

            # Return the downloaded chunk and its starting position. These will be used later to merge the chunks into the complete file
            return chunk, start

        # If an exception occurs, wait for 'delay' seconds before retrying. This can help with temporary network issues or server overload
        except Exception as e:
            time.sleep(delay)

    # If all retries fail, return None for the chunk and its starting position. This signifies that the download was unsuccessful
    return None, start

def download_file(session, link, output_file, max_retries=3, delay=5, max_threads_per_file=1):
    try:
        # Send a HEAD request to get the file size from the response headers
        response = session.head(link)
        file_size = int(response.headers['Content-Length'])

        # Calculate the chunk size based on the file size and the number of threads per file
        chunk_size = file_size // max_threads_per_file

        # Create a list of tasks, each containing the required arguments for downloading a chunk
        tasks = [(session, link, i * chunk_size, min((i + 1) * chunk_size - 1, file_size - 1), max_retries, delay) for i in range(max_threads_per_file)]

        # Open the output file in binary write mode, and set its size to the expected file size
        with open(output_file, "wb") as f:
            f.seek(file_size - 1)
            f.write(b'\0')

        # Initialize a list to store the progress of each thread
        progress = [0] * max_threads_per_file

        # Define a callback function to update progress and print the download percentage
        def progress_callback(chunk_size, index):
            progress[index] += chunk_size
            completed = sum(progress)
            percentage = (completed / file_size) * 100
            print(f"\rDownloading {os.path.basename(link)}: {percentage:.2f}%", end="")

        # Create a ThreadPoolExecutor and download each chunk in parallel using the executor
        with ThreadPoolExecutor(max_workers=max_threads_per_file) as executor:
            results = list(executor.map(lambda i, task: download_chunk(*task, progress_callback=lambda chunk_size: progress_callback(chunk_size, i)), range(max_threads_per_file), tasks))

        # If all chunks are downloaded successfully, write them to the output file. This merges the downloaded chunks into the complete file
        if all(result[0] is not None for result in results):
            with open(output_file, "rb+") as f:
                for content, start in results:
                    f.seek(start)
                    f.write(content)
            print()  # Add a newline to separate progress from the next print statement
            return True

        # If any chunk download fails, delete the output file and return False. This signifies that the download was unsuccessful and the file should not be kept
        else:
            os.remove(output_file)
            return False

    # If an exception occurs, print an error message and return False. This signifies that the download was unsuccessful due to an error
    except Exception as e:
        print(f"Failed to download {link} due to error: {e}")
        return False



def calculate_optimal_workers_and_threads(total_files, max_cores, max_workers):
    # Calculate the optimal number of workers, considering the total number of files, CPU cores, and max workers
    workers = min([max_cores, max_workers, total_files])
    
    # Calculate the optimal number of threads per worker based on the available CPU cores and the number of workers
    threads = math.ceil(max_cores / workers)
    
    return workers, threads

def get_datasets(session, name, project_path, ot_path, max_retries=3, delay=5):
    try:
        print(f"Starting to download {name} files...")

        # Set URL, current directory, and output directory for downloading files
        url = ot_path
        current_dir = os.getcwd()
        output_dir = f"{current_dir}/{project_path}"

        # Create the output directory if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Fetch the target URL's content and parse it using BeautifulSoup
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        # Extract the download links for .parquet files from the parsed content
        links = [url + link.get("href") for link in soup.find_all("a") if link.get("href").endswith(".parquet")]

        # Calculate the maximum number of CPU cores, workers, and threads per file
        max_cores = os.cpu_count()
        max_total_workers = 8  # Adjust this to control the maximum number of files to download at once
        max_workers, max_threads_per_file = calculate_optimal_workers_and_threads(len(links), max_cores, max_total_workers)

        # Initialize a list of tasks to download each file
        tasks = []
        for link in links:
            filename = os.path.basename(link)
            output_file = os.path.join(output_dir, filename)

            # If the file already exists, skip it and print a message
            if os.path.exists(output_file):
                print(f"File {filename} already exists. Skipping...")
            else:
                tasks.append((link, output_file, max_retries, delay, max_threads_per_file))

        # Print information about the number of workers and threads being used
        completed_files = 0
        total_files = len(tasks)
        print(f"Using {max_workers} workers and {max_threads_per_file} threads per file")

        # Use a ThreadPoolExecutor to download files concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(download_file, session, *task): task for task in tasks}

            # Iterate through completed download tasks and print their status
            for future in as_completed(futures):
                task = futures[future]
                link, output_file, _, _, _ = task
                success = future.result()
                completed_files += 1
                filename = os.path.basename(link)

                if success:
                    print(f"[{completed_files}/{total_files}] Downloaded {name} {filename}")
                else:
                    print(f"[{completed_files}/{total_files}] Failed to download {name} {filename} after {max_retries} retries.")

        print("Files downloaded successfully!")

    except Exception as e:
        print("Downloading files error: " + str(e))



def get_open_targets_version_from_file(file_name):
    try:
        cwd = os.getcwd()
        
        # Construct the path to the platform.conf file
        conf_file = os.path.join(cwd, file_name)
        
        # Read the contents of the file
        with open(conf_file, 'r') as f:
            contents = f.read()
        
        # Find the data_version line and extract the value
        data_version = None
        for line in contents.split('\n'):
            if line.startswith('data_version'):
                data_version = line.split('=')[1].strip()
                if data_version.startswith('"') and data_version.endswith('"'):
                    data_version = data_version[1:-1]
                break
        
        # Print the data_version value
        if data_version:
            return datetime.strptime(data_version, '%y.%m.%d').date()
        else:
            return datetime.strptime('21.01.01', '%y.%m.%d').date()
    except Exception as e:
        return datetime.strptime('21.01.01', '%y.%m.%d').date()



def download_latest_conf_file():
    try:
        # Specify the URL
        url = 'https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/conf/'

        # Use the current directory as the output directory
        output_dir = os.getcwd()

        # Use requests to retrieve the HTML content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the link to the file on the page
        link = ''
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.endswith('.conf'):
                link = url + href
                break

        # Download the file
        filename = os.path.basename(link)
        output_file = os.path.join(output_dir, "new" + filename)
        response = requests.get(link)
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"File {output_file} -- saved!")

    except Exception as e:
        print("Downloading file error: " + str(e))

def delete_existing_file():
    # Check if the platform.conf file exists
    if os.path.exists('platform.conf'):
        os.remove('platform.conf')
    
    # Rename the newplatform.conf file to platform.conf
    os.rename('newplatform.conf', 'platform.conf')
    print("Successfully updated platform.conf file.")

    current_dir = os.getcwd()

    for key, values in paths.items():
        delete_files_dir = f"{current_dir}/{values[0]}"
        for filename in os.listdir(delete_files_dir):
            try:
                file_path = os.path.join(delete_files_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print("Deleted" + filename)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def create_required_directories():
    current_dir = os.getcwd()
    # Iterate through the paths and create required directories if they don't exist
    for key, values in paths.items():
        dir_path = os.path.join(current_dir, values[0])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

if __name__ == "__main__":
    main()
