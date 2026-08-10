# Getting Started with Apache Hadoop on Docker

This guide walks you through setting up, verifying, configuring, and interacting with your single-node Apache Hadoop 3.1.2 cluster in Docker.

---

## 📑 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Verifying Cluster Health](#verifying-cluster-health)
- [Accessing Web Consoles](#accessing-web-consoles)
- [Essential HDFS Commands](#essential-hdfs-commands)
- [Running MapReduce Jobs](#running-mapreduce-jobs)
- [Stopping & Resetting the Cluster](#stopping--resetting-the-cluster)

---

## 💻 System Requirements

| Resource | Minimum | Recommended |
| :--- | :--- | :--- |
| **Operating System** | Linux, macOS, Windows 10/11 (WSL2) | Ubuntu 22.04+ / macOS 14+ |
| **Docker Engine** | 20.10.0+ | 24.0.0+ |
| **Docker Compose** | 2.0.0+ | 2.20.0+ |
| **RAM** | 4 GB | 8 GB+ |
| **Disk Space** | 5 GB free | 10 GB+ free |

---

## 🚀 Quick Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sohila-Khaled-Abbas/docker-hadoop.git
cd docker-hadoop
```

### Step 2: (Optional) Configure Environment Variables

You can customize port allocations and container names by copying `.env.example` to `.env`:

```bash
cp .env.example .env
```

### Step 3: Build and Launch

Using **Docker Compose**:

```bash
docker compose up -d
```

Or using **Make**:

```bash
make up
```

---

## 🩺 Verifying Cluster Health

### 1. Check Container Status

```bash
docker compose ps
```

The status should display `healthy` once the 40-second startup initialization period finishes.

### 2. Verify Running Java Daemons

Execute `jps` inside the container:

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

> [!NOTE]
> If any of the daemons are missing (e.g. `DataNode` or `ResourceManager`), check the logs with `docker compose logs hadoop --tail 100` or review the [Troubleshooting Guide](troubleshooting.md).

---

## 🌐 Accessing Web Consoles

Once the cluster is running, open the following endpoints in your browser:

| Interface | URL | What to look for |
| :--- | :--- | :--- |
| **HDFS NameNode** | [http://localhost:9870](http://localhost:9870) | Live nodes (`1`), Cluster Capacity, Browse Directory (`Utilities > Browse the file system`) |
| **HDFS DataNode** | [http://localhost:9864](http://localhost:9864) | Volume Information, DataNode status |
| **YARN ResourceManager** | [http://localhost:8088](http://localhost:8088) | Active Nodes (`1`), Cluster Metrics (Memory Total: `8192 MB`, VCores: `8`), Application Queue |
| **YARN NodeManager** | [http://localhost:8042](http://localhost:8042) | Container health, Node details |
| **MapReduce JobHistory** | [http://localhost:19888](http://localhost:19888) | Retired / Completed jobs and task execution logs |

---

## 💻 Essential HDFS Commands

You can interact with HDFS using `docker compose exec hadoop hdfs dfs <command>` or by opening an interactive shell:

```bash
# Open interactive shell
docker compose exec -it hadoop bash
```

### Common Commands Reference

```bash
# 1. List directory contents
hdfs dfs -ls /

# 2. Create a new directory
hdfs dfs -mkdir -p /user/mydata

# 3. Upload a file to HDFS
hdfs dfs -put /usr/local/hadoop/etc/hadoop/core-site.xml /user/mydata/

# 4. View file content from HDFS
hdfs dfs -cat /user/mydata/core-site.xml | head -n 20

# 5. Download a file from HDFS to local container filesystem
hdfs dfs -get /user/mydata/core-site.xml /tmp/downloaded-core-site.xml

# 6. Check file and directory sizes in human-readable format
hdfs dfs -du -h /user

# 7. Remove file from HDFS
hdfs dfs -rm /user/mydata/core-site.xml

# 8. Remove directory recursively
hdfs dfs -rm -r /user/mydata

# 9. Check cluster storage report and alive DataNodes
hdfs dfsadmin -report
```

---

## 🧪 Running MapReduce Jobs

### 1. Calculate Pi (Monte Carlo Estimation)

Run the built-in MapReduce example:

```bash
docker compose exec hadoop yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 4 1000
```

Output:

```text
Estimated value of Pi is 3.14150000000000000000
```

### 2. Run Automated Test Suite

```bash
make test
# or
docker compose exec hadoop /test-cluster.sh
```

---

## 🛑 Stopping & Resetting the Cluster

### Stop Container (Preserve Data)

```bash
make down
# or
docker compose down
```

### Full Teardown & Volume Reset (Deletes HDFS Data)

```bash
make clean
# or
docker compose down -v --rmi all
```
