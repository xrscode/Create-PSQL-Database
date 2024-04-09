## de-totes-project

A Github repository for the beekeepers group for the final data engineering Northcoders project.

The purpose of this project is to create applications that will Extract, Transform and Load data from a prepared source into a data lake and warehouse hosted in AWS.

The main challenges of the project are:
- to use python to interact with AWS and DB infrastructure and manipulate data as required
- to remodel data and insert it into a data warehouse hosted in AWS
- to monitor and record updated data 
- to have the project deployed using scripts or automation

this project will showcase knowledge of Python, SQL, database modelling, AWS, good operational practices and Agile working.

The intention is to create a data platform that extracts data from an operational database (and potentially other sources), archives it in a data lake, and makes it available in a remodelled OLAP data warehouse.

A Python application that continually ingests all tables from the `totesys` database will be used, this application must:
  - operate automatically on a schedule
  - log progress to Cloudwatch
  - trigger email alerts in the event of failures
  - follow good security practices (for example, preventing SQL injection and maintaining password security)

A separate Python application that remodels the data into a predefined schema suitable for a data warehouse and stores the data in Parquet format in a "processed" S3 bucket. This application must:
  - trigger automatically when it detects the completion of an ingested data job
  - be adequately logged and monitored
  - populate the dimension and fact tables of a single "star" schema in the warehouse (see details below) 

Another Python application that loads the data into a prepared data warehouse at defined intervals, which should be adequately logged and monitored and include a Quicksight dashboard that allows users to view useful data in the warehouse

The project will demonstrate that a change to the source database will be reflected in the data warehouse within 30 minutes at most.

## Tables

The tables to be ingested from `totesys` DB are:
|tablename|
|----------|
|counterparty|
|currency|
|department|
|design|
|staff|
|sales_order|
|address|
|payment|
|purchase_order|
|payment_type|
|transaction|

The list of tables in the complete warehouse is:
|tablename|
|---------|
|fact_sales_order|
|fact_purchase_orders|
|fact_payment|
|dim_transaction|
|dim_staff|
|dim_payment_type|
|dim_location|
|dim_design|
|dim_date|
|dim_currency|
|dim_counterparty|

The minimum viable product populates the following:
|tablename|
|---------|
|fact_sales_order|
|dim_staff|
|dim_location|
|dim_design|
|dim_date|
|dim_currency|
|dim_counterparty|

### Prerequisites for local development
- Python
- Make

## Instructions
1. First clone this repo. 
2. In the terminal, navigate to the root directory of the project, and run:
    ```bash
    make requirements
    ```
(more to be added to this later)
