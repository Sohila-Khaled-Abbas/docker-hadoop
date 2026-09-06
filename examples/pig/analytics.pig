-- ==============================================================================
-- 🐷 Apache Pig — Customer Analytical Pipeline in Pig Latin
-- ==============================================================================

-- 1. Load CSV dataset with schema
customers = LOAD '$INPUT' USING PigStorage(',') AS (
    id:int,
    first_name:chararray,
    last_name:chararray,
    email:chararray,
    city:chararray,
    country:chararray,
    registration_date:chararray,
    credit_limit:double
);

-- 2. Filter active customers with credit limit >= 5000
high_value_customers = FILTER customers BY credit_limit >= 5000.0;

-- 3. Group by country
country_groups = GROUP high_value_customers BY country;

-- 4. Aggregate metrics per country
country_summary = FOREACH country_groups GENERATE
    group AS country,
    COUNT(high_value_customers) AS customer_count,
    SUM(high_value_customers.credit_limit) AS total_credit,
    AVG(high_value_customers.credit_limit) AS avg_credit;

-- 5. Sort by total credit descending
sorted_summary = ORDER country_summary BY total_credit DESC;

-- 6. Store to HDFS directory
STORE sorted_summary INTO '$OUTPUT' USING PigStorage(',');
