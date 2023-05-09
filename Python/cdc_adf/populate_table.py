import logging
import configparser
from typing import List

import pyodbc
from faker import Faker

config = configparser.ConfigParser()

config.read('configparser.ini')

SQL_SERVER =  config["azure-sqldb"]["sql_server"]
SQL_DATABASE = config["azure-sqldb"]["sql_db"]
SQL_USER_NAME = config["azure-sqldb"]["sql_user_name"]
SQL_PASSWORD = config["azure-sqldb"]["sql_password"]

TABLE_NAME = 'dbo.customers'

driver= '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER=tcp:{SQL_SERVER};PORT=1433;DATABASE={SQL_DATABASE};UID={SQL_USER_NAME};PWD={SQL_PASSWORD}'



def create_records_customers(number: int):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT max(customer_id) FROM {TABLE_NAME}')
        rows = cursor.fetchall()
        max_id = rows[0][0]
    fake = Faker()
    records = []
    for i in range(max_id, max_id + number):
        name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        city = fake.city()
        records.append((i+1, name, last_name, email, city))
    return records

def fast_load(tuples: List[tuple], table: str)->None:

    connection_string = f'DRIVER={driver};SERVER=tcp:{SQL_SERVER};PORT=1433;DATABASE={SQL_DATABASE};UID={SQL_USER_NAME};PWD={SQL_PASSWORD}'

    with pyodbc.connect(connection_string) as conn:

        try:

            insert_to_tmp_tbl_stmt = f"INSERT INTO {table} VALUES (?,?,?,?,?)"
            cursor = conn.cursor()
            cursor.fast_executemany = True
            if tuples:
                cursor.executemany(insert_to_tmp_tbl_stmt, tuples)
                cursor.commit()
        except Exception as e:
            logging.debug(e)


def auto_insert_records():
    records_to_insert = create_records_customers(5)
    fast_load(records_to_insert, TABLE_NAME)

if __name__ == "__main__":
    auto_insert_records()