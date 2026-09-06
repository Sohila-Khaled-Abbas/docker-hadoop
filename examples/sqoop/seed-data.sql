-- ==============================================================================
-- 🐬 Apache Sqoop — RDBMS Mock Database & Seed Schema
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS retail_db;
USE retail_db;

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    city VARCHAR(50),
    country VARCHAR(50),
    registration_date DATE,
    credit_limit DECIMAL(10,2)
);

INSERT INTO customers (first_name, last_name, email, city, country, registration_date, credit_limit) VALUES
('Layla', 'Mahmoud', 'layla.m@example.com', 'Cairo', 'Egypt', '2024-01-15', 5000.00),
('Omar', 'Farooq', 'omar.f@example.com', 'Alexandria', 'Egypt', '2024-02-10', 3500.00),
('Sami', 'Haddad', 'sami.h@example.com', 'Beirut', 'Lebanon', '2024-02-28', 7500.00),
('Nour', 'El-Din', 'nour.e@example.com', 'Dubai', 'UAE', '2024-03-05', 12000.00),
('Fatima', 'Zahra', 'fatima.z@example.com', 'Casablanca', 'Morocco', '2024-03-20', 4500.00),
('Karim', 'Mansoor', 'karim.m@example.com', 'Riyadh', 'Saudi Arabia', '2024-04-01', 9000.00),
('Youssef', 'Ibrahim', 'youssef.i@example.com', 'Amman', 'Jordan', '2024-04-18', 6000.00),
('Hana', 'Salem', 'hana.s@example.com', 'Giza', 'Egypt', '2024-05-12', 4000.00);

DROP TABLE IF EXISTS customer_analytics_summary;
CREATE TABLE customer_analytics_summary (
    country VARCHAR(50) PRIMARY KEY,
    total_customers INT,
    total_credit_limit DECIMAL(12,2),
    avg_credit_limit DECIMAL(10,2)
);
