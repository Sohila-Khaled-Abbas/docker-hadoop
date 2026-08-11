#!/bin/bash
# Healthcheck script for Docker to verify Hadoop daemons and HTTP endpoints

set -e

# Check NameNode Web UI port (9870)
curl -f -s http://localhost:9870 > /dev/null || exit 1

# Check ResourceManager Web UI port (8088)
curl -f -s http://localhost:8088 > /dev/null || exit 1

# Check HDFS basic command response
su - hduser -c "export JAVA_HOME=/usr/local/java; export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$JAVA_HOME/bin:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; hdfs dfsadmin -report" > /dev/null || exit 1

exit 0

