-- ==============================================================================
-- 🐝 Apache Hive — External Tables and Partitioned DDL Schema
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS retail_warehouse
LOCATION '/user/hive/warehouse/retail_warehouse.db';

USE retail_warehouse;

-- 1. External CSV Table mapping to HDFS storage
DROP TABLE IF EXISTS raw_customers;
CREATE EXTERNAL TABLE raw_customers (
    customer_id INT,
    first_name STRING,
    last_name STRING,
    email STRING,
    city STRING,
    country STRING,
    registration_date STRING,
    credit_limit DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data/sqoop/customers'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. Partitioned Columnar Snappy Parquet Table (Data Lakehouse Tier)
DROP TABLE IF EXISTS customer_analytics;
CREATE TABLE customer_analytics (
    customer_id INT,
    full_name STRING,
    email STRING,
    city STRING,
    credit_limit DOUBLE,
    credit_tier STRING
)
PARTITIONED BY (country STRING)
STORED AS PARQUET
TBLPROPERTIES ("parquet.compression"="SNAPPY");
