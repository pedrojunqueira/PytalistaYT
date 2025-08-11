from faker import Faker
import pyodbc
import configparser

# Initialize Faker with Australian locale
fake = Faker('en_AU')

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Azure SQL Database connection details from config file
server = config['AZURE_DB']['server']
database = config['AZURE_DB']['database']
username = config['AZURE_DB']['username']
password = config['AZURE_DB']['password']

driver = '{ODBC Driver 18 for SQL Server}'

# Connect to Azure SQL Database
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

# Insert 10 rows of fake address data
for _ in range(10):
    street = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    postal_code = fake.postcode()
    # print(f"Inserting: {street}, {city}, {state}, {postal_code}")
    insert_query = """
    INSERT INTO Addresses (StreetAddress, City, State, PostalCode)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(insert_query, (street, city, state, postal_code))

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()