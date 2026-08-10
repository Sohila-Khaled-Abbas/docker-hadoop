# Apache Hadoop 3.1.2 Single-Node Cluster on Docker

[![Docker Build & Test CI](https://github.com/your-username/docker-hadoop/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/docker-hadoop/actions/workflows/ci.yml)
[![Apache Hadoop](https://img.shields.io/badge/Apache%20Hadoop-3.1.2-66CCFF?logo=apache)](https://hadoop.apache.org/)
[![Java](https://img.shields.io/badge/Java-OpenJDK%208-ED8B00?logo=openjdk)](https://openjdk.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A production-grade, standalone single-node **Apache Hadoop 3.1.2** cluster running in Docker. Perfect for local development, big data education, testing HDFS commands, running MapReduce jobs, and integrating with Spark, Hive, or Pig.

---

## 🚀 Features

- **Apache Hadoop 3.1.2** & **OpenJDK 8** pre-installed and configured.
- **Complete Daemon Stack**:
  - **HDFS**: NameNode, DataNode, SecondaryNameNode.
  - **YARN**: ResourceManager, NodeManager.
  - **MapReduce**: JobHistory Server.
- **Security & Best Practices**:
  - Non-root execution under dedicated `hduser` user and `hadoop` group.
  - Pre-configured passwordless SSH.
- **Persistent Data**: Named Docker volumes for HDFS NameNode metadata, DataNode blocks, temp data, and logs.
- **Healthchecks**: Built-in container health checks and automated CI testing.
- **Web UIs**: All standard Hadoop 3 web consoles exposed on host ports.

---

## 🌐 Web Interfaces & Port Mappings

| Service | Port | Web UI URL | Description |
| :--- | :--- | :--- | :--- |
| **HDFS NameNode** | `9870` | [http://localhost:9870](http://localhost:9870) | Browse HDFS filesystem, check cluster storage capacity and active DataNodes. |
| **HDFS DataNode** | `9864` | [http://localhost:9864](http://localhost:9864) | DataNode status, block information, and storage statistics. |
| **YARN ResourceManager** | `8088` | [http://localhost:8088](http://localhost:8088) | View running applications, memory/vcore metrics, and node status. |
| **YARN NodeManager** | `8042` | [http://localhost:8042](http://localhost:8042) | NodeManager status and container allocations. |
| **MapReduce JobHistory** | `19888` | [http://localhost:19888](http://localhost:19888) | Historical MapReduce job logs and analytics. |
| **HDFS RPC** | `9000` | `hdfs://localhost:9000` | IPC communication endpoint for clients and APIs. |
| **SSH Daemon** | `2222` | `ssh -p 2222 hduser@localhost` | Direct SSH access (password: `ubuntu`). |

---

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/docker-hadoop.git
cd docker-hadoop
```

### 2. Start the Cluster

Using **Docker Compose**:
```bash
docker compose up -d
```

Or using **Make**:
```bash
make up
```

### 3. Check Running Services

```bash
docker compose ps
```

To see running Java daemons inside the container:
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

Run the built-in automated test suite:
```bash
make test
# or
docker compose exec hadoop /test-cluster.sh
```

### Manual Verification: Calculate Pi with MapReduce

```bash
docker compose exec hadoop yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 2 5
```

---

## 💻 HDFS CLI Usage Examples

Open an interactive shell inside the container:
```bash
docker compose exec -it hadoop bash
```

Run HDFS commands:
```bash
# List root directory
hdfs dfs -ls /

# Create a new directory
hdfs dfs -mkdir -p /user/mydata

# Upload a local file to HDFS
hdfs dfs -put /usr/local/hadoop/etc/hadoop/core-site.xml /user/mydata/

# View file contents in HDFS
hdfs dfs -cat /user/mydata/core-site.xml

# Check HDFS storage report
hdfs dfsadmin -report
```

---

## 📁 Repository Structure

```
docker-hadoop/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated GitHub Actions CI workflow
├── config/
│   ├── core-site.xml           # HDFS core configuration
│   ├── hdfs-site.xml           # HDFS NameNode / DataNode parameters
│   ├── mapred-site.xml         # MapReduce on YARN & JobHistory server config
│   ├── yarn-site.xml           # YARN ResourceManager & NodeManager config
│   └── hadoop-env.sh           # Java & Hadoop runtime environment variables
├── scripts/
│   ├── entrypoint.sh           # Container bootstrap & daemon orchestration
│   ├── healthcheck.sh          # Container health check script
│   └── test-cluster.sh         # MapReduce & HDFS integration tests
├── .dockerignore               # Docker build exclusions
├── .env.example                # Configuration template
├── .gitignore                  # Git exclusions
├── Dockerfile                  # Multi-stage Ubuntu 20.04 Hadoop 3 image
├── docker-compose.yml          # Container orchestration with volumes & ports
├── LICENSE                     # Apache 2.0 License
├── Makefile                    # Developer CLI commands
└── README.md                   # Project documentation
```

---

## 🛠️ Management & Automation Commands

| Command | Description |
| :--- | :--- |
| `make build` | Build the Hadoop Docker image |
| `make up` | Start the cluster in detached mode |
| `make down` | Stop and remove the cluster container |
| `make restart` | Restart the cluster services |
| `make logs` | Stream container logs |
| `make ps` | Check container status |
| `make test` | Run integration tests |
| `make bash` | Open interactive shell |
| `make clean` | Stop and remove containers, volumes, and images |

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
