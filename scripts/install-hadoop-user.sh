#!/usr/bin/env bash
# ==============================================================================
# Apache Hadoop Single-Node Cluster User-Space Installer (Zero sudo required)
# Installs directly to ~/hadoop with high performance JVM tuning
# ==============================================================================
set -euo pipefail

echo "================================================================="
echo "  🐘 Apache Hadoop Automated User-Space Installer               "
echo "================================================================="

cd ~

echo "--> [1/5] Configuring Passwordless SSH..."
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

echo "--> [2/5] Downloading Apache Hadoop 3.3.6..."
HADOOP_VERSION="3.3.6"
HADOOP_TAR="hadoop-${HADOOP_VERSION}.tar.gz"

if [ ! -d "$HOME/hadoop" ]; then
    if [ ! -f "/tmp/${HADOOP_TAR}" ]; then
        echo "Downloading ${HADOOP_TAR}..."
        wget -c "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}" || \
        wget -c "https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}"
    fi
    echo "Extracting Hadoop to $HOME/hadoop..."
    tar -xzf "/tmp/${HADOOP_TAR}" -C "$HOME"
    mv "$HOME/hadoop-${HADOOP_VERSION}" "$HOME/hadoop"
fi

echo "--> [3/5] Setting up Environment Variables & JVM Memory Optimizations..."
JAVA_DETECTED_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")
HADOOP_DIR="$HOME/hadoop"

if ! grep -q "HADOOP_HOME=\$HOME/hadoop" ~/.bashrc 2>/dev/null; then
cat <<EOT >> ~/.bashrc

# --- Apache Hadoop Environment Variables ---
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

# Configure hadoop-env.sh
sed -i "s|# export JAVA_HOME=.*|export JAVA_HOME=${JAVA_DETECTED_HOME}|g" "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"
if ! grep -q "export JAVA_HOME=${JAVA_DETECTED_HOME}" "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"; then
    echo "export JAVA_HOME=${JAVA_DETECTED_HOME}" >> "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"
fi
echo "export HADOOP_HEAPSIZE_MAX=1024m" >> "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"
echo "export HADOOP_NAMENODE_OPTS=\"-Xms512m -Xmx1024m\"" >> "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"
echo "export HADOOP_DATANODE_OPTS=\"-Xms256m -Xmx512m\"" >> "$HADOOP_DIR/etc/hadoop/hadoop-env.sh"

echo "--> [4/5] Generating Cluster Configuration XMLs..."
mkdir -p "$HOME/hadoopdata/hdfs/namenode"
mkdir -p "$HOME/hadoopdata/hdfs/datanode"

cat <<EOT > "$HADOOP_DIR/etc/hadoop/core-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOT

cat <<EOT > "$HADOOP_DIR/etc/hadoop/hdfs-site.xml"
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

cat <<EOT > "$HADOOP_DIR/etc/hadoop/mapred-site.xml"
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

cat <<EOT > "$HADOOP_DIR/etc/hadoop/yarn-site.xml"
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

echo "--> [5/5] Formatting HDFS NameNode and Starting Daemons..."
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=$HOME/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

hdfs namenode -format -force
start-dfs.sh
start-yarn.sh

echo "================================================================="
echo "  🎉 Hadoop Single-Node Cluster Started Successfully!            "
echo "================================================================="
echo "Active Java Daemons (jps):"
jps

echo ""
echo "Web Interfaces:"
echo "  - HDFS NameNode UI:        http://localhost:9870"
echo "  - YARN ResourceManager UI: http://localhost:8088"
echo "  - HDFS DataNode UI:        http://localhost:9864"
echo "================================================================="
