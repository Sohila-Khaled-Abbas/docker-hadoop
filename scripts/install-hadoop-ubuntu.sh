#!/usr/bin/env bash
# ==============================================================================
# Automated Apache Hadoop Single-Node Cluster Installer on Ubuntu
# Compatible with Ubuntu 20.04 / 22.04 / 24.04 / 26.04
# ==============================================================================
set -euo pipefail

echo "================================================================="
echo "  🐘 Apache Hadoop Automated Ubuntu Installer                    "
echo "================================================================="

echo "--> [1/7] Updating apt repositories and installing prerequisites..."
sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk-headless openssh-server openssh-client curl wget rsync tar pdsh

echo "--> [2/7] Configuring passwordless SSH for local node..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa -q
fi
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
ssh-keyscan -H localhost >> ~/.ssh/known_hosts 2>/dev/null || true
ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts 2>/dev/null || true
ssh-keyscan -H 127.0.0.1 >> ~/.ssh/known_hosts 2>/dev/null || true

# Set PDSH RCMD type to ssh
if ! grep -q "PDSH_RCMD_TYPE=ssh" ~/.bashrc 2>/dev/null; then
    echo "export PDSH_RCMD_TYPE=ssh" >> ~/.bashrc
fi
export PDSH_RCMD_TYPE=ssh

echo "--> [3/7] Downloading and installing Apache Hadoop..."
HADOOP_VERSION="3.3.6"
HADOOP_TAR="hadoop-${HADOOP_VERSION}.tar.gz"

if [ ! -d "/usr/local/hadoop" ]; then
    if [ ! -f "/tmp/${HADOOP_TAR}" ]; then
        echo "Downloading Apache Hadoop ${HADOOP_VERSION}..."
        wget -q --show-progress -c "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}" || \
        wget -q --show-progress -c "https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}"
    fi
    echo "Extracting Hadoop to /usr/local/hadoop..."
    sudo tar -xzf "/tmp/${HADOOP_TAR}" -C /usr/local/
    sudo mv "/usr/local/hadoop-${HADOOP_VERSION}" /usr/local/hadoop
    sudo chown -R "$(whoami):$(whoami)" /usr/local/hadoop
fi

echo "--> [4/7] Setting up Environment Variables..."
JAVA_DETECTED_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

if ! grep -q "HADOOP_HOME=/usr/local/hadoop" ~/.bashrc 2>/dev/null; then
cat <<EOT >> ~/.bashrc

# --- Apache Hadoop Environment Variables ---
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=\$HADOOP_HOME
export HADOOP_MAPRED_HOME=\$HADOOP_HOME
export HADOOP_COMMON_HOME=\$HADOOP_HOME
export HADOOP_HDFS_HOME=\$HADOOP_HOME
export YARN_HOME=\$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native
export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin:\$JAVA_HOME/bin
EOT
fi

# Configure hadoop-env.sh
sed -i "s|# export JAVA_HOME=.*|export JAVA_HOME=${JAVA_DETECTED_HOME}|g" /usr/local/hadoop/etc/hadoop/hadoop-env.sh
if ! grep -q "export JAVA_HOME=${JAVA_DETECTED_HOME}" /usr/local/hadoop/etc/hadoop/hadoop-env.sh; then
    echo "export JAVA_HOME=${JAVA_DETECTED_HOME}" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
fi

echo "--> [5/7] Creating HDFS Directories and Cluster Config XMLs..."
mkdir -p "/home/$(whoami)/hadoopdata/hdfs/namenode"
mkdir -p "/home/$(whoami)/hadoopdata/hdfs/datanode"

# core-site.xml
cat <<EOT > /usr/local/hadoop/etc/hadoop/core-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOT

# hdfs-site.xml
cat <<EOT > /usr/local/hadoop/etc/hadoop/hdfs-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/$(whoami)/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/$(whoami)/hadoopdata/hdfs/datanode</value>
    </property>
</configuration>
EOT

# mapred-site.xml
cat <<EOT > /usr/local/hadoop/etc/hadoop/mapred-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
</configuration>
EOT

# yarn-site.xml
cat <<EOT > /usr/local/hadoop/etc/hadoop/yarn-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
</configuration>
EOT

echo "--> [6/7] Formatting HDFS NameNode..."
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
hdfs namenode -format -force

echo "--> [7/7] Launching HDFS (DFS) and YARN Daemons..."
start-dfs.sh
start-yarn.sh

echo "================================================================="
echo "  🎉 Hadoop Single-Node Cluster Started Successfully!            "
echo "================================================================="
echo "Active Java Daemons (jps):"
jps

echo ""
echo "Web Interfaces Available at:"
echo "  - HDFS NameNode UI:        http://localhost:9870"
echo "  - YARN ResourceManager UI: http://localhost:8088"
echo "  - HDFS DataNode UI:        http://localhost:9864"
echo "================================================================="
