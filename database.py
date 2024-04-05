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
    pass


create_database()
add_data()
con.close()
