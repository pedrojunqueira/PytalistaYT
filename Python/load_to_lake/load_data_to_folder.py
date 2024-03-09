from datetime import datetime
import configparser

import adlfs

config = configparser.ConfigParser()


config.read('config.ini')

STORAGE_ACCOUNT_NAME = config["azure"]["azure_storage_account_name"]
STORAGE_ACCOUNT_KEY = config["azure"]["azure_storage_account_key"] 

fs = adlfs.AzureBlobFileSystem(
        account_name=STORAGE_ACCOUNT_NAME,
        account_key=STORAGE_ACCOUNT_KEY,
    )



with fs.open("copy-files/hello.txt", "w") as fp:
    fp.write("hello world")

