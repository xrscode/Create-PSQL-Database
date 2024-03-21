\c temp_staff

DROP TABLE IF EXISTS counterparty;
CREATE TABLE counterparty 
    (
    counterparty_id SERIAL PRIMARY KEY,
    counterparty_legal_name character varying,
    legal_address_id integer,
    commercial_contact character varying,
    delivery_contact character varying,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
    );

DROP TABLE IF EXISTS address;
CREATE TABLE address
    (
    address_id SERIAL PRIMARY KEY,
    address_line_1 character varying,
    address_line_2 character varying, 
    district character varying, 
    postal_code character varying, 
    country character varying, 
    phone character varying, 
    created_at timestamp without time zone, 
    last_updated timestamp without time zone
    );

DROP TABLE IF EXISTS currency;
CREATE TABLE currency
    (
    currency_id integer,
    currency_code character varying,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
    );

DROP TABLE IF EXISTS department;
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name character varying,
    location character varying,
    manager character varying,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);

DROP TABLE IF EXISTS design;
CREATE TABLE design (
    design_id integer,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    design_name character varying,
    file_location character varying,
    file_name character varying
);

DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    transaction_id integer,
    counterparty_id integer,
    payment_amount numeric,
    currency_id integer,
    payment_type_id integer,
    paid boolean,
    payment_date character varying,
    company_ac_number integer,
    counterparty_ac_number integer
);

DROP TABLE IF EXISTS payment_type;
CREATE TABLE payment_type (
    payment_type_id integer,
    payment_type_name character varying,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);

DROP TABLE IF EXISTS purchase_order;
CREATE TABLE purchase_order (
    purchase_order_id SERIAL PRIMARY KEY,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    staff_id integer,
    counterparty_id integer,
    item_code character varying,
    item_quantity integer,
    item_unit_price numeric,
    currency_id integer,
    agreed_delivery_date character varying,
    agreed_payment_date character varying,
    agreed_delivery_location_id integer
);

DROP TABLE IF EXISTS sales_order;
CREATE TABLE sales_order (
    sales_order_id SERIAL PRIMARY KEY,
    created_at timestamp without time zone,
    last_updated timestamp without time zone,
    design_id integer,
    staff_id integer,
    counterparty_id integer,
    units_sold integer,
    unit_price numeric,
    currency_id integer,
    agreed_delivery_date character varying,
    agreed_payment_date character varying,
    agreed_delivery_location_id integer
);

DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    second_name VARCHAR,
    department_id INT,
    email_address VARCHAR,
    last_updated DATE,
    created_at DATE
);

DROP TABLE IF EXISTS transaction; 
CREATE TABLE transaction (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type character varying,
    sales_order_id character varying,
    purchase_order_id character varying,
    created_at timestamp without time zone,
    last_updated timestamp without time zone
);