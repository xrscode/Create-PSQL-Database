import pg8000
import json
import boto3
from pprint import pprint
import pandas as pd

online = 0

if online == 0:
    credentials = {'host': 'localhost',
                   'port': 5432,
                   'database': 'staff',
                   'user': 'mac'}

elif online == 1:
    credentials = None
    # AWS Secret Parameter Store - DB Credentials.
    # def get_secret():
    #     secret_name = "totesysDatabase"
    #     region_name = "eu-west-2"
    #     # Create a Secrets Manager client
    #     session = boto3.session.Session()
    #     client = session.client(
    #         service_name='secretsmanager',
    #         region_name=region_name
    #     )
    #     try:
    #         get_secret_value_response = client.get_secret_value(
    #             SecretId=secret_name
    #         )
    #     except RuntimeError as e:
    #         raise e
    #     secret = get_secret_value_response['SecretString']
    #     data = json.loads(secret)
    #     cred = {
    #         'host': data['host'],
    #         'port': data['port'],
    #         'user': data['username'],
    #         'password': data['password'],
    #         'database': data['dbname']
    #     }
    #     return cred
    # credentials = get_secret()

    # Load Data from json file:
with open('db/dbdata.json') as file:
    data = json.loads(file.read())

# Load SQL Queries to setup database:
with open('db/create_sales.sql') as file:
    sql = file.read()


def create_sales():
    # Creates tables for sales
    con = pg8000.connect(**credentials)
    queries = sql.split(';')
    for query in queries:
        print(query)
        con.run(query)
        con.commit()
    con.close()
    return queries


def dim_counterparty(file):
    """
    Function accepts a JSON object. 
    JSON object must have 'counterparty' and 'address' data. 
    Combines tables into 'dim_counterparty'.
    Converts dim_counterparty into pandas dataframe.
    Returns dataframe.
    """
    # Check there is data in 'counterparty'
    counterparty = file['counterparty']
    address = file['address']

    # Handle 0 data:
    if len(counterparty) == 0 or len(address) == 0:
        raise Exception('Not enough data.')

    # Create 'dim_counterparty' object.
    dim_counterparty_obj = {'dim_counterparty': []}

    for record in counterparty:
        schema = {'counterparty_id': record['counterparty_id'],
                  'counterparty_legal_name': record['counterparty_legal_name']}
        for item in address:
            if item['address_id'] == record['legal_address_id']:
                schema['counterparty_legal_address_line_1'] = item['address_line_1']
                schema['counterparty_legal_address_line_2'] = item['address_line_2']
                schema['counterparty_legal_district'] = item['district']
                schema['counterparty_legal_city'] = item['city']
                schema['counterparty_legal_postal_code'] = item['postal_code']
                schema['counterparty_legal_country'] = item['country']
                schema['counterparty_legal_phone_number'] = item['phone']

                break  # Stop Searching once address is found.
        dim_counterparty_obj['dim_counterparty'].append(schema)
    df = pd.DataFrame(data=dim_counterparty_obj)
    return df


print(dim_counterparty(data))

#   dim_staff = ['staff_id', 'first_name', 'last_name',
#                  'department_name', 'location', 'email_address']
#     dim_data = ['date_id', 'year', 'month', 'day',
#                 'day_of_week', 'day_name', 'month_name', 'quarter']
#     dim_counterparty = ['counterparty_id', 'counterparty_legal_name', 'counterparty_legal_address_line_1', 'counterparty_legal_address_line_2',
#                         'counterparty_legal_district', 'counterparty_legal_city', 'counterparty_legal_postal_code', 'counterparty_legal_country', 'counterparty_legal_phone_number']
#     dim_currency = ['currency_id', 'currency_code', 'currency_name']
#     dim_design = ['design_id', 'design_name', 'file_location', 'file_name']
#     dim_location = ['location_id', 'address_line_1', 'address_line_2',
#                     'district', 'city', 'postal_code', 'country', 'phone']
#     dim_date = ['date_id', 'year', 'month', 'day',
#                 'day_of_week', 'day_name', 'month_name', 'quarter']
#     fact_Sales_order = ['sales_record_id', 'sales_order_id', 'created_date', 'created_time', 'last_updated_date', 'sales_staff_id', 'counterparty_id',
#                         'units_sold', 'unit_price', 'currency_id', 'design_id', 'agreed_payment_date', 'agreed_delivery_date', 'agreed_delivery_location_id']
