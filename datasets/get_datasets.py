import urllib.request
from urllib.parse import urlparse
from datetime import datetime
import posixpath

# path = urlparse.urlsplit(url).path
# filename = posixpath.basename(path)

def main():

    print("Start Program... ")

    try:
        print("Start Downloading file... ")

        # Get current time
        timenow = datetime.now()
        timenow_iso = timenow.strftime('%Y-%m-%d')
        
        # Retrieve data
        url = 'http://ftp.ebi.ac.uk/pub/databases/opentargets/platform/23.02/output/etl/parquet/targets/part-00000-7c4d21db-d777-42ee-ae66-67426a0369f1-c000.snappy.parquet'

        # Add output's file name and location
        output = f'opentarget/OT_target_{timenow_iso}.parquet'
        urllib.request.urlretrieve(url, output)

        print(f"File {output} -- saved!")

    except Exception as e:
        print("Downloading file error: " + str(e))

if __name__ == "__main__":
    main()