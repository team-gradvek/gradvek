import wget
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
This script downloads Open Target datasets from the Open Target FTP server.
The datasets include information about diseases, FDA significant adverse drug reactions, 
mechanism of action, molecules, mouse phenotypes, and targets.

The script downloads files in parallel to try and speed up the process, particuarly when there are retries.
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
    "targets": ["opentarget/targets","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/targets/"]
}

def main():
    print("Starting the program...")

    # Iterate through the data types and their respective paths
    for key, values in paths.items():
        get_datasets(key, values[0], values[1])


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
                return False
            else:
                time.sleep(delay)

def get_datasets(name, project_path, ot_path, max_retries=3, delay=5, max_workers=5):
    try:
        print(f"Starting to download {name} files...")

        url = ot_path

        current_dir = os.getcwd()
        output_dir = f"{current_dir}/{project_path}"

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
        for n, link in enumerate(links):
            print(f"\nDownloading {name} file {n+1} of {len(links)} ")
            filename = os.path.basename(link)
            output_file = os.path.join(output_dir, filename)
            if os.path.exists(output_file):
                print(f"File {filename} already exists. Skipping...")
            else:
                tasks.append((link, output_file, max_retries, delay))

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

if __name__ == "__main__":
    main()
