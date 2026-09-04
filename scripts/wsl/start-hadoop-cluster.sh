#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/home/hadoopuser/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export PATH=$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$JAVA_HOME/bin:/usr/local/bin:/usr/bin:/bin
export PDSH_RCMD_TYPE=ssh

echo "--> Starting HDFS daemons..."
$HADOOP_HOME/sbin/start-dfs.sh

echo "--> Starting YARN ResourceManager..."
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

echo "--> Starting YARN NodeManager..."
$HADOOP_HOME/bin/yarn --daemon start nodemanager

echo "--> Starting MapReduce JobHistory Server..."
$HADOOP_HOME/bin/mapred --daemon start historyserver

echo ""
echo "--> Active Java Daemons:"
$JAVA_HOME/bin/jps
