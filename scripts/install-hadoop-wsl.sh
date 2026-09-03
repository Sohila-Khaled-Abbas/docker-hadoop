#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop 3.3.6 Automated Installer for Ubuntu 24.04 on WSL 2
# With OpenJDK 11 LTS, Optimized JVM Heap, and GUI Desktop/App Support
# ==============================================================================
set -euo pipefail

echo "================================================================="
echo "  🐘 Apache Hadoop & GUI Automated Setup for WSL 2 (Ubuntu 24.04) "
echo "================================================================="

# 1. Update and install prerequisites
echo "--> [1/6] Updating packages and installing OpenJDK LTS & Utilities..."
sudo apt-get update -y
sudo apt-get install -y \
    openjdk-11-jdk-headless \
    openssh-server \
    openssh-client \
    curl \
    wget \
    rsync \
    tar \
    pdsh \
    net-tools \
    xfce4-terminal \
    dbus-x11

# Optional: lightweight GUI desktop tools for WSLg
sudo apt-get install -y --no-install-recommends \
    nautilus \
    gedit || true

# 2. Configure Passwordless SSH Loopback
echo "--> [2/6] Configuring Passwordless SSH loopback..."
sudo systemctl enable --now ssh 2>/dev/null || sudo service ssh start

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

export PDSH_RCMD_TYPE=ssh
if ! grep -q "PDSH_RCMD_TYPE=ssh" ~/.bashrc 2>/dev/null; then
    echo "export PDSH_RCMD_TYPE=ssh" >> ~/.bashrc
fi

# 3. Download and Install Apache Hadoop 3.3.6
echo "--> [3/6] Installing Apache Hadoop 3.3.6..."
HADOOP_VERSION="3.3.6"
HADOOP_TAR="hadoop-${HADOOP_VERSION}.tar.gz"
HADOOP_INSTALL_DIR="$HOME/hadoop"

if [ ! -d "$HADOOP_INSTALL_DIR" ]; then
    if [ ! -f "/tmp/${HADOOP_TAR}" ]; then
        echo "Downloading Apache Hadoop ${HADOOP_VERSION}..."
        wget -q --show-progress -c "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}" || \
        wget -q --show-progress -c "https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}"
    fi
    echo "Extracting Hadoop to $HADOOP_INSTALL_DIR..."
    tar -xzf "/tmp/${HADOOP_TAR}" -C "$HOME"
    mv "$HOME/hadoop-${HADOOP_VERSION}" "$HADOOP_INSTALL_DIR"
fi

# 4. Set Environment Variables
echo "--> [4/6] Configuring Environment Profiles & JVM Memory Tuning..."
JAVA_DETECTED_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

if ! grep -q "HADOOP_HOME=\$HOME/hadoop" ~/.bashrc 2>/dev/null; then
cat <<EOT >> ~/.bashrc

# --- Apache Hadoop Environment Variables (WSL 2) ---
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=\$HOME/hadoop
export HADOOP_INSTALL=\$HADOOP_HOME
export HADOOP_MAPRED_HOME=\$HADOOP_HOME
export HADOOP_COMMON_HOME=\$HADOOP_HOME
export HADOOP_HDFS_HOME=\$HADOOP_HOME
export YARN_HOME=\$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=\$HADOOP_HOME/lib/native"
export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin:\$JAVA_HOME/bin
export PDSH_RCMD_TYPE=ssh
EOT
fi

# Configure hadoop-env.sh for optimal memory performance on WSL
sed -i "s|# export JAVA_HOME=.*|export JAVA_HOME=${JAVA_DETECTED_HOME}|g" "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"
if ! grep -q "export JAVA_HOME=${JAVA_DETECTED_HOME}" "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"; then
    echo "export JAVA_HOME=${JAVA_DETECTED_HOME}" >> "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"
fi
echo "export HADOOP_HEAPSIZE_MAX=1024m" >> "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"
echo "export HADOOP_NAMENODE_OPTS=\"-Xms512m -Xmx1024m\"" >> "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"
echo "export HADOOP_DATANODE_OPTS=\"-Xms256m -Xmx512m\"" >> "$HADOOP_INSTALL_DIR/etc/hadoop/hadoop-env.sh"

# 5. Generate Cluster Configuration XMLs
echo "--> [5/6] Generating Cluster XML Configurations..."
mkdir -p "$HOME/hadoopdata/hdfs/namenode"
mkdir -p "$HOME/hadoopdata/hdfs/datanode"

# core-site.xml
cat <<EOT > "$HADOOP_INSTALL_DIR/etc/hadoop/core-site.xml"
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
cat <<EOT > "$HADOOP_INSTALL_DIR/etc/hadoop/hdfs-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file://${HOME}/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file://${HOME}/hadoopdata/hdfs/datanode</value>
    </property>
</configuration>
EOT

# mapred-site.xml
cat <<EOT > "$HADOOP_INSTALL_DIR/etc/hadoop/mapred-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=${HOME}/hadoop</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=${HOME}/hadoop</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=${HOME}/hadoop</value>
    </property>
</configuration>
EOT

# yarn-site.xml
cat <<EOT > "$HADOOP_INSTALL_DIR/etc/hadoop/yarn-site.xml"
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
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
    <property>
        <name>yarn.nodemanager.pmem-check-enabled</name>
        <value>false</value>
    </property>
</configuration>
EOT

# 6. Format HDFS NameNode and Start Daemons
echo "--> [6/6] Formatting HDFS NameNode and Launching Cluster..."
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=$HOME/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

hdfs namenode -format -force
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver 2>/dev/null || true

echo "================================================================="
echo "  🎉 Hadoop Single-Node Cluster is Running Successfully on WSL 2!"
echo "================================================================="
echo "Active Java Daemons (jps):"
jps

echo ""
echo "Web Interfaces (Instant Localhost Access in Windows):"
echo "  - HDFS NameNode UI:        http://localhost:9870"
echo "  - YARN ResourceManager UI: http://localhost:8088"
echo "  - HDFS DataNode UI:        http://localhost:9864"
echo "  - MapReduce JobHistory UI: http://localhost:19888"
echo "================================================================="
