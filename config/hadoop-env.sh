#!/bin/bash
# Set Java installation path
export JAVA_HOME=/usr/local/java

# Set Hadoop installation paths
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop

# Java options and native libraries
export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true -Djava.library.path=/usr/local/hadoop/lib/native"
export HADOOP_HOME_WARN_SUPPRESS="TRUE"
export HADOOP_ROOT_LOGGER="WARN,DRFA"

# Hadoop Daemon execution users (running as non-root hduser)
export HDFS_NAMENODE_USER="hduser"
export HDFS_DATANODE_USER="hduser"
export HDFS_SECONDARYNAMENODE_USER="hduser"
export YARN_RESOURCEMANAGER_USER="hduser"
export YARN_NODEMANAGER_USER="hduser"
