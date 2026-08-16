# 🖥️ Oracle VirtualBox & Ubuntu Apache Hadoop Setup Guide

This guide provides complete, step-by-step instructions for creating, configuring, and operating an **Apache Hadoop single-node cluster** on **Ubuntu Linux** inside **Oracle VM VirtualBox**.

---

## 📋 Table of Contents

1. [Hardware & Prerequisites](#hardware--prerequisites)
2. [Automated VM Setup (PowerShell)](#automated-vm-setup-powershell)
3. [Display, FHD & Auto-Resize Configuration](#display-fhd--auto-resize-configuration)
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
* **RAM Allocation**: Recommended `4096 MB` (4 GB) or higher (Minimum `2560 MB`).
* **CPUs**: `2 vCPUs` with 100% execution cap.
* **Storage**: `40 GB` or more dynamically allocated virtual disk.
* **Software**:
  * [Oracle VM VirtualBox](https://www.virtualbox.org/) 7.0+
  * [Ubuntu Desktop or Server ISO](https://ubuntu.com/download/desktop) (22.04 LTS / 24.04 LTS / 26.04)

---

## ⚡ Automated VM Setup (PowerShell)

From your Windows host machine in PowerShell, run the provided provisioning script:

```powershell
# Standard Creation / Launch
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1

# Clean Rebuild from Scratch
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1 -Rebuild
```

This script automatically:
* Registers the VM named `Ubuntu-Hadoop`.
* Sets optimal RAM (`4096 MB`), CPUs (`2`), and Paravirtualization (`Hyper-V`).
* Configures **UEFI / EFI firmware** with native **Full HD (1920x1080)** GOP resolution.
* Enables **VMSVGA** graphics with **Dynamic Window Auto-Resize**.
* Creates a `40 GB` VDI virtual disk and attaches the Ubuntu ISO.
* Configures NAT Port Forwarding for SSH and all Hadoop Web interfaces.
* Boots the VM.

---

## 🖥️ Display, FHD & Auto-Resize Configuration

To ensure the virtual machine fills your window or monitor with crisp, unscaled 1:1 Full HD quality:

### Keyboard Shortcuts in VirtualBox Window:

| Shortcut | Action | Description |
| :--- | :--- | :--- |
| **`Right-Ctrl + F`** | **Full-Screen Mode** | Fills your entire monitor with native resolution. |
| **`Right-Ctrl + G`** | **Auto-Resize Guest Display** | Dynamic auto-resize whenever the window borders are dragged. |
| **`Right-Ctrl + L`** | **Seamless Mode** | Integrates guest windows with your Windows desktop. |

### Manual Display Commands (Host PowerShell):

```powershell
$VBox = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

# Set Native 1920x1080 EFI Framebuffer
& $VBox setextradata "Ubuntu-Hadoop" "VBoxInternal2/EfiGraphicsResolution" "1920x1080"
& $VBox setextradata "Ubuntu-Hadoop" "CustomVideoMode1" "1920x1080x32"

# Enable Unscaled 1:1 Display & Dynamic Auto-Resize
& $VBox setextradata "Ubuntu-Hadoop" "GUI/ScaleFactor" "1.0"
& $VBox setextradata "Ubuntu-Hadoop" "GUI/MaxGuestResolution" "any"
& $VBox setextradata "Ubuntu-Hadoop" "GUI/AutoResizeGuest" "on"
```

---

## 🌐 Network & Port Forwarding Configuration

Using **NAT with Port Forwarding** allows seamless access to Hadoop Web UIs and SSH directly from your Windows host browser and terminal:

| Rule Name | Protocol | Host IP | Host Port | Guest IP | Guest Port | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ssh` | TCP | `127.0.0.1` | **2222** | *(blank)* | **22** | SSH Terminal Access |
| `namenode` | TCP | `127.0.0.1` | **9870** | *(blank)* | **9870** | HDFS NameNode Web UI |
| `yarn` | TCP | `127.0.0.1` | **8088** | *(blank)* | **8088** | YARN ResourceManager Web UI |
| `datanode` | TCP | `127.0.0.1` | **9864** | *(blank)* | **9864** | HDFS DataNode Web UI |
| `jobhistory` | TCP | `127.0.0.1` | **19888** | *(blank)* | **19888** | MapReduce JobHistory UI |

---

## 🚀 Automated Hadoop Installation

Once the Ubuntu OS is installed inside the VM and running:

1. Copy the installer script from Windows to Ubuntu via SCP:
   ```powershell
   scp -P 2222 .\scripts\install-hadoop-ubuntu.sh hadoopuser@localhost:~/
   ```

2. SSH into the Ubuntu VM:
   ```powershell
   ssh -p 2222 hadoopuser@localhost
   ```

3. Run the automated cluster installer:
   ```bash
   chmod +x ~/install-hadoop-ubuntu.sh
   bash ~/install-hadoop-ubuntu.sh
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

### 3. Download & Install Hadoop 3.3.6
```bash
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -P /tmp
sudo tar -xzf /tmp/hadoop-3.3.6.tar.gz -C /usr/local/
sudo mv /usr/local/hadoop-3.3.6 /usr/local/hadoop
sudo chown -R $USER:$USER /usr/local/hadoop
```

### 4. Configure Environment Variables (`~/.bashrc`)
Add the following to `~/.bashrc`:
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
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
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
mapred --daemon start historyserver
```

---

## 🔍 Verifying the Cluster

1. Check active Java daemons with `jps`:
   ```bash
   jps
   ```
   Expected output:
   * `NameNode`
   * `DataNode`
   * `SecondaryNameNode`
   * `ResourceManager`
   * `NodeManager`
   * `JobHistoryServer`
   * `Jps`

2. Run the MapReduce Pi Calculation Benchmark:
   ```bash
   yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 2 100
   ```

3. Access Web UIs from your Windows Browser:
   * **HDFS NameNode UI**: [http://127.0.0.1:9870](http://127.0.0.1:9870)
   * **YARN ResourceManager UI**: [http://127.0.0.1:8088](http://127.0.0.1:8088)
   * **HDFS DataNode UI**: [http://127.0.0.1:9864](http://127.0.0.1:9864)
   * **MapReduce JobHistory UI**: [http://127.0.0.1:19888](http://127.0.0.1:19888)

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

### 1. `watchdog: BUG: soft lockup - CPU stuck` / Timer Drift
* **Root Cause**: Timer clocksource conflict between Linux kernel and Windows WHPX / Hyper-V.
* **Fix**: Set paravirtualization provider to `hyperv`:
  ```powershell
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Ubuntu-Hadoop" --paravirtprovider hyperv --hpet on
  ```

### 2. Blank / Black Screen on Live ISO Boot
* **Root Cause**: Linux DRM framebuffer mode-switch stall on legacy BIOS.
* **Fix**: Use EFI firmware (`--firmware efi`) with native GOP resolution:
  ```powershell
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Ubuntu-Hadoop" --firmware efi --graphicscontroller vmsvga --vram 128
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "Ubuntu-Hadoop" "VBoxInternal2/EfiGraphicsResolution" "1920x1080"
  ```

### 3. Display Has Black Bars / Does Not Fit Window
* **Fix**: Enable AutoResizeGuest and MaxGuestResolution:
  ```powershell
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "Ubuntu-Hadoop" "GUI/AutoResizeGuest" "on"
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "Ubuntu-Hadoop" "GUI/MaxGuestResolution" "any"
  ```
  In the VM window, press **`Right-Ctrl + G`** (Auto-Resize) or **`Right-Ctrl + F`** (Fullscreen).
