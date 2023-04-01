import wget
import os
import urllib.request
from urllib.parse import urlparse
from datetime import datetime
import posixpath


def main():
    print("Start Program... ")

    try:
        print("Start Downloading files... ")

        # Get current time
        timenow = datetime.now()
        timenow_iso = timenow.strftime('%Y-%m-%d')

        # Specify the URL

        
        url = 'https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.04/output/etl/parquet/diseases/'

        # Use the current directory as the output directory
        output_dir = os.getcwd()

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
        for link in links:
            filename = os.path.basename(link)
            output_file = os.path.join(output_dir, filename)
            wget.download(link, out=output_file)

        print("Files downloaded successfully!")

    except Exception as e:
        print("Downloading files error: " + str(e))

if __name__ == "__main__":
    main()