#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/home/hadoopuser/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:/usr/local/bin:/usr/bin:/bin

echo "--> Starting Hadoop daemons directly (zero SSH dependency)..."

$HADOOP_HOME/bin/hdfs --daemon start namenode
$HADOOP_HOME/bin/hdfs --daemon start datanode
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
$HADOOP_HOME/bin/yarn --daemon start resourcemanager
$HADOOP_HOME/bin/yarn --daemon start nodemanager
$HADOOP_HOME/bin/mapred --daemon start historyserver

sleep 2
echo "--> Active Java Daemons:"
jps
