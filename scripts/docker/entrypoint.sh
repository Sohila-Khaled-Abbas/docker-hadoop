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

# 1. Ensure volume permissions for hduser
mkdir -p /usr/local/hadoop/yarn_data/hdfs/namenode /usr/local/hadoop/yarn_data/hdfs/datanode /app/hadoop/tmp /usr/local/hadoop/logs /spark-logs
chown -R hduser:hadoop /usr/local/hadoop/yarn_data /app/hadoop/tmp /usr/local/hadoop/logs /spark-logs
chmod -R 755 /usr/local/hadoop/yarn_data

# 2. Configure SSHD & client for fast local container connections without banner exchange delays
sed -i 's/#*UseDNS .*/UseDNS no/' /etc/ssh/sshd_config 2>/dev/null || echo "UseDNS no" >> /etc/ssh/sshd_config
sed -i 's/#*GSSAPIAuthentication .*/GSSAPIAuthentication no/' /etc/ssh/sshd_config 2>/dev/null || echo "GSSAPIAuthentication no" >> /etc/ssh/sshd_config
sed -i 's/#*AddressFamily .*/AddressFamily inet/' /etc/ssh/sshd_config 2>/dev/null || echo "AddressFamily inet" >> /etc/ssh/sshd_config
grep -q "UseDNS no" /etc/ssh/sshd_config || echo "UseDNS no" >> /etc/ssh/sshd_config
grep -q "MaxStartups 100:30:200" /etc/ssh/sshd_config || echo "MaxStartups 100:30:200" >> /etc/ssh/sshd_config

mkdir -p /etc/ssh/ssh_config.d /home/hduser/.ssh /root/.ssh
echo "Host *" >> /etc/ssh/ssh_config
echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config
echo "    LogLevel ERROR" >> /etc/ssh/ssh_config
echo "    ConnectTimeout 5" >> /etc/ssh/ssh_config
echo "    AddressFamily inet" >> /etc/ssh/ssh_config

echo "[1/6] Starting SSH daemon..."
service ssh restart

# 3. Ensure hduser SSH keys exist and permissions are correct
run_hduser "
if [ ! -f ~/.ssh/id_rsa ]; then
    echo 'Generating SSH keys for hduser...'
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    chmod 0600 ~/.ssh/authorized_keys
    chmod 0700 ~/.ssh
fi
"

# 4. Format NameNode if not formatted yet
if [ ! -d "/usr/local/hadoop/yarn_data/hdfs/namenode/current" ]; then
    echo "[2/6] Formatting Hadoop NameNode..."
    run_hduser "hdfs namenode -format -force -nonInteractive"
else
    echo "[2/6] NameNode already formatted. Skipping format."
fi

# 5. Start HDFS daemons directly (NameNode, DataNode, SecondaryNameNode)
echo "[3/6] Starting HDFS daemons (NameNode, DataNode, SecondaryNameNode)..."
run_hduser "hdfs --daemon start namenode"
run_hduser "hdfs --daemon start datanode"
run_hduser "hdfs --daemon start secondarynamenode"

# 6. Start YARN daemons directly (ResourceManager, NodeManager)
echo "[4/6] Starting YARN daemons (ResourceManager, NodeManager)..."
run_hduser "yarn --daemon start resourcemanager"
run_hduser "yarn --daemon start nodemanager"

# 7. Start MapReduce JobHistory Server
echo "[5/6] Starting MapReduce JobHistory Server..."
run_hduser "mapred --daemon start historyserver" || true

# 8. Initialize HDFS directories
echo "[6/6] Initializing default HDFS directories for Hadoop, Spark & Hive..."
run_hduser "hdfs dfsadmin -safemode wait" || true
run_hduser "
hdfs dfs -mkdir -p /tmp /user /user/hduser /user/hadoop /spark-logs /user/hive/warehouse /data /datasets
hdfs dfs -chmod -R 1777 /tmp /spark-logs /user/hive/warehouse
hdfs dfs -chmod -R 777 /user /data /datasets
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

