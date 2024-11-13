# rsd_gcs_download
Small repo to create a subset-table and bulk download the data linked to the table. 

Requirements: 
- GCS account
- authentification key

How to access the public dataset is written here: https://cloud.google.com/bigquery/public-data?hl=de and the specific data can be found by using the index: bigquery-public-data.cloud_storage_geo_index

The rsd_data_query.sql file is an example to access the landsat and sentinel-2 folders and and filter the desired data. This script is executed in the gcs query console. The resulting table needs to be safed in the lokal project to access it with the rsd_bulk_download.py file. 

By using the python file of this repo, you need your authentification key.json to allow python to access your local table. This key can be created in the google cloud console https://console.cloud.google.com/. 
It is possible to further filter the objects you would like to download via the query. Before downloading, the script prints the number of folders available and the total size in GB. Due to the possibly large files, the script takes care of erroneously downloads by checking in if you actually want to download the files. 
