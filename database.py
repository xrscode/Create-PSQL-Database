import pg8000
import json
import boto3
from dotenv import load_dotenv
import os

online = 0

if online == 0:
    load_dotenv()
    credentials = {'host': os.getenv("DB_HOST"),
                   'port': os.getenv("DB_PORT"),
                   'database': os.getenv("DB_NAME"),
                   'user': os.getenv("DB_USER")}

elif online == 1:

    # AWS Secret Parameter Store - DB Credentials.
    def get_secret():
        secret_name = "totesysDatabase"
        region_name = "eu-west-2"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except RuntimeError as e:
            raise e
        secret = get_secret_value_response['SecretString']
        data = json.loads(secret)
        cred = {
            'host': data['host'],
            'port': data['port'],
            'user': data['username'],
            'password': data['password'],
            'database': data['dbname']
        }
        return cred
    credentials = get_secret()

# Load Data from json file:
with open('db/dbdata.json') as file:
    data = json.loads(file.read())

# Load SQL Queries to setup database:
with open('db/create_totesys.sql') as file:
    sql = file.read()


def create_database():
    con = pg8000.connect(**credentials)
    f"""This function will create a PSQL databse."""
    queries = sql.split('; ')
    for query in queries:
        try:
            con.run(query)
            con.commit()
        except RuntimeError as e:
            print(e)
    print('Database successfully created.')
    con.close()
    print('Connection closed.')


def add_data():
    con = pg8000.connect(**credentials)
    f"""This function will add data to a PSQL database."""
    cursor = con.cursor()
    for table in data:
        # Iterate through Dictionary.
        # Each Key is a table Name.
        print(f"Adding data to {table}")
        # Extract column names:
        column_names = [x for x in data[table][0]]
        column_names_string = ', '.join(column_names)
        placeholder = ', '.join('%s' for _ in range(len(column_names)))
        values = [list(row.values()) for row in data[table]]
        query = f"INSERT INTO {table} ({column_names_string}) VALUES ({placeholder});"
        cursor.executemany(query, values)
        con.commit()
    con.close()
    print('Connection closed.')
    pass


create_database()
add_data()
