#!/bin/bash
# Script to run Python Streaming WordCount on Hadoop Docker cluster

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar"

echo "=== 1. Preparing HDFS directories ==="
docker compose exec -T hadoop hdfs dfs -mkdir -p /example/python/input
docker compose exec -T hadoop hdfs dfs -rm -r -f /example/python/output

echo "=== 2. Copying files to container & HDFS ==="
docker compose cp "${SCRIPT_DIR}/mapper.py" hadoop:/tmp/mapper.py
docker compose cp "${SCRIPT_DIR}/reducer.py" hadoop:/tmp/reducer.py
docker compose cp "${SCRIPT_DIR}/sample.txt" hadoop:/tmp/sample.txt

docker compose exec -T hadoop chmod +x /tmp/mapper.py /tmp/reducer.py
docker compose exec -T hadoop hdfs dfs -put -f /tmp/sample.txt /example/python/input/

echo "=== 3. Executing Hadoop Streaming MapReduce Job ==="
docker compose exec -T hadoop hadoop jar "$STREAMING_JAR" \
    -files /tmp/mapper.py,/tmp/reducer.py \
    -mapper "python3 /tmp/mapper.py" \
    -reducer "python3 /tmp/reducer.py" \
    -input /example/python/input/sample.txt \
    -output /example/python/output

echo "=== 4. Displaying Results from HDFS ==="
docker compose exec -T hadoop hdfs dfs -cat /example/python/output/part-00000

echo "=== Python MapReduce Job Finished Successfully ==="
