#!/bin/bash
# Test Hadoop cluster HDFS and MapReduce execution

set -e

echo "=== 1. Checking running Java daemons (jps) ==="
su - hduser -c "jps"

echo ""
echo "=== 2. Testing HDFS file system operations ==="
su - hduser -c "hdfs dfs -mkdir -p /test/input"
su - hduser -c "hdfs dfs -put /usr/local/hadoop/etc/hadoop/core-site.xml /test/input/"
su - hduser -c "hdfs dfs -ls /test/input"
su - hduser -c "hdfs dfs -cat /test/input/core-site.xml | head -n 10"

echo ""
echo "=== 3. Testing MapReduce Pi Example ==="
su - hduser -c "yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 2 5"

echo ""
echo "=== 4. Cleaning test files in HDFS ==="
su - hduser -c "hdfs dfs -rm -r /test"

echo ""
echo "=========================================================="
echo "ALL TESTS PASSED SUCCESSFULLY!"
echo "=========================================================="
