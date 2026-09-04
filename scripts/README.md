# 📜 Platform Orchestration & Automation Scripts

This directory houses modular automation scripts organized by runtime environment, handling container lifecycle, guest VM optimization, network configuration, and bare-metal Hadoop setups.

---

## 📂 Subdirectory Architecture

```text
scripts/
├── docker/          # Docker container initialization & health monitoring
├── gcp/             # Google Cloud Dataproc & Compute Engine deployment automation
├── hyperv/          # Microsoft Hyper-V host & guest optimization scripts
├── linux/           # Ubuntu / Debian bare-metal Hadoop installation & systemd setup
├── virtualbox/      # Oracle VirtualBox automated provisioning scripts
├── vmware/          # VMware Workstation Kali Linux VMX tuning & display fixes
└── wsl/             # Windows Subsystem for Linux (WSL 2) xRDP & config sync
```

---

## 🛠️ Script Catalog

### 1. Docker Runtime (`scripts/docker/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`entrypoint.sh`](docker/entrypoint.sh) | Bash | Container PID 1 entrypoint. Formats NameNode if unformatted, launches OpenSSH, starts HDFS daemons (`start-dfs.sh`), starts YARN daemons (`start-yarn.sh`), starts JobHistoryServer (`mr-jobhistory-daemon.sh`), and tails logs to keep container foreground active. |
| [`healthcheck.sh`](docker/healthcheck.sh) | Bash | Container healthcheck probe. Runs `jps` to ensure all 5 core daemons (`NameNode`, `DataNode`, `SecondaryNameNode`, `ResourceManager`, `NodeManager`) and SSH are healthy. |
| [`test-cluster.sh`](docker/test-cluster.sh) | Bash | Automated verification suite: checks HDFS cluster capacity, tests file write/read, executes sample MapReduce job, and validates YARN node status. |

### 2. Microsoft Hyper-V (`scripts/hyperv/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`optimize-hyperv-vm.ps1`](hyperv/optimize-hyperv-vm.ps1) | PowerShell | Automatically scales VM resources to 4 vCPUs, sets Dynamic Memory (3072 MB - 4096 MB), prioritizes hard drive boot, sets UEFI CA, and boots VM. |
| [`fix-vm-internet.ps1`](hyperv/fix-vm-internet.ps1) | PowerShell | Diagnoses Hyper-V Default Switch NAT adapter, resets DNS bindings, and restores internet routing to the guest VM. |
| [`configure-hyperv-host-enhanced-session.ps1`](hyperv/configure-hyperv-host-enhanced-session.ps1) | PowerShell | Configures Hyper-V host global policy to permit Enhanced Session Mode for Linux guests. |
| [`enable-hyperv-enhanced-session.sh`](hyperv/enable-hyperv-enhanced-session.sh) | Bash | Guest-side setup for Linux xRDP / linux-vm-tools to negotiate Hyper-V Enhanced Session transport via VMBus vsock. |

### 3. Linux / Bare-Metal (`scripts/linux/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`install-hadoop-ubuntu.sh`](linux/install-hadoop-ubuntu.sh) | Bash | End-to-end installation script for Ubuntu 20.04/22.04: installs Java 8, creates `hduser`, downloads and unpacks Hadoop, configures XML files, and formats HDFS. |
| [`install-hadoop-user.sh`](linux/install-hadoop-user.sh) | Bash | Configures environment variables (`.bashrc`), SSH keypairs (`ssh-keygen`), and permissions for dedicated `hduser`. |
| [`setup-hadoop-systemd.sh`](linux/setup-hadoop-systemd.sh) | Bash | Registers systemd service units (`hadoop-hdfs.service`, `hadoop-yarn.service`) for automatic daemon startup on boot. |
| [`start-daemons-direct.sh`](linux/start-daemons-direct.sh) | Bash | Directly starts HDFS & YARN daemons via `hdfs --daemon start` without relying on master-worker SSH scripts. |

### 4. Oracle VirtualBox (`scripts/virtualbox/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`virtualbox-setup.ps1`](virtualbox/virtualbox-setup.ps1) | PowerShell | Automates VirtualBox VM creation, attaches Ubuntu ISO, sets RAM, vCPUs, and configures NAT port forwarding rules for Hadoop Web UIs. |

### 5. VMware Workstation (`scripts/vmware/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`optimize-kali-vmx.ps1`](vmware/optimize-kali-vmx.ps1) | PowerShell | Injects low-latency VMX settings into Kali VM: sets 6GB RAM, 4 vCPUs, disables nested VT-x popups (`vhv.enable=FALSE`), and enables clipboard sharing. |
| [`install-hadoop-kali.sh`](vmware/install-hadoop-kali.sh) | Bash | Guest-side installation of Apache Hadoop 3.3.6 and Java 11/8 on Kali Linux. |
| [`apply-guest-mouse-fix.ps1`](vmware/apply-guest-mouse-fix.ps1) | PowerShell | Fixes mouse grab and pointer desynchronization issues in VMware Workstation. |
| [`fix-mouse-in-guest.sh`](vmware/fix-mouse-in-guest.sh) | Bash | Configures guest `xserver-xorg-input-vmmouse` drivers inside Kali/Ubuntu. |
| [`set-fullscreen-resolution.ps1`](vmware/set-fullscreen-resolution.ps1) | PowerShell | Adjusts display resolution dynamically to match Windows host monitor. |

### 6. Windows Subsystem for Linux (`scripts/wsl/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`fix-xrdp.sh`](wsl/fix-xrdp.sh) | Bash | Reconfigures and restarts xRDP service on non-standard port `3390` with XFCE4 session for WSL 2 GUI. |
| [`install-hadoop-wsl.sh`](wsl/install-hadoop-wsl.sh) | Bash | Configures Hadoop inside Ubuntu WSL 2 distribution. |
| [`start-hadoop-cluster.sh`](wsl/start-hadoop-cluster.sh) | Bash | Starts NameNode, DataNode, ResourceManager, and NodeManager inside WSL 2. |
| [`sync-wsl-configs.sh`](wsl/sync-wsl-configs.sh) | Bash | Synchronizes Hadoop XML configuration files from repository `config/` directory into WSL `/usr/local/hadoop/etc/hadoop/`. |

### 7. Google Cloud Platform (`scripts/gcp/`)

| Script | Language | Purpose |
|:---|:---|:---|
| [`create-dataproc-cluster.sh`](gcp/create-dataproc-cluster.sh) | Bash | Provisions an auto-terminating Google Cloud Dataproc cluster with Component Gateway, Spot workers, and GCS integration. |
| [`submit-mapreduce-job.sh`](gcp/submit-mapreduce-job.sh) | Bash | Uploads datasets to `gs://` and submits Python Hadoop Streaming or Java MapReduce jobs to Dataproc. |
| [`teardown-dataproc-cluster.sh`](gcp/teardown-dataproc-cluster.sh) | Bash | Gracefully deletes an ephemeral Dataproc cluster to stop cloud compute billing. |
| [`deploy-hadoop-gce.sh`](gcp/deploy-hadoop-gce.sh) | Bash | Deploys containerized Docker Hadoop on an Ubuntu Google Compute Engine (GCE) VM with automated VPC firewall configuration. |

