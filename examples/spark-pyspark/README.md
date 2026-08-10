# Apache Spark & PySpark HDFS Integration

This example demonstrates how to use Apache Spark / PySpark from your host machine or another container to read and write data directly into the containerized HDFS storage layer via `hdfs://localhost:9000`.

---

## 📋 Prerequisites

Install PySpark locally:
```bash
pip install pyspark
```

Ensure your Hadoop cluster is running:
```bash
docker compose ps
```

---

## 🚀 Running the Example

Run the Python script:
```bash
python examples/spark-pyspark/pyspark_hdfs_read_write.py
```

Verify that the Parquet dataset was created in HDFS:
```bash
docker compose exec hadoop hdfs dfs -ls -R /data/spark_employees.parquet
```
