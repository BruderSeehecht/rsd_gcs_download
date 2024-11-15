# script to bulk download the rsd datasets with additional filter options 

from google.oauth2 import service_account
from google.cloud import bigquery, storage
import os
from tqdm import tqdm

# Set up credentials
credentials = service_account.Credentials.from_service_account_file('/path/to/key.json')
bigquery_client = bigquery.Client(credentials=credentials)
storage_client = storage.Client(credentials=credentials)

# Set up the query
query = """
SELECT source_url, total_size
FROM `bucket_name.folder_path.table_name`
WHERE EXTRACT(YEAR FROM sensing_time) = 2017
""" 

# Run the query
query_job = bigquery_client.query(query)
results = query_job.result()

# Define a local directory to store the downloaded files
output_folder = '/path/to/output/folder'

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Initialize counters
total_folders = 0
total_size = 0
folders_to_download = []

# List folders to be downloaded
for row in results:
    source_url = row.source_url
    folder_size = row.total_size
    
    # Extract bucket name and folder path from the source URL
    bucket_name = source_url.split('/')[2]  # Assuming source_url format is gs://bucket_name/folder_path
    folder_path = '/'.join(source_url.split('/')[3:])

    # Get the bucket object
    bucket = storage_client.bucket(bucket_name)

    # Check if the folder path exists
    blobs = list(bucket.list_blobs(prefix=folder_path))
    if not blobs:
        print(f"Error: The folder path '{folder_path}' does not exist or is empty.")
        continue

    total_folders += 1
    total_size += folder_size
    folders_to_download.append((bucket, folder_path))

# Print summary of folders to be downloaded
print(f"Total folders found: {total_folders}")
print(f"Total size of files to be downloaded: {total_size / (1024 ** 3):.2f} GB")

# Confirm download
confirm = input("Do you want to download these files? (yes/no): ").strip().lower()
if confirm != 'yes':
    print("Download cancelled.")
    exit()

# Initialize counters for download
total_files = 0
downloaded_files = 0
failed_files = 0

# Download files from each folder
for bucket, folder_path in folders_to_download:
    blobs = list(bucket.list_blobs(prefix=folder_path))
    total_files += len(blobs)
    for blob in tqdm(blobs, desc=f"Downloading files from {folder_path}"):
        try:
            # Create a local file path based on the blob's name
            local_file_path = os.path.join(output_folder, blob.name)
            local_dir = os.path.dirname(local_file_path)
            os.makedirs(local_dir, exist_ok=True)

            # Download the blob to the local file
            blob.download_to_filename(local_file_path)
            downloaded_files += 1

            print(f"Downloaded '{blob.name}' to '{local_file_path}'")
        except Exception as e:
            failed_files += 1
            print(f"Failed to download '{blob.name}': {e}")

# Print summary
print(f"Total files found: {total_files}")
print(f"Total files downloaded: {downloaded_files}")
print(f"Total files failed: {failed_files}")
