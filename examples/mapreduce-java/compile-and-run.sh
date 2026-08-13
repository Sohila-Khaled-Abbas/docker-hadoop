#!/bin/bash
# Script to compile and run Java MapReduce WordCount on Hadoop Docker cluster

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== 1. Copying Java source file into container ==="
docker compose cp "${SCRIPT_DIR}/WordCount.java" hadoop:/tmp/WordCount.java

echo "=== 2. Compiling Java MapReduce code against Hadoop classpath ==="
docker compose exec -T hadoop bash -c "
    mkdir -p /tmp/wordcount_classes
    javac -classpath \$(hadoop classpath) -d /tmp/wordcount_classes /tmp/WordCount.java
    jar -cvf /tmp/wordcount.jar -C /tmp/wordcount_classes .
"

echo "=== 3. Preparing HDFS input directories ==="
docker compose exec -T hadoop hdfs dfs -mkdir -p /example/java/input
docker compose exec -T hadoop hdfs dfs -rm -r -f /example/java/output
docker compose exec -T hadoop hdfs dfs -put -f /usr/local/hadoop/etc/hadoop/*.xml /example/java/input/

echo "=== 4. Running YARN MapReduce Job ==="
docker compose exec -T hadoop yarn jar /tmp/wordcount.jar WordCount /example/java/input /example/java/output

echo "=== 5. Reading Output from HDFS ==="
docker compose exec -T hadoop hdfs dfs -cat /example/java/output/part-r-00000 | head -n 30

echo "=== Java MapReduce Job Completed Successfully ==="
