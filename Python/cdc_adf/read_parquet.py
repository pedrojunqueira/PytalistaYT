import configparser

from adlfs import AzureBlobFileSystem
import pyarrow as pa
import pyarrow.parquet as pq

config = configparser.ConfigParser()

config.read('configparser.ini')

STORAGE_KEY = config["azure-storage"]["storage_key"]
STORAGE_ACCOUNT_URL = config["azure-storage"]["storage_url"]
STORAGE_CONTAINER_NAME = config["azure-storage"]["container_name"]
STORAGE_ACCOUNT_NAME = config["azure-storage"]["account_name"]
FOLDER_PATH = '/bronze/customers/incremental/'

fs = AzureBlobFileSystem(account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_KEY)

parquet_files = []
for root, dirs, files in fs.walk(FOLDER_PATH):
    for file in files:
        if file.endswith('.parquet'):
            parquet_files.append(fs.sep.join([root, file]))

data = []

for file in parquet_files:
    with fs.open(file, 'rb') as f:
        table = pq.read_table(f)
        data.append(table)

table = pa.concat_tables(data)

df = table.to_pandas()

print(df.loc[:,"customer_id":])

