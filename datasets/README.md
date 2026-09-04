# 📊 Sample Datasets

This directory provides pre-packaged sample datasets for testing HDFS distributed storage, MapReduce jobs, Apache Spark pipelines, and SQL analytical engines.

---

## 📁 Available Datasets

| Filename | Format | Description | Target Use Case |
| :--- | :--- | :--- | :--- |
| [`wordcount-sample.txt`](wordcount-sample.txt) | Plain Text | Text corpus explaining Apache Hadoop architecture | Java & Python MapReduce WordCount, text frequency analysis |
| [`employees.csv`](employees.csv) | CSV (Headered) | Tabular employee records (`id`, `name`, `department`, `salary`, `city`, `hire_date`) | PySpark DataFrame operations, aggregations, Hive external tables |

---

## 🚀 Quick Recipes: Loading Datasets into HDFS

### 1. Ingest via Docker Container Shell

```bash
# Enter container shell
docker compose exec -it hadoop bash

# Create target directories in HDFS
hdfs dfs -mkdir -p /user/datasets/text
hdfs dfs -mkdir -p /user/datasets/tabular

# Upload files from host/container mount into HDFS
# (Assuming files copied or mounted to /tmp/datasets)
hdfs dfs -put /tmp/datasets/wordcount-sample.txt /user/datasets/text/
hdfs dfs -put /tmp/datasets/employees.csv /user/datasets/tabular/

# Verify upload
hdfs dfs -ls -R /user/datasets
```

### 2. Copy Directly from Host Machine into Running Container and HDFS

```bash
# Copy from host machine to container's /tmp directory
docker cp datasets/wordcount-sample.txt hadoop-master:/tmp/
docker cp datasets/employees.csv hadoop-master:/tmp/

# Load into HDFS
docker compose exec hadoop hdfs dfs -mkdir -p /datasets
docker compose exec hadoop hdfs dfs -put -f /tmp/wordcount-sample.txt /datasets/
docker compose exec hadoop hdfs dfs -put -f /tmp/employees.csv /datasets/

# Inspect HDFS content
docker compose exec hadoop hdfs dfs -cat /datasets/employees.csv
```

### 3. Run MapReduce WordCount on Sample Dataset

```bash
docker compose exec hadoop hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar wordcount /datasets/wordcount-sample.txt /datasets/wordcount-output

# Inspect results
docker compose exec hadoop hdfs dfs -cat /datasets/wordcount-output/part-r-00000 | head -n 25
```
