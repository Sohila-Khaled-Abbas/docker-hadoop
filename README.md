<div align="center">

# 🐘 Apache Hadoop 3.1.2 Single-Node Cluster on Docker

### *Production-grade, fully configured Big Data environment for local development, education, and distributed processing.*

[![Docker Build & Test CI](https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/ci.yml/badge.svg)](https://github.com/Sohila-Khaled-Abbas/docker-hadoop/actions/workflows/ci.yml)
[![Apache Hadoop](https://img.shields.io/badge/Apache%20Hadoop-3.1.2-66CCFF?logo=apache&logoColor=white)](https://hadoop.apache.org/)
[![Java](https://img.shields.io/badge/Java-OpenJDK%208-ED8B00?logo=openjdk&logoColor=white)](https://openjdk.org/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04%20LTS-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v3.8-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Quick Start](#-quick-start) • [Architecture](#-system-architecture) • [Web Interfaces](#-web-interfaces--port-mappings) • [MapReduce Tutorials](#-mapreduce-tutorials) • [Documentation](#-in-depth-documentation) • [Troubleshooting](#-troubleshooting--faq)

</div>

---

## 📖 Overview

This repository provides a containerized, single-node **Apache Hadoop 3.1.2** cluster running on **Ubuntu 20.04** with **OpenJDK 8**. It includes the complete distributed daemon stack (HDFS, YARN, MapReduce JobHistory), non-root execution (`hduser`), automated health checks, persistent volume management, and hands-on examples for Java and Python Hadoop Streaming.

Ideal for:

- 🎓 **Big Data Education & Academic Courses**: Learn HDFS, YARN, and MapReduce internals without multi-machine cluster overhead.
- 🧪 **Local ETL & Algorithm Prototyping**: Test MapReduce jobs and HDFS storage pipelines locally before deploying to AWS EMR, GCP Dataproc, or on-premise clusters.
- 🔌 **Ecosystem Integration**: Seamlessly connect **Apache Spark**, **PySpark**, **Apache Hive**, **Presto / Trino**, and **Jupyter Notebooks** to HDFS.

---

## 🚀 Key Features

- **Complete Hadoop 3.1.2 Daemon Stack**:
  - **HDFS**: NameNode, DataNode, SecondaryNameNode.
  - **YARN**: ResourceManager, NodeManager.
  - **MapReduce**: JobHistory Server.
- **Enterprise Best Practices & Hardening**:
  - Secure non-root daemon execution under dedicated `hduser:hadoop` (UID/GID 1000).
  - Centralized `/etc/profile.d/hadoop.sh` and multi-shell profile exports (`.bashrc`, `.profile`) for seamless environment and PATH resolution.
  - Pre-configured passwordless SSH loopback keys with strict permission masks (`0600`/`0700`).
- **Optimized Multi-Stage Build**:
  - Automated pruning of ~60,000 redundant Javadoc/API HTML files to bypass WSL2/ext4 inode journal bottlenecks and accelerate build times.
- **Data Persistence**:
  - 4 named Docker volumes isolating NameNode metadata, DataNode blocks, temporary workspaces, and logs.
- **Automated Health Monitoring**:
  - Docker Compose container health checks querying Web UI endpoints and HDFS status.
  - GitHub Actions automated CI workflow validating builds, daemons, and MapReduce execution.
- **Developer Experience**:
  - Ready-to-run Java and Python Streaming MapReduce examples with one-click test runners.
  - Extensive `Makefile` shortcuts for all common lifecycle tasks.

---

## 🏛️ System Architecture

<p align="center">
  <img src="docs/images/hadoop-data-engineering-infographic.png" alt="Apache Hadoop Modern Big Data Engineering and Software Engineering Architecture" width="95%" />
</p>

```mermaid
graph TB
    subgraph Host["Host Machine"]
        Browser["Web Browser & Clients"]
        subgraph Volumes["Docker Named Volumes"]
            V_NN["hadoop_namenode_data<br/>(FSImage & Edits)"]
            V_DN["hadoop_datanode_data<br/>(HDFS Blocks)"]
            V_TMP["hadoop_tmp_data<br/>(/app/hadoop/tmp)"]
            V_LOG["hadoop_logs_data<br/>(/usr/local/hadoop/logs)"]
        end
    end

    subgraph Container["Hadoop Docker Container (hadoop-master)"]
        subgraph StorageLayer["HDFS Storage Layer"]
            NN["NameNode<br/>:9870 (Web) / :9000 (RPC)"]
            DN["DataNode<br/>:9864 (Web) / :9866 (Data)"]
            SNN["SecondaryNameNode<br/>:9868 (Web)"]
        end

        subgraph ComputeLayer["YARN Compute Layer"]
            RM["ResourceManager<br/>:8088 (Web)"]
            NM["NodeManager<br/>:8042 (Web)"]
            JHS["JobHistoryServer<br/>:19888 (Web)"]
        end

        SSHD["OpenSSH Daemon (:22222)"]
    end

    Browser -->|HTTP :9870| NN
    Browser -->|HTTP :9864| DN
    Browser -->|HTTP :8088| RM
    Browser -->|HTTP :8042| NM
    Browser -->|HTTP :19888| JHS
    Browser -->|RPC :9000| NN
    Browser -->|SSH :22222| SSHD

    NN <-->|Heartbeats & Block Reports| DN
    NN <-->|Checkpoints| SNN
    RM <-->|Container Allocations| NM

    NN -.->|Persist| V_NN
    DN -.->|Persist| V_DN
    StorageLayer -.->|Temp Files| V_TMP
    ComputeLayer -.->|Logs| V_LOG
```

> [!NOTE]
> For detailed architectural specifications, HDFS read/write pipelines, and YARN scheduling lifecycles, see the [Architecture Documentation](docs/architecture.md). Also check our [Big Data Engineering Patterns Guide](docs/data-engineering-patterns.md) and [Software Engineering Best Practices](docs/software-engineering-practices.md).

---

## 🌐 Web Interfaces & Port Mappings

All standard Apache Hadoop web consoles and service endpoints are mapped to host ports:

| Service | Container Port | Host Port | Web Console URL | Description |
| :--- | :---: | :---: | :--- | :--- |
| **HDFS NameNode** | `9870` | `9870` | [http://localhost:9870](http://localhost:9870) | Browse HDFS filesystem, inspect cluster capacity, and view active DataNodes. |
| **HDFS DataNode** | `9864` | `9864` | [http://localhost:9864](http://localhost:9864) | DataNode status, block storage details, and volume metrics. |
| **YARN ResourceManager** | `8088` | `8088` | [http://localhost:8088](http://localhost:8088) | View running applications, memory/vcore metrics, and node queues. |
| **YARN NodeManager** | `8042` | `8042` | [http://localhost:8042](http://localhost:8042) | NodeManager status and container allocations. |
| **MapReduce JobHistory** | `19888` | `19888` | [http://localhost:19888](http://localhost:19888) | Historical MapReduce job logs, execution counters, and analytics. |
| **HDFS RPC Endpoint** | `9000` | `9000` | `hdfs://localhost:9000` | Client IPC protocol endpoint for external tools (Spark, Flink, PySpark). |
| **SSH Daemon** | `22` | `22222` | `ssh -p 22222 hduser@localhost` | Direct SSH access (`password: ubuntu`). |

> [!TIP]
> You can customize all external port numbers by editing `.env` or setting environment variables (e.g. `HADOOP_NAMENODE_PORT=19870`).

> [!NOTE]
> Web consoles operate over plain HTTP (`http://`). If your browser displays `ERR_EMPTY_RESPONSE` or auto-redirects to HTTPS, access the dashboard in an **Incognito / Private Window** using [http://127.0.0.1:9870](http://127.0.0.1:9870) or see [Troubleshooting Guide: Issue 9](docs/troubleshooting.md#issue-9-browser-err_empty_response-localhost-didnt-send-any-data-on-web-uis).

---

## ⚡ Quick Start

### Prerequisites

- [Docker Engine](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)

### 1. Clone the Repository

```bash
git clone https://github.com/Sohila-Khaled-Abbas/docker-hadoop.git
cd docker-hadoop
```

### 2. Start the Cluster

<details open>
<summary><b>Option A: Using Docker Compose</b></summary>

```bash
# Build and start container in background
docker compose up -d

# Check startup status
docker compose ps
```

</details>

<details>
<summary><b>Option B: Using Make</b></summary>

```bash
# Build and start container in background
make up

# Check status
make ps
```

</details>

### 3. Verify Daemon Status

Verify that all 6 Java daemons are running:

```bash
docker compose exec hadoop jps
```

Expected output:

```text
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
JobHistoryServer
Jps
```

---

## 🧪 Testing & Verification

Run the automated integration suite:

```bash
make test
# or
docker compose exec hadoop /test-cluster.sh
```

### Calculate Pi with MapReduce (Monte Carlo Estimation)

```bash
docker compose exec hadoop yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 4 1000
```

---

## 💻 HDFS CLI Cheat Sheet

Open an interactive shell inside the container:

```bash
docker compose exec -it hadoop bash
```

| Operation | Command |
| :--- | :--- |
| **List Root Directory** | `hdfs dfs -ls /` |
| **Create Directory** | `hdfs dfs -mkdir -p /user/mydata` |
| **Upload Local File** | `hdfs dfs -put /path/to/local/file.txt /user/mydata/` |
| **Download File** | `hdfs dfs -get /user/mydata/file.txt /tmp/` |
| **Display File Content** | `hdfs dfs -cat /user/mydata/file.txt \| head -n 20` |
| **Check Storage Disk Usage** | `hdfs dfs -du -h /user` |
| **Delete File** | `hdfs dfs -rm /user/mydata/file.txt` |
| **Delete Directory (Recursive)** | `hdfs dfs -rm -r /user/mydata` |
| **HDFS Health Report** | `hdfs dfsadmin -report` |
| **Exit SafeMode** | `hdfs dfsadmin -safemode leave` |

---

## 🔬 MapReduce Tutorials

### 1. Python Hadoop Streaming WordCount

Run the Python streaming example using the pre-configured runner:

```bash
make test-mr-python
# or
bash examples/mapreduce-python/run.sh
```

*Read the full [Python Streaming Guide](examples/mapreduce-python/README.md).*

### 2. Java Native MapReduce WordCount

Compile and execute the standalone Java WordCount application:

```bash
make test-mr-java
# or
bash examples/mapreduce-java/compile-and-run.sh
```

*Read the full [Java MapReduce Guide](examples/mapreduce-java/README.md).*

---

## 🔌 Big Data Ecosystem Integration

Connect external data processing frameworks directly to this cluster:

```python
# PySpark HDFS Connection Example
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HadoopDockerDemo") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    .getOrCreate()

df = spark.read.parquet("hdfs://localhost:9000/data/spark_employees.parquet")
df.show()
```

*See [Ecosystem Integration Guide](docs/ecosystem-integration.md) for Apache Spark, Apache Hive, Presto/Trino, and Jupyter Notebook setup instructions.*

---

## 💾 Storage & Persistent Volumes

Cluster state is preserved across container lifecycles via named Docker volumes:

| Docker Volume Name | Container Mount Path | Description |
| :--- | :--- | :--- |
| `hadoop_namenode_data` | `/usr/local/hadoop/yarn_data/hdfs/namenode` | NameNode metadata, `fsimage`, and transaction edit logs. |
| `hadoop_datanode_data` | `/usr/local/hadoop/yarn_data/hdfs/datanode` | DataNode HDFS block storage. |
| `hadoop_tmp_data` | `/app/hadoop/tmp` | Hadoop intermediate temporary files. |
| `hadoop_logs_data` | `/usr/local/hadoop/logs` | Daemon log files and historical application logs. |

> [!WARNING]
> To perform a clean cluster reset and reformat the NameNode from scratch, run `make clean` or `docker compose down -v`.

---

## 📚 In-Depth Documentation

| Guide | Description |
| :--- | :--- |
| 📖 [Getting Started Guide](docs/getting-started.md) | Step-by-step installation, verification, and first steps. |
| 🏛️ [Architecture Blueprint](docs/architecture.md) | Complete internal architecture, HDFS pipelines, and Mermaid diagrams. |
| ⚙️ [MapReduce Developer Guide](docs/mapreduce-guide.md) | Java & Python MapReduce development, Combiners, and memory tuning. |
| 🔌 [Ecosystem Integration Guide](docs/ecosystem-integration.md) | Connecting Apache Spark, Hive, Presto/Trino, and Jupyter to HDFS. |
| 🛠️ [Troubleshooting Runbook](docs/troubleshooting.md) | Solutions for SafeMode, ClusterID mismatch, memory limits, and port conflicts. |
| 🚀 [Configuration & Performance Tuning](docs/configuration-tuning.md) | XML configuration parameters, JVM heap sizing, and optimization. |

---

## 🛠️ Troubleshooting & FAQ

<details>
<summary><b>Q: NameNode is stuck in SafeMode (<code>Cannot create file... Name node is in safe mode</code>)</b></summary>

**Fix**: Execute the following command to manually exit SafeMode:

```bash
make safemode-leave
# or
docker compose exec hadoop hdfs dfsadmin -safemode leave
```

</details>

<details>
<summary><b>Q: DataNode is missing or <code>clusterID</code> mismatch occurs</b></summary>

**Fix**: When NameNode is formatted without wiping DataNode storage, the IDs diverge. Perform a full volume reset:

```bash
make clean
make up
```

</details>

<details>
<summary><b>Q: Host port conflict (e.g. port 9870 or 8088 already in use)</b></summary>

**Fix**: Create a `.env` file and change the conflicting port mappings:

```bash
cp .env.example .env
# Edit .env and change HADOOP_NAMENODE_PORT=19870
docker compose up -d
```

</details>

*For more solutions, see the [Troubleshooting Runbook](docs/troubleshooting.md).*

---

## 📚 In-Depth Documentation & Guides

Explore specialized technical guides tailored for Data Engineers and Software Engineers:

| Guide | Description | Key Focus Areas |
| :--- | :--- | :--- |
| [🏗️ **Data Engineering Patterns**](docs/data-engineering-patterns.md) | Architectural patterns for high-throughput distributed data pipelines. | Lakehouse / Medallion Architecture, Parquet vs ORC vs Avro, Map-Side Joins, Small Files solutions, WAP pattern, PySpark ETL. |
| [🛠️ **Software Engineering Practices**](docs/software-engineering-practices.md) | Production engineering, containerization standards, and CI/CD. | 12-Factor Big Data, Tini init system, Zombie reaping, Signal propagation, Unit testing pipelines, JMX observability. |
| [🏛️ **System Architecture**](docs/architecture.md) | Complete Hadoop 3.1.2 topology blueprint and interaction lifecycles. | HDFS NameNode / DataNode RPC, YARN Scheduler, SecondaryNameNode Checkpointing, Network Port Matrix. |
| [⚡ **MapReduce Programming Guide**](docs/mapreduce-guide.md) | Comprehensive development guide for Java & Python Streaming. | Mapper/Reducer execution, Shuffle & Sort internals, Partitioner logic, In-Mapper Combiners, Streaming API. |
| [⚙️ **Configuration & JVM Tuning**](docs/configuration-tuning.md) | Complete XML parameter guide and JVM performance tuning. | Heap sizing, GC optimization, container vCore/RAM allocations, HDFS block sizing, speculative execution. |
| [🔌 **Ecosystem Integration**](docs/ecosystem-integration.md) | Connecting external Big Data and analytical compute engines. | Apache Spark / PySpark, Apache Hive Metastore, Presto / Trino SQL, Jupyter Notebooks. |
| [🔍 **Troubleshooting & Diagnostics**](docs/troubleshooting.md) | Operational runbook for diagnosing and resolving cluster failures. | Port conflicts, SafeMode deadlocks, DataNode clusterID divergence, OOM errors, Healthcheck debugging. |
| [🚀 **Getting Started Guide**](docs/getting-started.md) | Fast onboarding walkthrough for developers and researchers. | Prerequisites, step-by-step setup, cluster verification, CLI execution. |

---

## 📁 Repository Structure

```text
docker-hadoop/
├── .github/
│   ├── workflows/
│   │   └── ci.yml               # Automated GitHub Actions CI workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md        # Structured Bug Report template
│   │   ├── feature_request.md   # Structured Feature Proposal template
│   │   └── config.yml           # Issue template settings
│   └── pull_request_template.md # Standard PR checklist & description template
├── config/
│   ├── core-site.xml            # Default filesystem & temp storage parameters
│   ├── hdfs-site.xml            # HDFS NameNode / DataNode parameters
│   ├── mapred-site.xml          # MapReduce on YARN & JobHistory server config
│   ├── yarn-site.xml            # YARN ResourceManager & NodeManager config
│   └── hadoop-env.sh            # Java & Hadoop runtime environment variables
├── docs/
│   ├── architecture.md          # In-depth architectural blueprint & Mermaid diagrams
│   ├── configuration-tuning.md  # XML parameter reference & JVM tuning guide
│   ├── ecosystem-integration.md # Spark, Hive, Presto, and Jupyter integration
│   ├── getting-started.md       # Developer onboarding & operational guide
│   ├── mapreduce-guide.md       # Comprehensive MapReduce programming guide
│   └── troubleshooting.md       # Diagnostics & troubleshooting runbook
├── examples/
│   ├── mapreduce-java/          # Standalone Java WordCount with compile script
│   │   ├── WordCount.java
│   │   ├── compile-and-run.sh
│   │   └── README.md
│   ├── mapreduce-python/        # Python Hadoop Streaming WordCount example
│   │   ├── mapper.py
│   │   ├── reducer.py
│   │   ├── run.sh
│   │   ├── sample.txt
│   │   └── README.md
│   └── spark-pyspark/           # PySpark HDFS read/write integration example
│       ├── pyspark_hdfs_read_write.py
│       └── README.md
├── scripts/
│   ├── entrypoint.sh            # Container bootstrap & daemon orchestration
│   ├── healthcheck.sh           # Container health check script
│   └── test-cluster.sh          # MapReduce & HDFS integration tests
├── .dockerignore                # Docker build exclusions
├── .env.example                 # Configuration template
├── .gitignore                   # Git exclusions
├── CHANGELOG.md                 # Semantic version changelog
├── CODE_OF_CONDUCT.md           # Contributor Covenant Code of Conduct
├── CONTRIBUTING.md              # Development & contribution guidelines
├── Dockerfile                   # Multi-stage Ubuntu 20.04 Hadoop 3 image
├── docker-compose.yml           # Container orchestration with volumes & ports
├── LICENSE                      # Apache 2.0 License
├── Makefile                     # Developer CLI commands
├── README.md                    # Project documentation
└── SECURITY.md                  # Vulnerability reporting & container security
```

---

## 🛠️ Management & Automation Commands

| Command | Description |
| :--- | :--- |
| `make help` | Display list of available developer commands |
| `make build` | Build the Hadoop Docker image |
| `make up` | Start the cluster in detached mode |
| `make down` | Stop and remove the cluster container |
| `make restart` | Restart the cluster services |
| `make logs` | Stream container logs in real time |
| `make ps` | Check container health and running services |
| `make jps` | List running Hadoop Java daemons (`NameNode`, `DataNode`, etc.) |
| `make test` | Run built-in integration tests & Pi MapReduce |
| `make test-mr-python` | Run Python Hadoop Streaming WordCount job |
| `make test-mr-java` | Compile and run Java Native MapReduce WordCount job |
| `make safemode-leave` | Force HDFS NameNode to exit SafeMode |
| `make hdfs-report` | Display HDFS storage and DataNode health report |
| `make bash` | Open interactive shell inside the container |
| `make clean` | Stop and remove containers, images, and persistent volumes |

---

## 🤝 Contributing & Community

Contributions are welcome! Please review our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
