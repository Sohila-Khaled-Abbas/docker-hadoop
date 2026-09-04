#!/usr/bin/env bash
# ==============================================================================
# Script: install-hadoop-kali.sh
# Purpose: Automated Apache Hadoop Single-Node Cluster Installer for Kali Linux
# Environment: VMware Workstation / Debian Testing / Kali Rolling
# Tuned for: 6GB RAM VM, 4 vCPUs, OpenJDK 11, G1GC low-pause garbage collection
# ==============================================================================
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=================================================================${NC}"
echo -e "${CYAN}  🐘 Apache Hadoop Automated High-Performance Installer for Kali   ${NC}"
echo -e "${CYAN}  ⚡ Optimized for VMware Workstation & Big Data Engineering        ${NC}"
echo -e "${CYAN}=================================================================${NC}"

CURRENT_USER="$(whoami)"
USER_HOME="${HOME:-/home/${CURRENT_USER}}"

# Ensure non-root invocation with sudo privileges
if [ "${CURRENT_USER}" = "root" ]; then
    echo -e "${YELLOW}[WARNING] Running as root. Hadoop is best installed under a dedicated user (e.g., 'kali').${NC}"
fi

echo -e "${GREEN}--> [1/8] Updating apt package repositories & installing prerequisites...${NC}"
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
    libsnappy-dev \
    build-essential \
    net-tools

# Ensure SSH service is running and enabled on boot
sudo systemctl enable --now ssh || true

# Fix VMware X11 invisible mouse cursor bug (switch from hardware to software cursor)
sudo mkdir -p /etc/X11/xorg.conf.d
sudo tee /etc/X11/xorg.conf.d/20-vmware.conf > /dev/null << 'EOF'
Section "Device"
    Identifier "VMware SVGA"
    Driver "vmware"
    Option "HWCursor" "off"
EndSection
EOF

echo -e "${GREEN}--> [2/8] Applying Linux Kernel & Virtual Memory Hardening...${NC}"
# 1. Swappiness tuning (keep Hadoop JVMs in RAM, prevent paging out)
if ! grep -q "vm.swappiness=1" /etc/sysctl.conf 2>/dev/null; then
    echo "vm.swappiness=1" | sudo tee -a /etc/sysctl.d/99-hadoop.conf > /dev/null
    sudo sysctl -p /etc/sysctl.d/99-hadoop.conf 2>/dev/null || true
fi

# 2. File descriptors and process limits
sudo tee /etc/security/limits.d/99-hadoop.conf > /dev/null <<EOT
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
${CURRENT_USER} soft nofile 65536
${CURRENT_USER} hard nofile 65536
${CURRENT_USER} soft nproc 32768
${CURRENT_USER} hard nproc 32768
EOT

# 3. Disable Transparent Huge Pages (THP) for JVM stability
if [ -d /sys/kernel/mm/transparent_hugepage ]; then
    echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null || true
    echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/defrag 2>/dev/null || true
fi

echo -e "${GREEN}--> [3/8] Configuring passwordless SSH for local node...${NC}"
mkdir -p "${USER_HOME}/.ssh"
chmod 700 "${USER_HOME}/.ssh"

# Generate ed25519 key if not present (fallback to rsa if needed)
if [ ! -f "${USER_HOME}/.ssh/id_rsa" ] && [ ! -f "${USER_HOME}/.ssh/id_ed25519" ]; then
    ssh-keygen -t rsa -b 2048 -P "" -f "${USER_HOME}/.ssh/id_rsa" -q
fi

# Authorize keys
if [ -f "${USER_HOME}/.ssh/id_rsa.pub" ]; then
    cat "${USER_HOME}/.ssh/id_rsa.pub" >> "${USER_HOME}/.ssh/authorized_keys"
fi
if [ -f "${USER_HOME}/.ssh/id_ed25519.pub" ]; then
    cat "${USER_HOME}/.ssh/id_ed25519.pub" >> "${USER_HOME}/.ssh/authorized_keys"
fi

# Ensure unique entries and correct permissions
sort -u "${USER_HOME}/.ssh/authorized_keys" -o "${USER_HOME}/.ssh/authorized_keys"
chmod 600 "${USER_HOME}/.ssh/authorized_keys"

# Pre-seed known_hosts to bypass strict host checking for localhost
ssh-keyscan -H localhost >> "${USER_HOME}/.ssh/known_hosts" 2>/dev/null || true
ssh-keyscan -H 0.0.0.0 >> "${USER_HOME}/.ssh/known_hosts" 2>/dev/null || true
ssh-keyscan -H 127.0.0.1 >> "${USER_HOME}/.ssh/known_hosts" 2>/dev/null || true

# Set PDSH RCMD type to ssh
if ! grep -q "PDSH_RCMD_TYPE=ssh" "${USER_HOME}/.bashrc" 2>/dev/null; then
    echo "export PDSH_RCMD_TYPE=ssh" >> "${USER_HOME}/.bashrc"
fi
export PDSH_RCMD_TYPE=ssh

echo -e "${GREEN}--> [4/8] Downloading and installing Apache Hadoop...${NC}"
HADOOP_VERSION="3.3.6"
HADOOP_TAR="hadoop-${HADOOP_VERSION}.tar.gz"
HADOOP_DIR="/usr/local/hadoop"

if [ ! -d "${HADOOP_DIR}" ]; then
    if [ ! -f "/tmp/${HADOOP_TAR}" ]; then
        echo "Downloading Apache Hadoop ${HADOOP_VERSION} from Apache Archive..."
        wget -q --show-progress -c "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}" || \
        wget -q --show-progress -c "https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/${HADOOP_TAR}" -O "/tmp/${HADOOP_TAR}"
    fi
    echo "Extracting Hadoop distribution to ${HADOOP_DIR}..."
    sudo tar -xzf "/tmp/${HADOOP_TAR}" -C /usr/local/
    sudo mv "/usr/local/hadoop-${HADOOP_VERSION}" "${HADOOP_DIR}"
    sudo chown -R "${CURRENT_USER}:${CURRENT_USER}" "${HADOOP_DIR}"
else
    echo "Hadoop is already installed at ${HADOOP_DIR}."
    sudo chown -R "${CURRENT_USER}:${CURRENT_USER}" "${HADOOP_DIR}"
fi

echo -e "${GREEN}--> [5/8] Configuring Environment Variables & Low-Pause G1GC Tuning...${NC}"
JAVA_DETECTED_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")
if [ -z "${JAVA_DETECTED_HOME}" ]; then
    JAVA_DETECTED_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
fi
echo "--> Detected JAVA_HOME: ${JAVA_DETECTED_HOME}"

# Configure ~/.bashrc
if ! grep -q "HADOOP_HOME=${HADOOP_DIR}" "${USER_HOME}/.bashrc" 2>/dev/null; then
cat <<EOT >> "${USER_HOME}/.bashrc"

# --- Apache Hadoop Environment Variables ---
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=${HADOOP_DIR}
export HADOOP_INSTALL=\$HADOOP_HOME
export HADOOP_MAPRED_HOME=\$HADOOP_HOME
export HADOOP_COMMON_HOME=\$HADOOP_HOME
export HADOOP_HDFS_HOME=\$HADOOP_HOME
export YARN_HOME=\$HADOOP_HOME
export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop
export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=\$HADOOP_HOME/lib/native"
export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin:\$JAVA_HOME/bin
export PDSH_RCMD_TYPE=ssh
EOT
fi

# Export for current script execution
export JAVA_HOME=${JAVA_DETECTED_HOME}
export HADOOP_HOME=${HADOOP_DIR}
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$JAVA_HOME/bin

# Configure hadoop-env.sh
sed -i "s|# export JAVA_HOME=.*|export JAVA_HOME=${JAVA_DETECTED_HOME}|g" "${HADOOP_DIR}/etc/hadoop/hadoop-env.sh"
if ! grep -q "export JAVA_HOME=${JAVA_DETECTED_HOME}" "${HADOOP_DIR}/etc/hadoop/hadoop-env.sh"; then
    echo "export JAVA_HOME=${JAVA_DETECTED_HOME}" >> "${HADOOP_DIR}/etc/hadoop/hadoop-env.sh"
fi

if ! grep -q "HADOOP_HEAPSIZE_MAX" "${HADOOP_DIR}/etc/hadoop/hadoop-env.sh"; then
cat <<'EOT' >> "${HADOOP_DIR}/etc/hadoop/hadoop-env.sh"

# --- High-Performance JVM Heap & G1GC Sizing (Tuned for 6GB VM) ---
export HADOOP_HEAPSIZE_MAX=1024m
export HADOOP_NAMENODE_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"
export HADOOP_DATANODE_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"
export YARN_RESOURCEMANAGER_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"
export YARN_NODEMANAGER_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"
EOT
fi

echo -e "${GREEN}--> [6/8] Generating Production-Aligned Cluster XML Configurations...${NC}"
HDFS_DATA_DIR="${USER_HOME}/hadoopdata/hdfs"
mkdir -p "${HDFS_DATA_DIR}/namenode"
mkdir -p "${HDFS_DATA_DIR}/datanode"

# core-site.xml
cat <<EOT > "${HADOOP_DIR}/etc/hadoop/core-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
        <description>Default filesystem URI for HDFS clients</description>
    </property>
    <property>
        <name>io.file.buffer.size</name>
        <value>65536</value>
        <description>64KB Stream I/O buffer for high throughput</description>
    </property>
</configuration>
EOT

# hdfs-site.xml
cat <<EOT > "${HADOOP_DIR}/etc/hadoop/hdfs-site.xml"
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
        <value>file://${HDFS_DATA_DIR}/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file://${HDFS_DATA_DIR}/datanode</value>
    </property>
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
    </property>
</configuration>
EOT

# mapred-site.xml
cat <<EOT > "${HADOOP_DIR}/etc/hadoop/mapred-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=${HADOOP_DIR}</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=${HADOOP_DIR}</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=${HADOOP_DIR}</value>
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
cat <<EOT > "${HADOOP_DIR}/etc/hadoop/yarn-site.xml"
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>3072</value>
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

echo -e "${GREEN}--> [7/8] Formatting HDFS NameNode...${NC}"
# Check if NameNode was already formatted
if [ ! -d "${HDFS_DATA_DIR}/namenode/current" ]; then
    "${HADOOP_DIR}/bin/hdfs" namenode -format -force
else
    echo "HDFS NameNode directory already contains metadata; skipping reformat to preserve existing data."
fi

echo -e "${GREEN}--> [8/8] Starting Hadoop Daemons (HDFS, YARN & JobHistory)...${NC}"
"${HADOOP_DIR}/sbin/stop-all.sh" 2>/dev/null || true

"${HADOOP_DIR}/sbin/start-dfs.sh"
"${HADOOP_DIR}/sbin/start-yarn.sh"
"${HADOOP_DIR}/bin/mapred" --daemon start historyserver

echo -e "${CYAN}=================================================================${NC}"
echo -e "${GREEN}  🎉 Apache Hadoop Cluster Initialized Successfully!             ${NC}"
echo -e "${CYAN}=================================================================${NC}"

echo -e "${YELLOW}Active JVM Daemons (jps):${NC}"
jps

echo ""
echo -e "${CYAN}Cluster Web UIs Available at:${NC}"
VM_IP=$(hostname -I | awk '{print $1}')
echo -e "  - HDFS NameNode UI:        http://${VM_IP}:9870  (or http://localhost:9870)"
echo -e "  - YARN ResourceManager UI: http://${VM_IP}:8088  (or http://localhost:8088)"
echo -e "  - YARN NodeManager UI:     http://${VM_IP}:8042  (or http://localhost:8042)"
echo -e "  - HDFS DataNode UI:        http://${VM_IP}:9864  (or http://localhost:9864)"
echo -e "  - MapReduce JobHistory UI: http://${VM_IP}:19888 (or http://localhost:19888)"
echo -e "${CYAN}=================================================================${NC}"
