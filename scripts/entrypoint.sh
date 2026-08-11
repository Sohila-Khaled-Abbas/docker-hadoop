#!/bin/bash
set -e

echo "=========================================================="
echo "Starting Apache Hadoop 3.1.2 Single-Node Container"
echo "=========================================================="

export JAVA_HOME=/usr/local/java
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
export HADOOP_MAPRED_HOME=/usr/local/hadoop
export HADOOP_COMMON_HOME=/usr/local/hadoop
export HADOOP_HDFS_HOME=/usr/local/hadoop
export YARN_HOME=/usr/local/hadoop
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"

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

# 1. Start SSH daemon
echo "[1/6] Starting SSH daemon..."
service ssh start

# 2. Ensure hduser SSH keys exist and permissions are correct
run_hduser "
if [ ! -f ~/.ssh/id_rsa ]; then
    echo 'Generating SSH keys for hduser...'
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    chmod 0600 ~/.ssh/authorized_keys
    chmod 0700 ~/.ssh
fi
"

# 3. Format NameNode if not formatted yet
if [ ! -d "/usr/local/hadoop/yarn_data/hdfs/namenode/current" ]; then
    echo "[2/6] Formatting Hadoop NameNode..."
    run_hduser "hdfs namenode -format -force"
else
    echo "[2/6] NameNode already formatted. Skipping format."
fi

# 4. Start HDFS daemons (NameNode, DataNode, SecondaryNameNode)
echo "[3/6] Starting HDFS daemons (NameNode, DataNode, SecondaryNameNode)..."
run_hduser "start-dfs.sh"

# 5. Start YARN daemons (ResourceManager, NodeManager)
echo "[4/6] Starting YARN daemons (ResourceManager, NodeManager)..."
run_hduser "start-yarn.sh"

# 6. Start MapReduce JobHistory Server
echo "[5/6] Starting MapReduce JobHistory Server..."
run_hduser "mapred --daemon start historyserver" || true

# 7. Initialize HDFS directories
echo "[6/6] Initializing default HDFS directories..."
run_hduser "hdfs dfsadmin -safemode wait" || true
run_hduser "
hdfs dfs -mkdir -p /tmp /user /user/hduser /user/hadoop
hdfs dfs -chmod -R 1777 /tmp
hdfs dfs -chmod -R 777 /user
" || true

echo "=========================================================="
echo "Hadoop Cluster Started Successfully!"
echo "Running Java Processes:"
run_hduser "jps"
echo "=========================================================="
echo "Web Interfaces Available:"
echo "  - HDFS NameNode UI:          http://localhost:9870"
echo "  - HDFS DataNode UI:          http://localhost:9864"
echo "  - YARN ResourceManager UI:   http://localhost:8088"
echo "  - YARN NodeManager UI:       http://localhost:8042"
echo "  - MapReduce JobHistory UI:   http://localhost:19888"
echo "=========================================================="

if [ "$#" -gt 0 ]; then
    exec "$@"
else
    # Stream logs to stdout
    mkdir -p /usr/local/hadoop/logs
    touch /usr/local/hadoop/logs/hadoop-hduser-namenode.log
    tail -F /usr/local/hadoop/logs/*.log
fi

