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

* **Host OS**: Windows 11 / 10 Pro (64-bit) with Hyper-V / WSL2 support.
* **CPU Sizing**: `4 vCPUs` (50% of an 8-thread CPU like Intel Core i5-10300H) with 100% execution cap for smooth parallel MapReduce & Spark execution.
* **RAM Allocation**: `5120 MB` (5 GB). For a 16 GB host machine, 5 GB VM RAM gives ample headroom for Hadoop daemons (2 GB) and YARN compute containers (3.5 GB) while leaving 11 GB for Windows, IDEs, and browser UIs.
* **Storage**: `40 GB` or more dynamically allocated virtual disk located on your high-capacity drive (e.g., `D:\VirtualBoxVMs`) with **Host I/O Cache** enabled.
* **Paravirtualization**: `Hyper-V` paravirtualization provider for precise clock synchronization and zero timer drift under Windows WHPX.
* **Input Controller**: USB Keyboard & USB Tablet Mouse for zero-latency keystroke polling.
* **Software**:
  * [Oracle VM VirtualBox](https://www.virtualbox.org/) 7.0+
  * [Ubuntu Desktop or Server ISO](https://ubuntu.com/download/desktop) (22.04 LTS / 24.04 LTS / 26.04)

---

## ⚡ Automated VM Setup (PowerShell)

From your Windows host machine in PowerShell or via `make`, run the provided provisioning script:

```powershell
# Standard Creation / Launch with GUI Window (4 vCPUs, 5GB RAM, UEFI, FHD)
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1

# High-Performance Headless Launch (Runs quietly in background, saves CPU/RAM)
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1 -Headless

# Clean Rebuild from Scratch (tears down previous VM and recreates clean VDI)
powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1 -Rebuild
```

Or using the repository `Makefile`:
```bash
make vm-create            # Create and configure VM
make vm-start             # Start with GUI window
make vm-start-headless    # Start headless (recommended for terminal/SSH work)
make vm-ssh               # Open SSH session to Ubuntu
make vm-status            # Check running state and memory
make vm-stop              # Graceful ACPI shutdown
```

This script automatically:
* Registers the VM named `Ubuntu-Hadoop`.
* Sets optimal RAM (`5120 MB`), CPUs (`4 vCPUs`), USB keyboard/mouse, and Paravirtualization (`Hyper-V`).
* Configures **UEFI / EFI firmware** with native **Full HD (1920x1080)** GOP resolution.
* Configures **`--large-pages off`** preventing Windows standard user `VERR_UNRESOLVED_ERROR` allocation failures.
* Enables **VMSVGA** graphics with **Dynamic Window Auto-Resize**.
* Creates a `40 GB` VDI virtual disk with **Host I/O Caching** and attaches the Ubuntu ISO.
* Configures NAT Port Forwarding for SSH, HDFS, YARN, MapReduce, Spark, and Hive.
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

Using **NAT with Port Forwarding** allows seamless access to all Hadoop & Big Data Web UIs and SSH directly from your Windows host browser and terminal:

| Service / Component | Protocol | Host IP | Host Port | Guest Port | Web UI / Direct Link |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SSH Terminal** | TCP | `127.0.0.1` | **2222** | **22** | `ssh -p 2222 hadoopuser@localhost` |
| **HDFS NameNode** | TCP | `127.0.0.1` | **9870** | **9870** | [http://127.0.0.1:9870](http://127.0.0.1:9870) |
| **YARN ResourceManager** | TCP | `127.0.0.1` | **8088** | **8088** | [http://127.0.0.1:8088](http://127.0.0.1:8088) |
| **YARN NodeManager** | TCP | `127.0.0.1` | **8042** | **8042** | [http://127.0.0.1:8042](http://127.0.0.1:8042) |
| **HDFS DataNode** | TCP | `127.0.0.1` | **9864** | **9864** | [http://127.0.0.1:9864](http://127.0.0.1:9864) |
| **MapReduce JobHistory** | TCP | `127.0.0.1` | **19888** | **19888** | [http://127.0.0.1:19888](http://127.0.0.1:19888) |
| **HDFS RPC Port** | TCP | `127.0.0.1` | **9000** | **9000** | `hdfs://127.0.0.1:9000` |
| **Apache Spark UI** | TCP | `127.0.0.1` | **4040** | **4040** | [http://127.0.0.1:4040](http://127.0.0.1:4040) |
| **Spark History Server** | TCP | `127.0.0.1` | **18080** | **18080** | [http://127.0.0.1:18080](http://127.0.0.1:18080) |
| **HiveServer2 JDBC/Thrift** | TCP | `127.0.0.1` | **10000** | **10000** | `jdbc:hive2://127.0.0.1:10000` |
| **HiveServer2 Web UI** | TCP | `127.0.0.1` | **10002** | **10002** | [http://127.0.0.1:10002](http://127.0.0.1:10002) |

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

### 4. `VERR_UNRESOLVED_ERROR` / `0x80004005` on VM Launch
* **Root Cause**: VirtualBox requesting `MEM_LARGE_PAGES` on Windows when the user account lacks the `SeLockMemoryPrivilege` security policy.
* **Fix**: Disable large-pages:
  ```powershell
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Ubuntu-Hadoop" --large-pages off --nested-paging on
  ```

### 5. VM Terminal Typing Lag or Compositor Sluggishness
* **Root Cause**: GNOME Mutter desktop compositor using LLVMpipe software rendering on 1080p when allocated fewer than 4 cores, plus PS/2 keyboard polling overhead.
* **Fix**: Assign 4 vCPUs and USB input controller:
  ```powershell
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "Ubuntu-Hadoop" --cpus 4 --keyboard usb --mouse usbtablet
  ```

### 6. Installing Hadoop in User Space (Zero Sudo / Passwordless)
* If you do not wish to use `sudo` or provide root passwords during Hadoop cluster setup, run the standalone user-space installer:
  ```bash
  bash ~/docker-hadoop/scripts/install-hadoop-user.sh
  ```
  This installs Apache Hadoop directly into `~/hadoop` and manages all data in `~/hadoopdata`.

---

## ⚡ High-Performance Headless Workflow & VS Code Remote SSH

For the highest possible speed, lowest RAM consumption, and zero UI lag:

1. **Start the VM Headless** (no GUI window rendered, saving ~1GB RAM and CPU rendering):
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox-setup.ps1 -Headless
   # OR using make
   make vm-start-headless
   ```

2. **Connect via VS Code / Antigravity Remote-SSH**:
   - Install the **Remote - SSH** extension.
   - Add to your `~/.ssh/config`:
     ```ssh
     Host hadoop-vm
         HostName 127.0.0.1
         Port 2222
         User hadoopuser
         StrictHostKeyChecking no
         UserKnownHostsFile /dev/null
     ```
   - Click **Connect to Host -> hadoop-vm**. You get a full Linux terminal, native file tree, and code editor directly inside the VM!

3. **Access Web UIs in Windows Browser**:
   Open [http://127.0.0.1:9870](http://127.0.0.1:9870) (NameNode) or [http://127.0.0.1:8088](http://127.0.0.1:8088) (YARN).

---

## 📊 Comparison: VirtualBox VM vs Docker Compose vs WSL2

| Dimension | 🖥️ VirtualBox VM (Tuned) | 🐳 Docker Compose (Current Repo) | 🐧 WSL2 Native |
| :--- | :--- | :--- | :--- |
| **Primary Learning Goal** | Full Linux cluster administration, systemd, SSH nodes, authentic production VM feel | Fast MapReduce / Spark algorithm testing, containerized pipelines, rapid teardown | Direct Windows-Linux integration, lowest resource usage |
| **RAM Consumption** | ~5 GB (Fixed allocation) | ~1.5 GB - 3 GB (Dynamic container memory) | ~2 GB - 4 GB (Dynamic WSL memory) |
| **CPU Overhead** | Medium (Hardware virtualization layer) | Low (Shares host kernel) | Low (Direct Hyper-V microVM) |
| **Startup Time** | ~15 - 25 seconds | ~3 - 5 seconds (`make up`) | ~2 seconds |
| **Isolation** | Complete (Isolated guest OS & virtual disk) | Process-level (Isolated container filesystem) | User-space isolation |
| **Recommended For** | Deep-dive Big Data infrastructure & multi-node practice | Daily ETL, PySpark, MapReduce scripting & Git CI/CD | Hybrid Windows/Linux scripting |


