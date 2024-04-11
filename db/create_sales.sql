DROP TABLE IF EXISTS dim_counterparty;
CREATE TABLE dim_counterparty
    (
    counterparty_id SERIAL PRIMARY KEY,
    counterparty_legal_name character varying,
    counterparty_legal_address_line_1 character varying,
    counterparty_legal_address_line_2 character varying,
    counterparty_legal_district character varying, 
    counterparty_legal_city character varying,
    counterparty_legal_postal_code character varying,
    counterparty_legal_country character varying,
    counterparty_legal_phone_number character varying 
    );

DROP TABLE IF EXISTS dim_currency;
CREATE TABLE dim_currency 
    (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR,
    currency_name VARCHAR
    );

DROP TABLE IF EXISTS dim_location;
CREATE TABLE dim_location 
    (
    location_id SERIAL PRIMARY KEY,
    address_line_1 VARCHAR,
    address_line_2 VARCHAR,
    district VARCHAR,
    city VARCHAR,
    postal_code VARCHAR,
    country VARCHAR,
    phone VARCHAR
    );

DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    day_name VARCHAR,
    mont_name VARCHAR,
    quarter
);

DROP TABLE IF EXISTS dim_staff;
CREATE TABLE dim_staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    department_name VARCHAR,
    location VARCHAR,
    email_address VARCHAR
);

DROP TABLE IF EXISTS fact_purchase_order;
CREATE TABLE fact_purchase_order (
    purchase_record_id SERIAL PRIMARY KEY,
    purchase_order_id INT,
    created_date DATE,
    created_time TIME,
    last_updated_date DATE,
    last_updated_time TIME,
    staff_id INT,
    counterparty_id INT,
    item_code VARCHAR,
    item_quantity INT,
    item_unit_price NUMERIC,
    currency_id INT,
    agreed_delivery_date DATE,
    agreed_payment_date DATE,
    agreed_delivery_location_id INT
);