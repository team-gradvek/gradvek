import wget
import os
import urllib.request
from urllib.parse import urlparse
from datetime import datetime
import posixpath


# Project path and Open Target path dict
paths = {
    "diseases": ["opentarget/diseases", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/diseases/"],
    "fda": ["opentarget/fda", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/fda/significantAdverseDrugReactions/"],
    "mechanismOfAction": ["opentarget/mechanismOfAction", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/mechanismOfAction/"],
    "molecules": ["opentarget/molecule", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/molecule/"],
    "mousePhenotypes": ["opentarget/mousePhenotypes", "https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/mousePhenotypes/"],
    "targets": ["opentarget/targets","https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/etl/parquet/targets/"]
}


def main():

    print("Start Program... ")

    for key, values in paths.items():
        get_datasets(key, values[0], values[1])

    
def get_datasets(name, project_path, ot_path):
    """
    Get and download datasets files inside Open Target(OT) directory.
    """
    try:
        print(f"Start Downloading {name} files... ")

        # Specify the URL
        url = ot_path

        # Use the opentarget directory as the output directory
        current_dir = os.getcwd()
        output_dir = f"{current_dir}/{project_path}"

        # remove any lingering .tmp files from the output directory
        for file in os.listdir(output_dir):
            if file.endswith(".tmp"):
                os.remove(os.path.join(output_dir, file))

        # Use wget to retrieve the HTML content of the page
        html_content = wget.download(url, out=output_dir)

        # Extract the links to the files on the page
        links = []
        with open(os.path.join(output_dir, html_content), 'r') as f:
            for line in f:
                if 'href' in line:
                    start = line.find('href="') + 6
                    end = line.find('"', start)
                    link = line[start:end]
                    if link.endswith('.parquet'):
                        links.append(url + link)
        # Download the files
        for n, link in enumerate(links):
            print(f"\nDownloading {name} file {n+1} of {len(links)} ")
            filename = os.path.basename(link)
            output_file = os.path.join(output_dir, filename)
            if os.path.exists(output_file):
                print(f"File {filename} already exists. Skipping...")
            else:
                wget.download(link, out=output_file)

        print("Files downloaded successfully!")

    except Exception as e:
        print("Downloading files error: " + str(e))

if __name__ == "__main__":
    main()