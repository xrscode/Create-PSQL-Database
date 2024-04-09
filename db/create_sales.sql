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