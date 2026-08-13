#!/bin/bash
# Test Hadoop cluster HDFS and MapReduce execution

set -e

run_hduser() {
    su - hduser -c "
        export JAVA_HOME=/usr/local/java
        export HADOOP_HOME=/usr/local/hadoop
        export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
        export HADOOP_MAPRED_HOME=/usr/local/hadoop
        export HADOOP_COMMON_HOME=/usr/local/hadoop
        export HADOOP_HDFS_HOME=/usr/local/hadoop
        export YARN_HOME=/usr/local/hadoop
        export PATH=\$PATH:\$JAVA_HOME/bin:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin
        export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native
        export HADOOP_OPTS=\"-Djava.library.path=\$HADOOP_HOME/lib\"
        $*
    "
}

echo "=== 1. Checking running Java daemons (jps) ==="
run_hduser "jps"

echo ""
echo "=== 2. Testing HDFS file system operations ==="
run_hduser "hdfs dfs -mkdir -p /test/input"
run_hduser "hdfs dfs -put /usr/local/hadoop/etc/hadoop/core-site.xml /test/input/"
run_hduser "hdfs dfs -ls /test/input"
run_hduser "hdfs dfs -cat /test/input/core-site.xml | head -n 10"

echo ""
echo "=== 3. Testing MapReduce Pi Example ==="
run_hduser "yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 2 5"

echo ""
echo "=== 4. Cleaning test files in HDFS ==="
run_hduser "hdfs dfs -rm -r /test"

echo ""
echo "=========================================================="
echo "ALL TESTS PASSED SUCCESSFULLY!"
echo "=========================================================="

