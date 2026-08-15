# 🖥️ Oracle VirtualBox & Ubuntu Apache Hadoop Setup Guide

This guide provides complete, step-by-step instructions for creating, configuring, and operating an **Apache Hadoop single-node cluster** on **Ubuntu Linux** inside **Oracle VM VirtualBox**.

---

## 📋 Table of Contents

1. [Hardware & Prerequisites](#hardware--prerequisites)
2. [Automated VM Setup (PowerShell)](#automated-vm-setup-powershell)
3. [Manual VirtualBox Configuration](#manual-virtualbox-configuration)
4. [Network & Port Forwarding Configuration](#network--port-forwarding-configuration)
5. [Automated Hadoop Installation](#automated-hadoop-installation)
6. [Manual Hadoop Installation Steps](#manual-hadoop-installation-steps)
7. [Verifying the Cluster](#verifying-the-cluster)
8. [Managing Cluster Daemons](#managing-cluster-daemons)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## ⚙️ Hardware & Prerequisites

* **Host OS**: Windows 10/11, macOS, or Linux.
* **Virtualization**: Intel VT-x / AMD-V enabled in BIOS/UEFI.
* **RAM Allocation**: Minimum `2560 MB` (2.5 GB), Recommended `4096 MB` (4 GB) or higher.
* **CPUs**: Minimum `2 vCPUs`.
* **Storage**: `40 GB` or more dynamically allocated virtual disk.
* **Software**:
  * [Oracle VM VirtualBox](https://www.virtualbox.org/) 7.0+
  * [Ubuntu Desktop or Server ISO](https://ubuntu.com/download/desktop) (22.04 LTS / 24.04 LTS)

---

## ⚡ Automated VM Setup (PowerShell)

From your Windows host machine, run the provided provisioning script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1
```

This script automatically:
* Registers the VM named `Ubuntu-Hadoop`.
* Sets optimal RAM (`2560 MB`), CPUs (`2`), and Paravirtualization (`Hyper-V`).
* Creates a `40 GB` VDI virtual disk.
* Attaches the Ubuntu installation ISO.
* Configures NAT Port Forwarding for SSH and Hadoop Web interfaces.
* Boots the VM.

---

## 🛠️ Manual VirtualBox Configuration

If configuring manually via the VirtualBox Graphical Interface:

1. Click **New**:
   * **Name**: `Ubuntu-Hadoop`
   * **Type**: `Linux`
   * **Version**: `Ubuntu (64-bit)`
   * **ISO Image**: Browse to your downloaded Ubuntu `.iso`.
2. **Hardware**:
   * **Base Memory**: `2560 MB` to `4096 MB`
   * **Processors**: `2 CPUs`
3. **Hard Disk**:
   * Create a Virtual Hard Disk Now $\rightarrow$ `VDI` $\rightarrow$ Dynamically Allocated $\rightarrow$ `40.00 GB`.
4. **System Acceleration Settings**:
   * Go to **Settings** $\rightarrow$ **System** $\rightarrow$ **Acceleration**.
   * Set **Paravirtualization Interface** to `Hyper-V` (recommended for Windows hosts) or `Default`.
   * Enable **HPET** (High Precision Event Timer) and **IO APIC**.

---

## 🌐 Network & Port Forwarding Configuration

Using **NAT with Port Forwarding** allows seamless access to Hadoop Web UIs and SSH from the Windows host without needing Bridged networking:

In VirtualBox:
**Settings** $\rightarrow$ **Network** $\rightarrow$ **Adapter 1 (NAT)** $\rightarrow$ **Advanced** $\rightarrow$ **Port Forwarding**:

| Rule Name | Protocol | Host IP | Host Port | Guest IP | Guest Port | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ssh` | TCP | `127.0.0.1` | **2222** | *(blank)* | **22** | SSH Terminal Access |
| `namenode` | TCP | `127.0.0.1` | **9870** | *(blank)* | **9870** | HDFS NameNode Web UI |
| `yarn` | TCP | `127.0.0.1` | **8088** | *(blank)* | **8088** | YARN ResourceManager Web UI |
| `datanode` | TCP | `127.0.0.1` | **9864** | *(blank)* | **9864** | HDFS DataNode Web UI |
| `jobhistory` | TCP | `127.0.0.1` | **19888** | *(blank)* | **19888** | MapReduce JobHistory UI |

---

## 🚀 Automated Hadoop Installation

1. Connect to the Ubuntu VM via SSH:
   ```bash
   ssh -p 2222 hadoopuser@localhost
   ```

2. Download and run the automated cluster installer:
   ```bash
   bash /path/to/install-hadoop-ubuntu.sh
   ```

---

## 📖 Manual Hadoop Installation Steps

### 1. Install Java and OpenSSH
```bash
sudo apt update && sudo apt install -y openjdk-11-jdk-headless openssh-server openssh-client pdsh
```

### 2. Configure Passwordless SSH
```bash
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
ssh localhost # verify without password prompt
exit
```

### 3. Download & Install Hadoop
```bash
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -P /tmp
sudo tar -xzf /tmp/hadoop-3.3.6.tar.gz -C /usr/local/
sudo mv /usr/local/hadoop-3.3.6 /usr/local/hadoop
sudo chown -R $USER:$USER /usr/local/hadoop
```

### 4. Configure Environment Variables (`~/.bashrc`)
Add the following to the bottom of `~/.bashrc`:
```bash
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$JAVA_HOME/bin
export PDSH_RCMD_TYPE=ssh
```
Apply the changes:
```bash
source ~/.bashrc
```

### 5. Configure Hadoop XML Files

#### `core-site.xml` (`$HADOOP_HOME/etc/hadoop/core-site.xml`)
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

#### `hdfs-site.xml` (`$HADOOP_HOME/etc/hadoop/hdfs-site.xml`)
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoopuser/hadoopdata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/hadoopuser/hadoopdata/hdfs/datanode</value>
    </property>
</configuration>
```

#### `mapred-site.xml` (`$HADOOP_HOME/etc/hadoop/mapred-site.xml`)
```xml
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
```

#### `yarn-site.xml` (`$HADOOP_HOME/etc/hadoop/yarn-site.xml`)
```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

### 6. Format and Start Cluster
```bash
# Format NameNode
hdfs namenode -format

# Start DFS and YARN
start-dfs.sh
start-yarn.sh
```

---

## 🔍 Verifying the Cluster

1. Check active Java processes with `jps`:
   ```bash
   jps
   ```
   You should see:
   * `NameNode`
   * `DataNode`
   * `SecondaryNameNode`
   * `ResourceManager`
   * `NodeManager`
   * `Jps`

2. Test HDFS file operations:
   ```bash
   hdfs dfs -mkdir -p /user/hadoopuser/input
   echo "Hello Hadoop in VirtualBox Ubuntu" > /tmp/sample.txt
   hdfs dfs -put /tmp/sample.txt /user/hadoopuser/input/
   hdfs dfs -ls /user/hadoopuser/input/
   hdfs dfs -cat /user/hadoopuser/input/sample.txt
   ```

3. Open Web UIs in Windows Browser:
   * **NameNode Status**: [http://localhost:9870](http://localhost:9870)
   * **YARN Applications**: [http://localhost:8088](http://localhost:8088)

---

## 🔄 Managing Cluster Daemons

| Command | Purpose |
| :--- | :--- |
| `start-dfs.sh` | Starts NameNode, DataNodes, SecondaryNameNode |
| `stop-dfs.sh` | Stops all HDFS daemons |
| `start-yarn.sh` | Starts ResourceManager and NodeManagers |
| `stop-yarn.sh` | Stops all YARN daemons |
| `mapred --daemon start historyserver` | Starts MapReduce JobHistory server |
| `mapred --daemon stop historyserver` | Stops MapReduce JobHistory server |

---

## 🛠️ Troubleshooting Common Issues

### 1. `rcu_preempt self-detected stall on CPU` during boot
* **Cause**: Timer clocksource conflict when running multi-vCPU Linux kernels under Windows Hyper-V/WHPX.
* **Fix**: Run `VBoxManage modifyvm "Ubuntu-Hadoop" --paravirtprovider hyperv --hpet on`.

### 2. `VERR_NO_PAGE_MEMORY` Error on VM Startup
* **Cause**: VirtualBox failed to allocate contiguous host RAM.
* **Fix**: Lower VM RAM to `2560 MB` or close high-RAM host processes.

### 3. `Permission denied (publickey)` when running `start-dfs.sh`
* **Fix**: Ensure SSH keys are properly authorized:
  ```bash
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
  ```
