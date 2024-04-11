import pg8000
import json
import boto3
from pprint import pprint
import pandas as pd
from forex_python.converter import CurrencyCodes
from datetime import datetime

online = 0

if online == 0:
    credentials = {'host': 'fact_purchase_order',
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


def dim_currency(file):
    # Currency_id, currency_code, currency_name.
    currency = file['currency']
    if len(currency) < 1:
        raise Exception('No data.')

    c = CurrencyCodes()
    dim_currency_obj = {'dim_currency': []}
    for record in currency:
        obj = {'currency_id': record['currency_id'], 'currency_code': record['currency_code'],
               'currency_name': c.get_currency_name(record['currency_code'])}
        dim_currency_obj['dim_currency'].append(obj)
    df = pd.DataFrame(data=dim_currency_obj)
    return df


def dim_design(file):
    design = file['design']
    dim_design_obj = {'dim_design': []}
    for item in design:
        obj = {'design_id': item['design_id'], 'design_name': item['design_name'],
               'file_location': item['file_location'], 'file_name': item['file_name']}
        dim_design_obj['dim_design'].append(obj)
    df = pd.DataFrame(data=dim_design_obj)
    return df


def dim_location(file):
    address = file['address']
    dim_location_obj = {'dim_location': []}
    for item in address:
        obj = {'location_id': item['address_id'], 'address_line_1': item['address_line_1'], 'address_line_2': item['address_line_2'],
               'district': item['district'], 'city': item['city'], 'postal_code': item['postal_code'], 'country': item['country'], 'phone': item['phone']}
        dim_location_obj['dim_location'].append(obj)
        df = pd.DataFrame(data=dim_location_obj)
    return dim_location_obj


def dim_staff(file):
    staff = file['staff']
    department = file['department']
    dim_staff_obj = {'dim_staff': []}
    for item in staff:
        staff_id = item['staff_id']
        department_id = item['department_id']
        obj = {'staff_id': item['staff_id'], 'first_name': item['first_name'], 'last_name': item['last_name'],
               'email_address': item['email_address']}
        for record in department:
            if department_id == record['department_id']:
                obj['department_name'] = record['department_name']
                obj['location'] = record['location']
                break
        dim_staff_obj['dim_staff'].append(obj)
    df = pd.DataFrame(data=dim_staff_obj)
    return df


def dim_date(file):
    sales_order = file['sales_order']
    dim_date_obj = {'dim_date': []}
    for item in sales_order:
        obj = {}
        datetime_str = item['created_at'].split('.')[0]
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        obj['date_id'] = item['created_at']
        obj['year'] = datetime_obj.year
        obj['month'] = datetime_obj.month
        obj['day'] = datetime_obj.day
        obj['day_of_week'] = datetime_obj.weekday()
        obj['day_name'] = datetime_obj.strftime('%A')
        obj['month_name'] = datetime_obj.strftime('%B')
        if datetime_obj.month > 0 and datetime_obj.month <= 3:
            quarter = 1
        elif datetime_obj.month > 3 and datetime_obj.month <= 6:
            quarter = 2
        elif datetime_obj.month > 6 and datetime_obj.month <= 9:
            quarter = 3
        else:
            quarter = 4
        obj['quarter'] = quarter
        dim_date_obj['dim_date'].append(obj)
    df = pd.DataFrame(data=dim_date_obj)
    return df


def fact_sales_order(file):
    sales_order = file['sales_order']
    fact_sales_order_obj = {'fact_sales_order': []}
    for item in sales_order:
        pprint(item)
        obj = {}
        obj['sales_order_id'] = item['sales_order_id']
        obj['created_date'] = item['created_at'][0:10]
        obj['created_time'] = item['created_at'][10:]
        obj['last_updated_date'] = item['last_updated'][0:10]
        obj['last_updated_time'] = item['last_updated'][10:]
        obj['sales_staff_id'] = item['staff_id']
        obj['counterparty_id'] = item['counterparty_id']
        obj['units_sold'] = item['units_sold']
        obj['unit_price'] = item['unit_price']
        obj['currency_id'] = item['currency_id']
        obj['design_id'] = item['design_id']
        obj['agreed_payment_date'] = item['agreed_payment_date']
        obj['agreed_delivery_date'] = item['agreed_delivery_date']
        obj['agreed_delivery_location_id'] = item['agreed_delivery_location_id']
        fact_sales_order_obj['fact_sales_order'].append(obj)
    df = pd.DataFrame(data=fact_sales_order_obj)
    return df
