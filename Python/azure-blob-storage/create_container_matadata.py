from collections import defaultdict
import configparser

from azure.storage.blob import BlobServiceClient
import pandas as pd

config = configparser.ConfigParser()

config.read('example.ini')

STORAGE_KEY = config["azure-storage"]["storage_key"]
STORAGE_ACCOUNT_URL = config["azure-storage"]["storage_url"]
STORAGE_CONTAINER_NAME = config["azure-storage"]["container_name"]

# create a storage account service client

service = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=STORAGE_KEY)

# create a container client

container_client = service.get_container_client(STORAGE_CONTAINER_NAME)

# list all blobs in the container

blobs = container_client \
    .list_blobs()

container_data = defaultdict(list)

for blob in blobs:
    file_name = blob.name.split("/")[-1]
    path = "/".join(blob.name.split("/")[:-1])
    container_data["container"].append(blob.container)
    container_data["name"].append(blob.name)
    container_data["size"].append(blob.size)
    container_data["blob_tier"].append(blob.blob_tier)
    container_data["creation_time"].append(blob.creation_time)
    container_data["path"].append(path)
    container_data["file_name"].append(file_name)

print(container_data)

df = pd.DataFrame(container_data)

# save file to same container

blob = container_client \
    .get_blob_client("container_metadata/azure_storage_metadata.csv")

blob.upload_blob(df.to_csv(index=False), overwrite = True)