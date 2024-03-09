import configparser

import adlfs

config = configparser.ConfigParser()


config.read('config.ini')

STORAGE_ACCOUNT_NAME = config["azure"]["azure_storage_account_name"]
STORAGE_ACCOUNT_KEY = config["azure"]["azure_storage_account_key"] 
STORAGE_ACCOUNT_URL = config["azure"]["account_url"]

from azure.storage.blob import BlobServiceClient

service = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=STORAGE_ACCOUNT_KEY)

blob_client = service.get_blob_client(container="copy-files", blob="hello.txt")

with open("text.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)