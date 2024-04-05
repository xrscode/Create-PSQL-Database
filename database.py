import pg8000
import json
import boto3

online = 0

if online == 0:
    con = pg8000.connect(
        host='localhost',
        port=5432,
        database='totesys',
        user='mac'
    )
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
        return data

    credentials = get_secret()

    con = pg8000.connect(
        host=credentials['host'],
        port=credentials['port'],
        database=credentials['dbname'],
        user=credentials['username'],
        password=credentials['password']
    )

# Load Data from json file:
with open('db/dbdata.json') as file:
    data = json.loads(file.read())

# Load SQL Queries to setup database:
with open('db/02-create_tables.sql') as file:
    sql = file.read()


# # Counterparty function - creates table and populates with data.
# def create_counterparty_table():
#     # Establish Connection to Database
#     create_table = f"""DROP TABLE IF EXISTS counterparty;
#     CREATE TABLE counterparty (
#     counterparty_id SERIAL PRIMARY KEY,
#     counterparty_legal_name VARCHAR,
#     legal_address_id INTEGER,
#     commercial_contact VARCHAR,
#     delivery_contact VARCHAR,
#     created_at TIMESTAMP WITHOUT TIME ZONE,
#     last_updated TIMESTAMP WITHOUT TIME ZONE);
#     """
#     con.run(create_table)
#     con.commit()
#     con.close()


# def insert_counterparty():
#     counterparty = data['counterparty']
#     # Establish Connection to Database
#     con = pg8000.connect(
#         host=credentials['host'],
#         port=credentials['port'],
#         database=credentials['database'],
#         user=credentials['user'],
#         # password=credentials['password']
#     )

#     cursor = con.cursor()

#     for item in counterparty:
#         id = item['counterparty_id']
#         legal = item['counterparty_legal_name']
#         address = item['legal_address_id']
#         commercial = item['commercial_contact']
#         delivery = item['delivery_contact']
#         created = item['created_at']
#         last = item['last_updated']

#         query = f"""
#         INSERT INTO COUNTERPARTY (counterparty_id, counterparty_legal_name, legal_address_id, commercial_contact, delivery_contact, created_at, last_updated)
#         VALUES (%s, %s, %s, %s, %s, %s, %s);
#         """
#         vals = (id, legal, address, commercial, delivery, created, last)
#         cursor.execute(query, vals)
#         con.commit()
#     cursor.close()
#     con.close()

# This function will create the database structure.


def create_database():
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


def add_data():
    f"""This function will add data to a PSQL database."""
    cursor = con.cursor()
    for item in data:
        # Iterate over Table.
        table = item
        print(f"Adding data to {table}")
        rows = [x for x in data[item][0]]
        placeholder = ', '.join('%s' for _ in range(len(rows)))
        a = data[item]

        for x in a:
            # Iterate over values in table
            val = [str(value) for value in x.values()]
            query = f"""INSERT INTO {table} ({', '.join(rows)}) VALUES ({placeholder});"""
            cursor.execute(query, val)
            con.commit()
        print(f'Data added to {table}...moving onto next table now.')
    cursor.close()
    con.close()
    pass


# create_database()
# add_data()
