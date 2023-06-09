import wget
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
    "pathways": ["opentarget/pathways","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/evidence/sourceId=reactome/"],
    #"gwasTraitProfile": ["opentarget/gwasTraitProfile","https://ftp.ebi.ac.uk/pub/databases/opentargets/genetics/latest/d2v2g/"]
}

def get_datasets():
    # Print the initial message when the program starts
    print("Starting the program...")

    # Create necessary directories for storing data
    create_required_directories()

    # Get the current script's directory instead of the working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        # Get the current data version from the existing platform.conf file
        current_data_date = get_open_targets_version_from_file("platform.conf")
        print(f"Current data version: {current_data_date}")

        # Download the latest platform.conf file
        download_latest_conf_file()
        # Get the latest data version from the downloaded newplatform.conf file
        latest_data_date = get_open_targets_version_from_file("newplatform.conf")
        print(f"Latest data version: {latest_data_date}")
        # Get the number of CPU cores available
        core_count = os.cpu_count()
        # If the latest data is newer than the current data, or the current data version is unknown, update the data
        if current_data_date is None or latest_data_date > current_data_date:
            print("Files being updated")
            # Delete existing parquet files before downloading new ones
            delete_existing_file()
            # Download new data
            for key, values in paths.items():
                get_datatype(key, values[0], values[1], max_retries=3, delay=5, max_workers=core_count)

        # If the current open targets files are up to date, validate the existing files
        else:
            # Construct the path to the newplatform.conf file
            new_platform_conf_path = os.path.join(current_dir, 'newplatform.conf')

            if os.path.exists(new_platform_conf_path):
                os.remove(new_platform_conf_path)
            print("Files are already up to date")
            for key, values in paths.items():
                get_datatype(key, values[0], values[1], max_retries=3, delay=5, max_workers=core_count)

    except Exception as e:
        print("Couldn't validate latest open targets version and update data." + str(e))



def download_file(link, output_file, max_retries=3, delay=5):
    # Download the specified file with a retry mechanism
    retries = 0
    while retries < max_retries:
        try:
            wget.download(link, out=output_file)
            return True
        except Exception as e:
            retries += 1
            if retries == max_retries:
                print(f"Failed to download {link} due to error: {e}")
                return False
            else:
                print(f"Retrying {link} after error: {e}")
                time.sleep(delay)


def get_datatype(name, project_path, ot_path, max_retries=3, delay=5, max_workers=5):
    try:
        print(f"Starting to download {name} files...")

        url = ot_path

        # Get the current script's directory instead of the working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_dir, project_path)

         # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Remove any leftover .wget files from previous runs
        for file in os.listdir(output_dir):
            if file.endswith(".wget"):
                os.remove(os.path.join(output_dir, file))

        # Download the HTML file containing the list of files to download
        html_content = wget.download(url, out=output_dir, bar=None)

        # Extract the file links from the HTML file
        links = []
        with open(os.path.join(output_dir, html_content), 'r') as f:
            for line in f:
                if 'href' in line:
                    start = line.find('href="') + 6
                    end = line.find('"', start)
                    link = line[start:end]
                    if link.endswith('.parquet'):
                        links.append(url + link)

       # Prepare the download tasks for each file link
        tasks = []
        existing_files_count = 0
        for n, link in enumerate(links):
            filename = os.path.basename(link)
            output_file = os.path.join(output_dir, filename)
            if os.path.exists(output_file):
                existing_files_count += 1
            else:
                tasks.append((link, output_file, max_retries, delay))

        if existing_files_count == len(links):
            print(f"All {name} files are present. Skipping...")
        elif existing_files_count > 0:
            print(f"{existing_files_count}/{len(links)} {name} files are present. Downloading missing files...")


        # Initialize the count of completed files
        completed_files = 0
        # Calculate the total number of files to download
        total_files = len(tasks)
        # Create a ThreadPoolExecutor to download files in parallel
        # The 'max_workers' parameter determines the maximum number of threads that can be used concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit each download task to the ThreadPoolExecutor
            # A future object represents the result of a computation that may not have completed yet
            # Create a dictionary (futures) that maps each future to its corresponding task (input arguments)
            futures = {executor.submit(download_file, *task): task for task in tasks}
            # The 'as_completed' function returns an iterator that yields futures as they complete
            for future in as_completed(futures):
                # Get the input arguments (task) of the completed future
                task = futures[future]
                # Unpack the task arguments to get the link and output_file
                link, output_file, _, _ = task
                # Get the result (True or False) of the completed future
                success = future.result()
                # Increment the completed files counter
                completed_files += 1
                # Extract the filename from the link
                filename = os.path.basename(link)
                # Print the progress and status based on the success of the download
                if success:
                    print(f"\n[{completed_files}/{total_files}] Downloaded {name} {filename}")
                else:
                    print(f"\n[{completed_files}/{total_files}] Failed to download {name} {filename} after {max_retries} retries.")

        print("Files downloaded successfully!")

    except Exception as e:
        print("Downloading files error: " + str(e))

def get_open_targets_version_from_file(file_name):
    try:
        # Get the current script's directory instead of the working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the path to the platform.conf file
        conf_file = os.path.join(current_dir, file_name)
        
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
                # If data_version is in year.month format, append the first day of the month
                if data_version.count('.') == 1:
                    data_version += ".01"
                break
        print(f"Data version: {data_version}")
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

        # Get the current script's directory instead of the working directory
        output_dir = os.path.dirname(os.path.abspath(__file__))

        # Use wget to retrieve the HTML content of the page
        html_content = wget.download(url, out=output_dir)

        # Extract the link to the file on the page
        link = ''
        with open(os.path.join(output_dir, html_content), 'r') as f:
            for line in f:
                if 'href' in line:
                    start = line.find('href="') + 6
                    end = line.find('"', start)
                    link = line[start:end]
                    if link.endswith('.conf'):
                        link = url + link
                        break

        # Download the file
        filename = os.path.basename(link)
        output_file = os.path.join(output_dir, "new" + filename)
        wget.download(link, out=output_file)

        #shutil.move(output_file, os.path.join(output_dir, 'platform.conf'))

        print(f"File {output_file} -- saved!")

        # Delete the HTML file
        os.remove(os.path.join(output_dir, html_content))

    except Exception as e:
        print("Downloading file error: " + str(e))

def delete_existing_file():
    # Get the current script's directory instead of the working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the platform.conf file and newplatform.conf file
    platform_conf_path = os.path.join(current_dir, 'platform.conf')
    new_platform_conf_path = os.path.join(current_dir, 'newplatform.conf')

    # Check if the platform.conf file exists
    if os.path.exists(platform_conf_path):
        os.remove(platform_conf_path)

    # Rename the newplatform.conf file to platform.conf
    os.rename(new_platform_conf_path, platform_conf_path)
    print("Successfully updated platform.conf file.")

    for key, values in paths.items():
        delete_files_dir = os.path.join(current_dir, values[0])
        for filename in os.listdir(delete_files_dir):
            file_path = os.path.join(delete_files_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print("Deleted" + filename)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")


def create_required_directories():
    # Get the current script's directory instead of the working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Iterate through the paths and create required directories if they don't exist
    for key, values in paths.items():
        dir_path = os.path.join(current_dir, values[0])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

if __name__ == "__main__":
    get_datasets()
