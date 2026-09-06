# ==============================================================================
# 📊 Apache HBase — Columnar NoSQL Schema & Shell Commands
# ==============================================================================

# 1. Create Table with Two Column Families: personal_data and financial_data
create 'retail_customers', {NAME => 'personal', VERSIONS => 3}, {NAME => 'financial', COMPRESSION => 'SNAPPY'}

# 2. Insert Sample Records (RowKey, ColumnFamily:ColumnQualifier, Value)
put 'retail_customers', 'usr_101', 'personal:name', 'Layla Mahmoud'
put 'retail_customers', 'usr_101', 'personal:city', 'Cairo'
put 'retail_customers', 'usr_101', 'personal:country', 'Egypt'
put 'retail_customers', 'usr_101', 'financial:credit_limit', '5000.00'
put 'retail_customers', 'usr_101', 'financial:tier', 'GOLD'

put 'retail_customers', 'usr_102', 'personal:name', 'Omar Farooq'
put 'retail_customers', 'usr_102', 'personal:city', 'Alexandria'
put 'retail_customers', 'usr_102', 'financial:credit_limit', '3500.00'
put 'retail_customers', 'usr_102', 'financial:tier', 'SILVER'

# 3. Retrieve Individual Row by Key
get 'retail_customers', 'usr_101'

# 4. Scan Table with Column Projection
scan 'retail_customers', {COLUMNS => ['personal:name', 'financial:tier'], LIMIT => 10}

# 5. Table Statistics and Row Count
count 'retail_customers'
