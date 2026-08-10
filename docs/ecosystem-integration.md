# Big Data Ecosystem Integration Guide

This guide describes how to connect external data processing frameworks, engines, and notebooks to this containerized Apache Hadoop 3.1.2 cluster.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Apache Spark & PySpark](#apache-spark--pyspark)
- [Apache Hive](#apache-hive)
- [Presto / Trino Query Engine](#presto--trino-query-engine)
- [Jupyter Notebook & Python Clients](#jupyter-notebook--python-clients)

---

## 🌐 Overview

Because this container publishes standard Hadoop HDFS RPC (`:9000`) and Web UIs on the host, any external framework running locally or on other Docker containers can interact with HDFS and YARN.

```text
+-------------------+       HDFS RPC (hdfs://localhost:9000)       +---------------------+
|   Apache Spark    | -------------------------------------------> |                     |
+-------------------+                                              |                     |
|   Apache Hive     | ------> HDFS Warehouse (/user/hive/warehouse)  |  Hadoop Container   |
+-------------------+                                              |    (HDFS + YARN)    |
|   Presto / Trino  | -------------------------------------------> |                     |
+-------------------+                                              |                     |
|  Jupyter Notebook | ------> WebHDFS REST API (http://localhost:9870) |                 |
+-------------------+                                              +---------------------+
```

---

## ⚡ Apache Spark & PySpark

You can read and write datasets directly from/to HDFS using PySpark on your host machine or in separate containers.

### PySpark Connection Example:

```python
from pyspark.sql import SparkSession

# Initialize Spark session with HDFS defaultFS
spark = SparkSession.builder \
    .appName("HadoopDockerIntegration") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    .getOrCreate()

# Create a sample DataFrame
data = [("Alice", 34, "Engineering"), ("Bob", 45, "Marketing"), ("Charlie", 29, "Data Science")]
df = spark.createDataFrame(data, ["name", "age", "department"])

# Write DataFrame to HDFS as Parquet
df.write.mode("overwrite").parquet("hdfs://localhost:9000/data/employees.parquet")

# Read Parquet from HDFS
read_df = spark.read.parquet("hdfs://localhost:9000/data/employees.parquet")
read_df.show()

spark.stop()
```

---

## 🐝 Apache Hive

To connect Apache Hive to this Hadoop cluster:

1. **Create HDFS Warehouse Directories**:
   ```bash
   docker compose exec hadoop hdfs dfs -mkdir -p /tmp /user/hive/warehouse
   docker compose exec hadoop hdfs dfs -chmod -R 1777 /tmp
   docker compose exec hadoop hdfs dfs -chmod -R 777 /user/hive/warehouse
   ```

2. **Configure `hive-site.xml`**:
   ```xml
   <configuration>
       <property>
           <name>fs.defaultFS</name>
           <value>hdfs://localhost:9000</value>
       </property>
       <property>
           <name>hive.metastore.warehouse.dir</name>
           <value>/user/hive/warehouse</value>
       </property>
   </configuration>
   ```

---

## 🚀 Presto / Trino Query Engine

To query HDFS tables using Presto or Trino, configure the Hive connector catalog:

`etc/catalog/hive.properties`:
```properties
connector.name=hive
hive.metastore.uri=thrift://localhost:9083
hive.config.resources=/path/to/core-site.xml,/path/to/hdfs-site.xml
```

---

## 📓 Jupyter Notebook & Python (`hdfs` library)

You can interact with HDFS via WebHDFS or the Python `hdfs` library:

```python
import hdfs

# Connect to NameNode WebHDFS endpoint
client = hdfs.InsecureClient('http://localhost:9870', user='hduser')

# List files
print(client.list('/'))

# Upload a local file
client.upload('/user/mydata/sample.csv', './sample.csv', overwrite=True)

# Read file directly into Pandas
import pandas as pd
with client.read('/user/mydata/sample.csv', encoding='utf-8') as reader:
    df = pd.read_csv(reader)
    print(df.head())
```
