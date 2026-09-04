#!/usr/bin/env bash
# ==============================================================================
# Automated Apache Hadoop Single-Node Cluster Installer on Ubuntu
# Compatible with Ubuntu 20.04 / 22.04 / 24.04 / 26.04
# Tuned for High Performance & Low Latency on 5GB-8GB VMs
# ==============================================================================
set -euo pipefail

echo "================================================================="
echo "  🐘 Apache Hadoop Automated High-Performance Installer          "
echo "  ⚡ Engineered for Big Data Learning & Production Best Practices"
echo "================================================================="

echo "--> [1/8] Updating apt repositories and installing prerequisites..."
sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk-headless openssh-server openssh-client curl wget rsync tar pdsh libsnappy-dev build-essential

echo "--> [2/8] Applying Linux Kernel & OS Performance Tuning..."
# Disable aggressive swapping
if ! grep -q "vm.swappiness=1" /etc/sysctl.conf 2>/dev/null; then
    echo "vm.swappiness=1" | sudo tee -a /etc/sysctl.d/99-hadoop.conf > /dev/null
    sudo sysctl -p /etc/sysctl.d/99-hadoop.conf 2>/dev/null || true
fi

# Increase file descriptors and process limits
sudo tee /etc/security/limits.d/99-hadoop.conf > /dev/null <<EOT
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
EOT

# Disable Transparent Huge Pages (THP) for JVM stability
if [ -d /sys/kernel/mm/transparent_hugepage ]; then
    echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null || true
    echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/defrag 2>/dev/null || true
fi

echo "--> [3/8] Configuring passwordless SSH for local node..."
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

echo "--> [4/8] Downloading and installing Apache Hadoop..."
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

echo "--> [5/8] Setting up Environment Variables & G1GC JVM Heap Limits..."
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
export HADOOP_OPTS="-Djava.library.path=\$HADOOP_HOME/lib/native"
export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin:\$JAVA_HOME/bin
export PDSH_RCMD_TYPE=ssh
EOT
fi

# Configure hadoop-env.sh for optimal heap limits & G1GC low-pause garbage collector
sed -i "s|# export JAVA_HOME=.*|export JAVA_HOME=${JAVA_DETECTED_HOME}|g" /usr/local/hadoop/etc/hadoop/hadoop-env.sh
if ! grep -q "export JAVA_HOME=${JAVA_DETECTED_HOME}" /usr/local/hadoop/etc/hadoop/hadoop-env.sh; then
    echo "export JAVA_HOME=${JAVA_DETECTED_HOME}" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
fi

cat <<'EOT' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh

# High-Performance JVM Heap & G1GC Sizing
export HADOOP_HEAPSIZE_MAX=1024m
export HADOOP_NAMENODE_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"
export HADOOP_DATANODE_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"
export YARN_RESOURCEMANAGER_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"
export YARN_NODEMANAGER_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"
EOT

echo "--> [6/8] Generating Optimized Cluster XML Configurations..."
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
        <description>Default filesystem URI</description>
    </property>
    <property>
        <name>io.file.buffer.size</name>
        <value>65536</value>
        <description>64KB Stream I/O buffer for high throughput</description>
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
        <name>dfs.blocksize</name>
        <value>134217728</value>
        <description>128MB HDFS Block Size</description>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/$(whoami)/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/$(whoami)/hadoopdata/hdfs/datanode</value>
    </property>
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
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
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>1024</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx819m -XX:+UseG1GC</value>
    </property>
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx1638m -XX:+UseG1GC</value>
    </property>
</configuration>
EOT

# yarn-site.xml
cat <<EOT > /usr/local/hadoop/etc/hadoop/yarn-site.xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>3584</value>
        <description>Total memory (MB) allocated for YARN compute tasks</description>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>
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

echo "--> [7/8] Formatting HDFS NameNode..."
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
hdfs namenode -format -force

echo "--> [8/8] Launching HDFS, YARN & JobHistory Server..."
start-dfs.sh
start-yarn.sh
mapred --daemon start historyserver

echo "================================================================="
echo "  🎉 Hadoop High-Performance Cluster Started Successfully!       "
echo "================================================================="
echo "Active Java Daemons (jps):"
jps

echo ""
echo "Web Interfaces Available at:"
echo "  - HDFS NameNode UI:        http://localhost:9870"
echo "  - YARN ResourceManager UI: http://localhost:8088"
echo "  - YARN NodeManager UI:     http://localhost:8042"
echo "  - HDFS DataNode UI:        http://localhost:9864"
echo "  - MapReduce JobHistory UI: http://localhost:19888"
echo "================================================================="

