import pg8000
import json

# Credentials for Database connection:
credentials = {
    'user': 'postgres',
    'host': 'database-5761i.cfk2gikqsjhw.eu-west-2.rds.amazonaws.com',
    'database': 'database5761',
    'password': 'amberdog',
    'port': 5432
}

# Load Data from json file:
with open('db/dbdata.json') as file:
    data = json.loads(file.read())


# Counterparty function - creates table and populates with data.
def counterparty():
    # Establish Connection to Database
    con = pg8000.connect(
        host=credentials['host'],
        port=credentials['port'],
        database=credentials['database'],
        user=credentials['user'],
        password=credentials['password']
    )
    table = data['counterparty']
    create_table = f"""
        DROP TABLE IF EXISTS counterparty;
        CREATE TABLE counterparty (
            counterparty_id SERIAL PRIMARY KEY,
            counterparty_legal_name VARCHAR,
            legal_address_id INTEGER,
            commercial_contact VARCHAR,
            delivery_contact VARCHAR,
            created_at TIMESTAMP WITHOUT TIME ZONE,
            last_updated TIMESTAMP WITHOUT TIME ZONE
        );
    """
    con.run(create_table)
    # Iterate through values and create queries.
    for x in table:
        val = f"{x['counterparty_id']}, '{x['counterparty_legal_name']}', {x['legal_address_id']}, '{x['commercial_contact']}', '{x['delivery_contact']}', '{x['created_at']}', '{x['last_updated']}'"

        sentence = f"""INSERT INTO counterparty (counterparty_id, counterparty_legal_name, legal_address_id, commercial_contact, delivery_contact, created_at, last_updated)
        VALUES ({val});"""
        print(sentence)
        con.run(sentence)
    # print(con.run('SELECT * FROM counterparty;'))
    con.close()


counterparty()
