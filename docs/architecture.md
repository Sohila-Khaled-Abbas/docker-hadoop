# Apache Hadoop Docker Architecture

This document provides a comprehensive architectural overview of the single-node **Apache Hadoop 3.1.2** containerized cluster, detailing component interactions, daemons, HDFS storage pipelines, YARN scheduling mechanics, container filesystem hierarchy, and network topology.

---

## 📑 Table of Contents

- [System Architecture Overview](#system-architecture-overview)
- [Daemon Responsibilities](#daemon-responsibilities)
- [Storage & Volume Persistence Layout](#storage--volume-persistence-layout)
- [Container Startup & Initialization Flow](#container-startup--initialization-flow)
- [HDFS Data Pipelines](#hdfs-data-pipelines)
  - [HDFS File Write Lifecycle](#hdfs-file-write-lifecycle)
  - [HDFS File Read Lifecycle](#hdfs-file-read-lifecycle)
- [YARN MapReduce Job Execution Flow](#yarn-mapreduce-job-execution-flow)
- [Network & Port Topology](#network--port-topology)
- [Security & Process Execution Model](#security--process-execution-model)

---

## 🏛️ System Architecture Overview

<p align="center">
  <a href="images/hadoop-data-engineering-system-architecture.svg">
    <img src="images/hadoop-data-engineering-infographic.png" alt="Apache Hadoop Modern Big Data Engineering and Software Engineering Architecture" width="100%" />
  </a>
  <br/>
  <em>🔍 Click the diagram above to view the scalable, high-definition vector SVG version.</em>
</p>

The container orchestrates the complete Apache Hadoop 3.1.2 daemon stack inside an isolated Ubuntu 20.04 environment. It exposes all native Web UIs, RPC ports, and SSH endpoints to the host while persisting cluster state through named Docker volumes.

```mermaid
flowchart TB
    subgraph Host["💻 DEVELOPER HOST & CLIENT ACCESS LAYER"]
        direction LR
        DevUI["🌐 Web Consoles<br/>(:9870, :8088, :19888)"]
        DevCLI["💻 Terminal CLI<br/>(make / docker compose)"]
        DevLaunch["🚀 1-Click Launchers<br/>(launchers/windows/*.bat)"]
        DevSSH["🔑 SSH Client<br/>(:22222 hduser:ubuntu)"]
    end

    subgraph Container["🐳 DOCKER CONTAINER: hadoop-master (Ubuntu 20.04 / OpenJDK 8 / hduser:1000)"]
        direction TB

        subgraph HDFS["🗄️ DISTRIBUTED STORAGE LAYER (HDFS)"]
            direction TB
            NN["👑 NameNode (Master)<br/>Port: 9870 (Web) / 9000 (RPC)<br/>• Inodes Tree • FSImage • EditLog"]
            SNN["🔄 SecondaryNameNode (Checkpointer)<br/>Port: 9868 (HTTP)<br/>• Merges FSImage + Edits Checkpoints"]
            DN["📦 DataNode (Worker)<br/>Port: 9864 (Web) / 9866 (Data)<br/>• 128MB Blocks • CRC32C Checksums"]
            NN <-->|"Heartbeats (3s) & Block Reports"| DN
            NN <-->|"Checkpoint Sync"| SNN
        end

        subgraph YARN["⚙️ RESOURCE & COMPUTE ORCHESTRATION (YARN)"]
            direction TB
            RM["🧠 ResourceManager (Master)<br/>Port: 8088 (Web) / 8032 (IPC)<br/>• Capacity Scheduler • ApplicationsManager"]
            NM["👷 NodeManager (Worker)<br/>Port: 8042 (Web) / 8040 (IPC)<br/>• Container Allocation & cgroups Monitoring"]
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

## ⚙️ Daemon Responsibilities

| Daemon | Layer | Process Class | Primary Function |
| :--- | :--- | :--- | :--- |
| **NameNode** | HDFS | `org.apache.hadoop.hdfs.server.namenode.NameNode` | Master node for HDFS metadata. Tracks file hierarchy, directory namespace, block locations, and replication factors in memory and FSImage. |
| **DataNode** | HDFS | `org.apache.hadoop.hdfs.server.datanode.DataNode` | Slave storage node. Stores raw block data on disk, validates block checksums, and serves read/write requests from clients. |
| **SecondaryNameNode** | HDFS | `org.apache.hadoop.hdfs.server.namenode.SecondaryNameNode` | Periodically merges the NameNode's `fsimage` with edit logs (`edits_inprogress`) to prevent edit log growth and expedite NameNode restarts. |
| **ResourceManager** | YARN | `org.apache.hadoop.yarn.server.resourcemanager.ResourceManager` | Master resource scheduler and arbiter. Manages cluster CPU and memory resources, arbitrates allocations across applications, and tracks NodeManagers. |
| **NodeManager** | YARN | `org.apache.hadoop.yarn.server.nodemanager.NodeManager` | Per-node compute agent. Launches and monitors compute containers, enforces memory limits, and reports node health to the ResourceManager. |
| **JobHistoryServer** | MapReduce | `org.apache.hadoop.mapreduce.v2.hs.JobHistoryServer` | Archives completed MapReduce application logs, counters, and execution histories for post-mortem analysis and debugging. |

---

## 💾 Storage & Volume Persistence Layout

Hadoop data persists across container restarts using four dedicated Docker volumes:

```text
Host Docker Volume               Container Mount Path                                Description
├── hadoop_namenode_data   --->  /usr/local/hadoop/yarn_data/hdfs/namenode           NameNode fsimage metadata & edit logs
├── hadoop_datanode_data   --->  /usr/local/hadoop/yarn_data/hdfs/datanode           DataNode raw HDFS block files
├── hadoop_tmp_data        --->  /app/hadoop/tmp                                     Hadoop intermediate temp storage
└── hadoop_logs_data       --->  /usr/local/hadoop/logs                              Daemon runtime logs & job histories
```

> [!IMPORTANT]
> Because NameNode metadata and DataNode blocks are stored in separate persistent volumes, formatting the NameNode without clearing the DataNode volume will cause a `clusterID` mismatch error. Always use `make clean` or `docker compose down -v` to perform a full reset.

---

## 🚀 Container Startup & Initialization Flow

When the container boots, `scripts/docker/entrypoint.sh` executes the bootstrap sequence:

```mermaid
sequenceDiagram
    autonumber
    participant Docker as Docker Runtime
    participant Entrypoint as entrypoint.sh (root)
    participant SSH as OpenSSH Service
    participant HDUSER as hduser
    participant HDFS as HDFS Daemons
    participant YARN as YARN Daemons
    participant JHS as JobHistoryServer

    Docker->>Entrypoint: Container Starts (ENTRYPOINT)
    Entrypoint->>SSH: service ssh start
    Entrypoint->>HDUSER: Check / Generate SSH Keys (~/.ssh/id_rsa)
    
    alt NameNode directory empty
        Entrypoint->>HDUSER: hdfs namenode -format -force
    else NameNode already initialized
        Entrypoint->>HDUSER: Skip formatting
    end

    Entrypoint->>HDUSER: start-dfs.sh
    HDUSER->>HDFS: Launch NameNode, DataNode, SecondaryNameNode
    
    Entrypoint->>HDUSER: start-yarn.sh
    HDUSER->>YARN: Launch ResourceManager & NodeManager

    Entrypoint->>HDUSER: mapred --daemon start historyserver
    HDUSER->>JHS: Launch JobHistoryServer

    Entrypoint->>HDUSER: hdfs dfsadmin -safemode wait
    Entrypoint->>HDUSER: Initialize /tmp and /user/hduser directories
    
    Entrypoint->>Docker: Stream logs via tail -F
```

---

## 🌊 HDFS Data Pipelines

### HDFS File Write Lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Client as Client / Application
    participant NN as NameNode (:9000)
    participant DN as DataNode (:9866)
    participant Disk as Persistent Volume

    Client->>NN: 1. Create File Request (/data/file.txt)
    NN-->>Client: 2. Grant Write Lease & Return Target DataNode
    Client->>DN: 3. Stream Data Block Packets (64KB chunks)
    DN->>Disk: 4. Write Block to Disk & Update Checksum
    DN-->>Client: 5. Acknowledge Block Storage Complete
    Client->>NN: 6. Complete File Request
    NN->>NN: 7. Commit Metadata to Edit Log
```

### HDFS File Read Lifecycle

```mermaid
sequenceDiagram
    autonumber
    participant Client as Client / Application
    participant NN as NameNode (:9000)
    participant DN as DataNode (:9866)

    Client->>NN: 1. Get Block Locations for File (/data/file.txt)
    NN-->>Client: 2. Return Block IDs & DataNode Hosting Blocks
    Client->>DN: 3. Read Block Stream directly from DataNode
    DN-->>Client: 4. Stream Raw Block Data with Checksum Verification
    Client->>Client: 5. Reassemble Stream for Application
```

---

## ⚡ YARN MapReduce Job Execution Flow

When a user submits a MapReduce job (e.g. `yarn jar hadoop-mapreduce-examples.jar pi 2 5`):

```mermaid
sequenceDiagram
    autonumber
    participant Client as YARN Client (yarn jar)
    participant RM as ResourceManager (:8088)
    participant NM as NodeManager (:8042)
    participant AM as MR ApplicationMaster
    participant Container as Map/Reduce Task Containers
    participant HDFS as HDFS Storage (:9000)
    participant JHS as JobHistoryServer (:19888)

    Client->>RM: Submit Application Request
    RM->>NM: Allocate Container for ApplicationMaster (AM)
    NM->>AM: Launch ApplicationMaster Container
    AM->>HDFS: Read Input File Splits
    AM->>RM: Request Containers for Map and Reduce Tasks
    RM-->>AM: Grant Container Leases
    AM->>NM: Launch Map / Reduce Task Containers
    Container->>HDFS: Read Input Splits & Write Intermediate Data (Shuffle)
    Container->>HDFS: Write Final Output to HDFS
    Container-->>AM: Report Task Completion
    AM-->>RM: Notify Job Success & Release Containers
    AM->>JHS: Archive Job Logs & Counters
```

---

## 🌐 Network & Port Topology

The container maps internal daemons to host network interfaces:

```text
+-------------------------------------------------------------------------------+
| HOST MACHINE                                                                  |
|                                                                               |
|   :9870  ------------------->  NameNode Web UI                                |
|   :9864  ------------------->  DataNode Web UI                                |
|   :8088  ------------------->  YARN ResourceManager Web UI                    |
|   :8042  ------------------->  YARN NodeManager Web UI                        |
|   :19888 ------------------->  MapReduce JobHistory Web UI                    |
|   :9000  ------------------->  HDFS RPC Port (Client IPC)                     |
|   :22222 ------------------->  Container SSH Daemon (Port 22)                 |
|                                                                               |
+-------------------------------------------------------------------------------+
```

---

## 🔒 Security & Process Execution Model

1. **Non-Root Execution**:
   - Daemons run under the non-privileged `hduser` account (UID: 1000).
   - Sudo privileges (`NOPASSWD:ALL`) are granted to `hduser` for administrative operations inside the container.
2. **Passwordless SSH**:
   - Hadoop start scripts (`start-dfs.sh`, `start-yarn.sh`) require SSH loopback communication.
   - Dedicated RSA keypairs (`~/.ssh/id_rsa` and `~/.ssh/authorized_keys`) are generated with `0600` permissions.
3. **Relaxed Permission Checking**:
   - `dfs.permissions.enabled` is disabled in `hdfs-site.xml` to allow seamless local development and multi-tool experimentation.
4. **Environment & PATH Propagation**:
   - Environment variables (`JAVA_HOME`, `HADOOP_HOME`, `HADOOP_CONF_DIR`, `PATH`) are centralized in `/etc/profile.d/hadoop.sh` and backed into `.bashrc` and `.profile` for both `hduser` and `root`.
   - Automation scripts (`entrypoint.sh`, `healthcheck.sh`, `test-cluster.sh`) utilize subshell environment wrappers (`run_hduser`) ensuring uninterrupted execution across interactive and non-interactive sessions.

