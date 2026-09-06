-- ==============================================================================
-- 🐝 Apache Hive — Analytical Window Functions & Rollup Queries
-- ==============================================================================

USE retail_warehouse;

-- 1. Insert Transformed Records into Partitioned Parquet Table
INSERT OVERWRITE TABLE customer_analytics PARTITION (country)
SELECT 
    customer_id,
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    city,
    credit_limit,
    CASE 
        WHEN credit_limit >= 10000 THEN 'PLATINUM'
        WHEN credit_limit >= 5000  THEN 'GOLD'
        ELSE 'SILVER'
    END AS credit_tier,
    country
FROM raw_customers
WHERE customer_id IS NOT NULL;

-- 2. Advanced Analytical Window Query (Dense Rank & Running Total)
SELECT 
    country,
    credit_tier,
    full_name,
    credit_limit,
    DENSE_RANK() OVER (PARTITION BY country ORDER BY credit_limit DESC) AS country_rank,
    SUM(credit_limit) OVER (PARTITION BY country) AS total_country_credit,
    AVG(credit_limit) OVER () AS global_avg_credit
FROM customer_analytics
ORDER BY country, country_rank;
