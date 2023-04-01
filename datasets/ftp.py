from ftplib import FTP



#https://stackoverflow.com/questions/2605119/downloading-a-directory-tree-with-ftplib

ftp = FTP('ftp.ebi.ac.uk/pub/databases/opentargets/platform/23.02/output/etl/parquet/targets')  # connect to host, default port
ftp.login()                     # user anonymous, passwd anonymous@

ftp.cwd('targets')               # change into "debian" directory

ftp.retrlines('LIST')           # list directory contents


# with open('README', 'wb') as fp:
#     ftp.retrbinary('RETR README', fp.write)

ftp.quit()
