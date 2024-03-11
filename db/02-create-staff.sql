\c temp_staff
DROP TABLE IF EXISTS staff_table;
CREATE TABLE staff_table (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    second_name VARCHAR,
    department_id INT,
    email_address VARCHAR,
    last_updated DATE,
    created_at DATE
);
