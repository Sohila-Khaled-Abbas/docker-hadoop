<div align="center">

# 🐘 Apache Hadoop Enterprise Multi-Platform Lab

### *Unified Big Data Engineering Ecosystem for Docker, VMware (Kali Linux), Hyper-V, WSL 2, Oracle VirtualBox & Bare-Metal Linux*

<p align="center">
  <a href="https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/ci.yml">
    <img src="https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/ci.yml/badge.svg" alt="CI Build & Test" />
  </a>
  <a href="https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/security-scan.yml">
    <img src="https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/security-scan.yml/badge.svg" alt="Security Scan" />
  </a>
  <a href="https://hadoop.apache.org/">
    <img src="https://img.shields.io/badge/Apache%20Hadoop-3.1.2%20%7C%203.3.6-66CCFF?logo=apache&logoColor=white" alt="Hadoop" />
  </a>
  <a href="https://openjdk.org/">
    <img src="https://img.shields.io/badge/Java-OpenJDK%208%20%7C%2011-ED8B00?logo=openjdk&logoColor=white" alt="Java" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8%2B%20%7C%20PySpark-3776AB?logo=python&logoColor=white" alt="Python" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License" />
  </a>
</p>

<p align="center">
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Platform-Docker%20%26%20Compose-2496ED?logo=docker&logoColor=white" alt="Docker" />
  </a>
  <a href="https://www.vmware.com/">
    <img src="https://img.shields.io/badge/Platform-VMware%20Workstation-607078?logo=vmware&logoColor=white" alt="VMware" />
  </a>
  <a href="https://learn.microsoft.com/virtualization/hyper-v-on-windows/">
    <img src="https://img.shields.io/badge/Platform-Microsoft%20Hyper--V-0078D4?logo=windows&logoColor=white" alt="Hyper-V" />
  </a>
  <a href="https://learn.microsoft.com/windows/wsl/">
    <img src="https://img.shields.io/badge/Platform-WSL%202%20Ubuntu-FCC624?logo=linux&logoColor=black" alt="WSL 2" />
  </a>
  <a href="https://www.kali.org/">
    <img src="https://img.shields.io/badge/OS-Kali%20Linux%20Rolling-557C94?logo=kalilinux&logoColor=white" alt="Kali Linux" />
  </a>
  <a href="https://ubuntu.com/">
    <img src="https://img.shields.io/badge/OS-Ubuntu%2020.04%20%7C%2024.04-E95420?logo=ubuntu&logoColor=white" alt="Ubuntu" />
  </a>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-supported-environments">Environments</a> •
  <a href="#-1-click-quick-start">Quick Start</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-web-interfaces--port-mappings">Web Consoles</a> •
  <a href="#-data-engineering-tutorials">Tutorials</a> •
  <a href="#-sample-datasets">Datasets</a> •
  <a href="#-repository-structure">Structure</a> •
  <a href="#-documentation">Docs</a>
</p>

</div>

---

## 📖 Overview

Welcome to the **Apache Hadoop Enterprise Multi-Platform Lab** — a unified, production-grade Big Data engineering workspace designed for distributed computing research, university courses, ETL prototyping, and performance benchmarking.

Unlike conventional single-purpose repositories, this project delivers a **cross-platform deployment suite** supporting:
1. **Containerized Cluster (Docker & Docker Compose)**: Single-node Hadoop 3.1.2 with automated daemon supervisors, named persistent storage, and built-in health probes.
2. **Virtual Machine Workstations (VMware Workstation Pro & Kali Linux)**: Automated VMX hardware tuning (6GB RAM, 4 vCPUs, G1GC optimization, swappiness tuning, full-screen 1080p, programmatic mouse fix, and Hadoop 3.3.6 installer).
3. **Enterprise Type-1 Hypervisor (Microsoft Hyper-V Generation 2)**: 4 vCPUs, dynamic memory allocation, enhanced session mode (`HvSocket` bidirectional clipboard), and automated NAT virtual switch recovery.
4. **Near-Bare-Metal Windows Subsystem (WSL 2 Ubuntu)**: Ultra-fast I/O with XFCE4 visual desktop over RDP (port 3390) and zero-friction cluster startup.
5. **Open Source Virtualization (Oracle VirtualBox)**: Automated PowerShell VM orchestrator (`virtualbox-setup.ps1`) with NAT port forwarding rules.
6. **Native Linux & Bare Metal**: Non-root systemd service unit configurations and user-space zero-sudo installers.

---

## 🚀 Key Features

- **Multi-Environment Orchestration**: Launch Hadoop across Docker, VMware, Hyper-V, WSL 2, or VirtualBox with platform-tailored scripts.
- **Complete Hadoop Daemon Stack**:
  - **HDFS**: NameNode, DataNode, SecondaryNameNode.
  - **YARN**: ResourceManager, NodeManager.
  - **MapReduce**: JobHistory Server.
- **1-Click Windows Launchers ([`launchers/windows/`](launchers/windows/))**:
  - [`Start-Hadoop-Docker.bat`](launchers/windows/Start-Hadoop-Docker.bat) & [`Stop-Hadoop-Docker.bat`](launchers/windows/Stop-Hadoop-Docker.bat) for instant Docker cluster control.
  - [`Launch-Kali-VMware.bat`](launchers/windows/Launch-Kali-VMware.bat) for automated VMX tuning & Kali boot.
  - [`Fix-Lag-And-Start-VM.bat`](launchers/windows/Fix-Lag-And-Start-VM.bat) & [`Fix-VM-Internet.bat`](launchers/windows/Fix-VM-Internet.bat) for Hyper-V management.
  - [`Ubuntu-WSL-GUI.rdp`](launchers/windows/Ubuntu-WSL-GUI.rdp) for instant Remote Desktop GUI access.
- **Hands-On Big Data Tutorials (`examples/`)**:
  - **HDFS CLI**: Comprehensive operations walkthrough (`demo-hdfs-operations.sh`) covering block inspection, quotas, and SafeMode.
  - **Python Hadoop Streaming**: Automated mapper/reducer WordCount pipeline.
  - **Java Native MapReduce**: Standalone WordCount application with automated compiler and runner.
  - **Apache Spark & PySpark**: Direct HDFS Parquet & CSV DataFrame ingestion and aggregation.
- **Pre-Packaged Datasets (`datasets/`)**:
  - Real-world unstructured text (`wordcount-sample.txt`) and tabular records (`employees.csv`) for zero-setup experimentation.
- **Enterprise Hardening & DevOps CI/CD**:
  - Dedicated non-root `hduser:hadoop` (UID/GID 1000) execution.
  - Multi-stage Docker build pruning ~60,000 redundant Javadoc HTML files to bypass filesystem journal overhead.
  - GitHub Actions CI matrix validating builds, container health checks, JPS daemons, and MapReduce jobs on every push.

---

## 🏛️ System Architecture

<p align="center">
  <a href="docs/images/hadoop-data-engineering-system-architecture.svg">
    <img src="docs/images/hadoop-data-engineering-infographic.png" alt="Apache Hadoop Modern Big Data Engineering and Software Engineering Architecture" width="100%" />
  </a>
  <br/>
  <em>🔍 Click the diagram above to view the scalable, high-definition vector SVG version.</em>
</p>

```mermaid
flowchart TB
    subgraph Host["💻 DEVELOPER HOST & CLIENT ACCESS LAYER"]
        direction LR
        DevUI["🌐 Web Consoles<br/>(:9870, :8088, :19888)"]
        DevCLI["💻 Terminal CLI<br/>(make / docker compose)"]
        DevLaunch["🚀 1-Click Launchers<br/>(launchers/windows/*.bat)"]
        DevSSH["🔑 SSH Client<br/>(:22222 hduser:ubuntu)"]
    end

    subgraph Container["🐳 DOCKER RUNTIME: hadoop-master (Ubuntu 20.04 / OpenJDK 8 / hduser:1000)"]
        direction TB

        subgraph HDFS["🗄️ DISTRIBUTED STORAGE LAYER (HDFS)"]
            direction TB
            NN["👑 NameNode (Master)<br/>Port: 9870 (Web) / 9000 (RPC)<br/>• Inodes Tree • FSImage • EditLog"]
            SNN["🔄 SecondaryNameNode (Checkpointer)<br/>Port: 9868 (HTTP)<br/>• Periodically Merges FSImage + Edits"]
            DN["📦 DataNode (Worker)<br/>Port: 9864 (Web) / 9866 (Data)<br/>• 128MB Blocks • CRC32C Checksums"]
            NN <-->|"Heartbeats (3s) & Block Reports"| DN
            NN <-->|"Checkpoint Sync"| SNN
        end

        subgraph YARN["⚙️ RESOURCE & COMPUTE ORCHESTRATION (YARN)"]
            direction TB
            RM["🧠 ResourceManager (Master)<br/>Port: 8088 (Web) / 8032 (IPC)<br/>• Pluggable Scheduler • AppManager"]
            NM["👷 NodeManager (Worker)<br/>Port: 8042 (Web) / 8040 (IPC)<br/>• Container Lifecycle & Monitoring"]
            AM["🎯 ApplicationMaster<br/>(Container #001)<br/>• Per-Job Coordinator"]
            Tasks["⚡ Map / Reduce Tasks<br/>(Containers #002, #003)<br/>• In-Container Execution"]
            JHS["📜 JobHistoryServer<br/>Port: 19888 (Web)<br/>• Historical Logs & Counters"]
            RM <-->|"Heartbeats & Allocations"| NM
            NM -->|"Launch"| AM
            AM -->|"Directs"| Tasks
            NM -->|"Aggregated Logs"| JHS
        end

        Tasks -.->|"Data Locality Read (128MB)"| DN
        Tasks -.->|"Write Results (part-r-00000)"| DN
    end

    subgraph Engines["⚡ ANALYTICS & PROCESSING ENGINES"]
        direction TB
        Spark["🔥 Apache Spark / PySpark<br/>(DataFrames & RDDs)"]
        MR["☕ Native Java MapReduce<br/>(Compiled JAR)"]
        StreamMR["🐍 Python Streaming<br/>(mapper.py | reducer.py)"]
        HDFSCLI["📁 Interactive HDFS CLI<br/>(hdfs dfs -put / -ls)"]
    end

    subgraph Volumes["💾 DOCKER NAMED VOLUMES (Persistent Host Storage)"]
        direction LR
        V_NN["📁 hadoop_namenode_data<br/>/usr/local/hadoop/hdfs/namenode"]
        V_DN["🧱 hadoop_datanode_data<br/>/usr/local/hadoop/hdfs/datanode"]
        V_TMP["📦 hadoop_tmp_data<br/>/app/hadoop/tmp"]
        V_LOG["📜 hadoop_logs_data<br/>/usr/local/hadoop/logs"]
    end

    Host ==>|"① Submit Job & Ingest Data"| RM & NN
    Engines ==>|"Submit Applications"| RM
    NN ==>|"Persist Inode Metadata"| V_NN
    DN ==>|"Persist 128MB Blocks"| V_DN
    YARN -.->|"Temp Spills & Tokens"| V_TMP
    Container -.->|"Daemon Event Logs"| V_LOG

    classDef hostStyle fill:#0c4a6e,stroke:#0284c7,stroke-width:2px,color:#ffffff;
    classDef hdfsStyle fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#ffffff;
    classDef yarnStyle fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#ffffff;
    classDef engineStyle fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#ffffff;
    classDef volStyle fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#ffffff;

    class DevUI,DevCLI,DevLaunch,DevSSH hostStyle;
    class NN,SNN,DN hdfsStyle;
    class RM,NM,AM,Tasks,JHS yarnStyle;
    class Spark,MR,StreamMR,HDFSCLI engineStyle;
    class V_NN,V_DN,V_TMP,V_LOG volStyle;
```

---

## 🌐 Web Interfaces & Port Mappings

All standard Hadoop web consoles and service endpoints are mapped to localhost:

| Service | Container Port | Host Port | Web Console URL | Description |
| :--- | :---: | :---: | :--- | :--- |
| **HDFS NameNode** | `9870` | `9870` | [http://localhost:9870](http://localhost:9870) | Browse HDFS filesystem, inspect cluster capacity, and view active DataNodes. |
| **YARN ResourceManager** | `8088` | `8088` | [http://localhost:8088](http://localhost:8088) | Monitor running applications, cluster memory/vcore metrics, and scheduler queues. |
| **HDFS DataNode** | `9864` | `9864` | [http://localhost:9864](http://localhost:9864) | Inspect DataNode volume status and raw block metrics. |
| **YARN NodeManager** | `8042` | `8042` | [http://localhost:8042](http://localhost:8042) | Container allocation and node execution details. |
| **MapReduce JobHistory** | `19888` | `19888` | [http://localhost:19888](http://localhost:19888) | Historical MapReduce task counters, logs, and execution timelines. |
| **HDFS RPC Endpoint** | `9000` | `9000` | `hdfs://localhost:9000` | IPC protocol endpoint for external tools (Spark, Flink, PySpark). |
| **SSH Daemon** | `22` | `22222` | `ssh -p 22222 hduser@localhost` | Direct SSH access (`password: ubuntu`). |
| **WSL 2 GUI Desktop** | `3390` | `3390` | `localhost:3390` (RDP) | XFCE4 graphical desktop session for WSL 2 (`Ubuntu-WSL-GUI.rdp`). |

> [!NOTE]
> Web consoles operate over plain HTTP (`http://`). If your browser auto-redirects to HTTPS, open an **Incognito / Private Window** using [http://127.0.0.1:9870](http://127.0.0.1:9870) or refer to [Troubleshooting Runbook: Issue 9](docs/troubleshooting.md#issue-9-browser-err_empty_response-localhost-didnt-send-any-data-on-web-uis).

---

## ⚡ 1-Click Quick Start

Choose your preferred deployment platform below:

<details open>
<summary><b>Option 1: Docker Compose (1-Click or CLI) - Recommended</b></summary>

### Via 1-Click Windows Launcher:
Double-click **[`launchers/windows/Start-Hadoop-Docker.bat`](launchers/windows/Start-Hadoop-Docker.bat)**.

### Via Terminal:
```bash
# Clone the repository
git clone https://github.com/Sohila-Khaled-Abbas/docker-hadoop.git
cd docker-hadoop

# Build and start container in background
docker compose up -d

# Check startup status and running daemons
docker compose ps
docker compose exec hadoop jps
```

To stop the cluster:
```bash
docker compose down
# or double-click launchers/windows/Stop-Hadoop-Docker.bat
```

</details>

<details>
<summary><b>Option 2: Kali Linux on VMware Workstation Pro</b></summary>

1. From Windows host, double-click **[`launchers/windows/Launch-Kali-VMware.bat`](launchers/windows/Launch-Kali-VMware.bat)** (tunes VMX for 6GB RAM, 4 vCPUs, disables WHPX popups, and launches VMware).
2. Inside Kali Linux terminal (`user: kali`, `pass: kali`):
   ```bash
   bash scripts/vmware/install-hadoop-kali.sh
   ```
3. Read the complete [Kali Linux & VMware Guide](docs/kali-vmware-hadoop-guide.md).

</details>

<details>
<summary><b>Option 3: Microsoft Hyper-V Generation 2 (Ubuntu)</b></summary>

1. Double-click **[`launchers/windows/Fix-Lag-And-Start-VM.bat`](launchers/windows/Fix-Lag-And-Start-VM.bat)** to allocate 4 vCPUs and launch the VM.
2. If internet connection is lost, double-click **[`launchers/windows/Fix-VM-Internet.bat`](launchers/windows/Fix-VM-Internet.bat)**.
3. To enable clipboard & full-screen resizing, run **[`launchers/windows/Eject-ISO-And-Enable-Clipboard.bat`](launchers/windows/Eject-ISO-And-Enable-Clipboard.bat)**.
4. Read the complete [Hyper-V Ubuntu Guide](docs/hyperv-ubuntu-guide.md).

</details>

<details>
<summary><b>Option 4: WSL 2 Ubuntu with Visual XFCE4 GUI</b></summary>

1. Inside WSL 2 Ubuntu terminal:
   ```bash
   bash scripts/wsl/install-hadoop-wsl.sh
   ```
2. Double-click **[`launchers/windows/Ubuntu-WSL-GUI.rdp`](launchers/windows/Ubuntu-WSL-GUI.rdp)** to connect to the desktop interface on `localhost:3390`.
3. Start the Hadoop cluster with `bash scripts/wsl/start-hadoop-cluster.sh`.
4. Read the complete [WSL 2 Ubuntu GUI Guide](docs/wsl2-ubuntu-hadoop-guide.md).

</details>

<details>
<summary><b>Option 5: Oracle VirtualBox Automated Setup</b></summary>

1. Run the automated PowerShell VM creator:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\virtualbox\virtualbox-setup.ps1
   ```
2. SSH into the VM: `ssh -p 2222 hadoopuser@localhost` (password: `hadoopuser`).
3. Read the complete [VirtualBox Ubuntu Guide](docs/virtualbox-ubuntu-guide.md).

</details>

---

## 🔬 Data Engineering Tutorials

### 1. Interactive HDFS CLI Operations
Run the comprehensive HDFS operations walkthrough inside the container:
```bash
docker compose exec hadoop bash < examples/hdfs-cli/demo-hdfs-operations.sh
```
*Read the [HDFS CLI Tutorial](examples/hdfs-cli/README.md) for complete command examples.*

### 2. Python Hadoop Streaming WordCount
Execute mapper/reducer streaming pipeline on sample text:
```bash
make test-mr-python
# or
bash examples/mapreduce-python/run.sh
```
*Read the [Python Streaming Guide](examples/mapreduce-python/README.md).*

### 3. Native Java MapReduce WordCount
Compile and execute standalone Java MapReduce job:
```bash
make test-mr-java
# or
bash examples/mapreduce-java/compile-and-run.sh
```
*Read the [Java MapReduce Guide](examples/mapreduce-java/README.md).*

### 4. Apache Spark & PySpark HDFS Integration
```bash
python examples/spark-pyspark/pyspark_hdfs_read_write.py
```
*Read the [PySpark Integration Guide](examples/spark-pyspark/README.md).*

---

## 📊 Sample Datasets

The repository includes pre-built test datasets in [`datasets/`](datasets/):

| Dataset | Format | Path | Purpose |
| :--- | :---: | :--- | :--- |
| **Text Corpus** | `.txt` | [`datasets/wordcount-sample.txt`](datasets/wordcount-sample.txt) | WordCount benchmarking, tokenization, grep |
| **Employees Data** | `.csv` | [`datasets/employees.csv`](datasets/employees.csv) | PySpark DataFrames, aggregations, SQL queries |

To load them directly into HDFS:
```bash
docker cp datasets/employees.csv hadoop-master:/tmp/
docker compose exec hadoop hdfs dfs -mkdir -p /datasets
docker compose exec hadoop hdfs dfs -put -f /tmp/employees.csv /datasets/
docker compose exec hadoop hdfs dfs -cat /datasets/employees.csv
```
*See [Datasets Documentation](datasets/README.md) for advanced ingestion recipes.*

---

## 📁 Repository Structure

```text
docker-hadoop/
├── .github/
│   ├── ISSUE_TEMPLATE/          # Bug report & feature templates
│   ├── workflows/
│   │   ├── ci.yml               # Automated GitHub Actions build & test CI
│   │   ├── security-scan.yml    # Hadolint Docker linter & Trivy vulnerability scanner
│   │   └── release-drafter.yml  # Automated release notes drafter
│   ├── dependabot.yml           # Automated dependency updates
│   ├── pull_request_template.md # PR guidelines template
│   └── release-drafter.yml      # Release draft configuration
├── config/                      # Core XML configurations
│   ├── core-site.xml            # Filesystem & temporary storage configuration
│   ├── hadoop-env.sh            # Environment exports & JVM options
│   ├── hdfs-site.xml            # NameNode, DataNode & replication settings
│   ├── mapred-site.xml          # MapReduce framework & JobHistory configuration
│   └── yarn-site.xml            # YARN ResourceManager & NodeManager settings
├── datasets/                    # Built-in sample datasets
│   ├── employees.csv            # Structured employee records for Spark/SQL
│   ├── wordcount-sample.txt     # Distributed systems text corpus
│   └── README.md                # HDFS loading instructions & recipes
├── docs/                        # Comprehensive technical documentation
│   ├── architecture.md          # Internal architecture & sequence diagrams
│   ├── configuration-tuning.md  # XML tuning & JVM GC optimization
│   ├── data-engineering-patterns.md # Lakehouse, Medallion, & join patterns
│   ├── ecosystem-integration.md # Spark, Hive, Presto, & Jupyter guides
│   ├── getting-started.md       # Fast onboarding guide
│   ├── hyperv-ubuntu-guide.md   # Microsoft Hyper-V setup & optimization
│   ├── kali-vmware-hadoop-guide.md # VMware Workstation & Kali Linux guide
│   ├── mapreduce-guide.md       # Comprehensive MapReduce manual
│   ├── software-engineering-practices.md # 12-factor Big Data & DevOps
│   ├── troubleshooting.md       # Diagnostic runbook for cluster issues
│   ├── virtualbox-ubuntu-guide.md # Oracle VirtualBox guide
│   └── wsl2-ubuntu-hadoop-guide.md# WSL 2 Ubuntu GUI & Hadoop setup
├── examples/                    # Hands-on Big Data examples
│   ├── hdfs-cli/                # Interactive HDFS CLI demonstration & guide
│   │   ├── demo-hdfs-operations.sh
│   │   └── README.md
│   ├── mapreduce-java/          # Standalone Java WordCount application
│   │   ├── WordCount.java
│   │   ├── compile-and-run.sh
│   │   └── README.md
│   ├── mapreduce-python/        # Python Hadoop Streaming example
│   │   ├── mapper.py
│   │   ├── reducer.py
│   │   ├── run.sh
│   │   ├── sample.txt
│   │   └── README.md
│   └── spark-pyspark/           # PySpark HDFS read/write integration
│       ├── pyspark_hdfs_read_write.py
│       └── README.md
├── launchers/                   # Standalone 1-Click platform launchers
│   ├── README.md                # Launcher catalog and usage guide
│   └── windows/                 # Windows 1-click desktop batch launchers
│       ├── Start-Hadoop-Docker.bat # 1-Click Docker cluster startup
│       ├── Stop-Hadoop-Docker.bat  # 1-Click Docker cluster shutdown
│       ├── Launch-Kali-VMware.bat  # VMware Workstation Kali launcher
│       ├── Fix-Lag-And-Start-VM.bat# Hyper-V 4-vCPU & performance launcher
│       ├── Fix-VM-Internet.bat     # Hyper-V virtual switch network repair
│       ├── Eject-ISO-And-Enable-Clipboard.bat # Hyper-V ISO & clipboard setup
│       └── Ubuntu-WSL-GUI.rdp      # WSL 2 Remote Desktop profile
├── scripts/                     # Modular automation scripts
│   ├── README.md                # Script catalog and runtime architecture
│   ├── docker/                  # Docker container entrypoint & probes
│   │   ├── entrypoint.sh
│   │   ├── healthcheck.sh
│   │   └── test-cluster.sh
│   ├── vmware/                  # VMware & Kali Linux automation
│   │   ├── install-hadoop-kali.sh
│   │   ├── optimize-kali-vmx.ps1
│   │   ├── apply-guest-mouse-fix.ps1
│   │   ├── fix-mouse-in-guest.sh
│   │   └── set-fullscreen-resolution.ps1
│   ├── hyperv/                  # Hyper-V host & guest automation
│   │   ├── configure-hyperv-host-enhanced-session.ps1
│   │   ├── enable-hyperv-enhanced-session.sh
│   │   ├── fix-vm-internet.ps1
│   │   └── optimize-hyperv-vm.ps1
│   ├── virtualbox/              # VirtualBox VM provisioning
│   │   └── virtualbox-setup.ps1
│   ├── wsl/                     # WSL 2 Ubuntu automation
│   │   ├── install-hadoop-wsl.sh
│   │   ├── start-hadoop-cluster.sh
│   │   ├── sync-wsl-configs.sh
│   │   └── fix-xrdp.sh
│   └── linux/                   # Bare-metal & native Linux scripts
│       ├── install-hadoop-ubuntu.sh
│       ├── install-hadoop-user.sh
│       ├── setup-hadoop-systemd.sh
│       └── start-daemons-direct.sh
├── .dockerignore                # Docker build exclusions
├── .env.example                 # Port and environment variable templates
├── .gitignore                   # Git exclusions (ISOs, 7z, and VM disks ignored)
├── CHANGELOG.md                 # Semantic version history
├── CODE_OF_CONDUCT.md           # Community code of conduct
├── CONTRIBUTING.md              # Guidelines for contributing
├── Dockerfile                   # Multi-stage Ubuntu 20.04 Hadoop 3.1.2 image
├── docker-compose.yml           # Multi-volume container orchestration
├── LICENSE                      # Apache 2.0 License
├── Makefile                     # Developer CLI shortcuts
├── README.md                    # Project documentation
└── SECURITY.md                  # Security policies & vulnerability reporting
```

---

## 🛠️ Developer Command Shortcuts (`Makefile`)

| Command | Description |
| :--- | :--- |
| `make help` | Display available developer CLI commands |
| `make build` | Build the Hadoop Docker image locally |
| `make up` | Start the Hadoop Docker cluster in background |
| `make down` | Stop and remove the Docker container |
| `make restart` | Restart the cluster services |
| `make logs` | Stream container logs in real time |
| `make ps` | Inspect container health status |
| `make jps` | List running Java daemons inside the container |
| `make test` | Run built-in integration tests & Pi MapReduce |
| `make test-mr-python` | Run Python Streaming MapReduce WordCount |
| `make test-mr-java` | Compile & run Java Native MapReduce WordCount |
| `make test-hdfs-cli` | Run HDFS CLI interactive demo script |
| `make safemode-leave` | Force HDFS NameNode to leave SafeMode |
| `make hdfs-report` | Display HDFS storage capacity report |
| `make bash` | Open root shell inside the container |
| `make hdfs-shell` | Open interactive shell as `hduser` |
| `make clean` | Full teardown (removes containers, images, and named volumes) |
| `make vm-create` | Create & configure Ubuntu VM in Oracle VirtualBox |
| `make vm-start` | Start VirtualBox VM in GUI window |
| `make vm-ssh` | Connect to VirtualBox VM via SSH (`port 2222`) |
| `make vm-kali-optimize` | Tune Kali VMX hardware specs (6GB RAM, 4 vCPUs) |
| `make vm-kali-start` | Launch Kali Linux in VMware Workstation |

---

## 🤝 Contributing & Community

Contributions are warmly welcomed! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
