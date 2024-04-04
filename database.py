import pg8000
import json

# Credentials for Database connection:
# credentials = {
#     'user': 'postgres',
#     'host': 'database-5761i.cfk2gikqsjhw.eu-west-2.rds.amazonaws.com',
#     'database': 'database5761',
#     'password': 'amberdog',
#     'port': 5432
# }

# Credentials for Local connection:
credentials = {
    'user': 'mac',
    'host': 'localhost',
    'database': 'totesys',
    'port': 5432
}

# Load Data from json file:
with open('db/dbdata.json') as file:
    data = json.loads(file.read())


# Counterparty function - creates table and populates with data.
def create_counterparty_table():
    # Establish Connection to Database
    con = pg8000.connect(
        host=credentials['host'],
        port=credentials['port'],
        database=credentials['database'],
        user=credentials['user'],
        # password=credentials['password']
    )
    
    create_table = f"""DROP TABLE IF EXISTS counterparty;
    CREATE TABLE counterparty (
    counterparty_id SERIAL PRIMARY KEY,
    counterparty_legal_name VARCHAR,
    legal_address_id INTEGER,
    commercial_contact VARCHAR,
    delivery_contact VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    last_updated TIMESTAMP WITHOUT TIME ZONE);
    """
    con.run(create_table)
    con.commit()
    con.close()

def insert_counterparty():
    counterparty = data['counterparty']
    # Establish Connection to Database
    con = pg8000.connect(
        host=credentials['host'],
        port=credentials['port'],
        database=credentials['database'],
        user=credentials['user'],
        # password=credentials['password']
    )

    cursor = con.cursor()

   
    for item in counterparty:
        id = item['counterparty_id']
        legal = item['counterparty_legal_name']
        address = item['legal_address_id']
        commercial = item['commercial_contact']
        delivery = item['delivery_contact']
        created = item['created_at']
        last = item['last_updated']

        query = f"""
        INSERT INTO COUNTERPARTY (counterparty_id, counterparty_legal_name, legal_address_id, commercial_contact, delivery_contact, created_at, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        vals = (id, legal, address, commercial, delivery, created, last)
        cursor.execute(query, vals)
        con.commit()
    cursor.close()
    con.close()
