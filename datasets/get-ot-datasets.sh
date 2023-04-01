#!/bin/bash
echo "Retrieving data..."  


cd opentarget
cd targets
wget --recursive --no-parent --no-host-directories --cut-dirs 8 ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/23.02/output/etl/parquet/targets


echo "Done."  