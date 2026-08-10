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

The container orchestrates the complete Apache Hadoop 3.1.2 daemon stack inside an isolated Ubuntu 20.04 environment. It exposes all native Web UIs, RPC ports, and SSH endpoints to the host while persisting cluster state through named Docker volumes.

```mermaid
graph TB
    subgraph Host["Host Machine"]
        subgraph Browsers["Web Browsers & External Clients"]
            ClientUI["Developer Browser / External Client"]
        end
        subgraph Volumes["Docker Named Volumes"]
            V_NN["hadoop_namenode_data<br/>(FSImage & Edits)"]
            V_DN["hadoop_datanode_data<br/>(HDFS Blocks)"]
            V_TMP["hadoop_tmp_data<br/>(/app/hadoop/tmp)"]
            V_LOG["hadoop_logs_data<br/>(/usr/local/hadoop/logs)"]
        end
    end

    subgraph Container["Hadoop Docker Container (localhost / hadoop-master)"]
        subgraph StorageLayer["HDFS Storage Layer"]
            NN["NameNode<br/>Port: 9870 (Web), 9000 (RPC)"]
            SNN["SecondaryNameNode<br/>Port: 9868 (Web)"]
            DN["DataNode<br/>Port: 9864 (Web), 9866 (Data)"]
        end

        subgraph ComputeLayer["YARN Compute Layer"]
            RM["ResourceManager<br/>Port: 8088 (Web), 8032 (IPC)"]
            NM["NodeManager<br/>Port: 8042 (Web), 8040 (IPC)"]
            JHS["JobHistoryServer<br/>Port: 19888 (Web), 10020 (IPC)"]
        end

        subgraph OS["Container OS / Runtime"]
            SSHD["OpenSSH Daemon<br/>Port: 22 (Mapped to 2222)"]
            JVM["OpenJDK 8 Runtime"]
            HDUSER["hduser (UID: 1000, GID: 1000)"]
        end
    end

    ClientUI -->|HTTP :9870| NN
    ClientUI -->|HTTP :9864| DN
    ClientUI -->|HTTP :8088| RM
    ClientUI -->|HTTP :8042| NM
    ClientUI -->|HTTP :19888| JHS
    ClientUI -->|RPC :9000| NN
    ClientUI -->|SSH :2222| SSHD

    NN <-->|Heartbeats & Block Reports| DN
    NN <-->|Checkpoint Merging| SNN
    RM <-->|Node Heartbeats & Allocations| NM
    NM -->|Completed Job Logs| JHS

    NN -.->|Persist Metadata| V_NN
    DN -.->|Persist Data Blocks| V_DN
    StorageLayer -.->|Temp Files| V_TMP
    ComputeLayer -.->|Runtime Logs| V_LOG
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

When the container boots, `scripts/entrypoint.sh` executes the bootstrap sequence:

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
|   :2222  ------------------->  Container SSH Daemon (Port 22)                 |
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
