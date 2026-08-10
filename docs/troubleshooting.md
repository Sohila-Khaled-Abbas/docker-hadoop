# Hadoop Docker Troubleshooting Runbook

This guide contains diagnostic steps and solutions for common operational issues encountered when running Apache Hadoop in Docker.

---

## 📑 Table of Contents

- [Diagnostic Quick-Check](#diagnostic-quick-check)
- [Issue 1: NameNode Stuck in SafeMode](#issue-1-namenode-stuck-in-safemode)
- [Issue 2: DataNode Not Starting / ClusterID Mismatch](#issue-2-datanode-not-starting--clusterid-mismatch)
- [Issue 3: YARN Containers Failing / Out of Memory](#issue-3-yarn-containers-failing--out-of-memory)
- [Issue 4: Host Port Conflicts](#issue-4-host-port-conflicts)
- [Issue 5: Missing Java Daemons on Startup](#issue-5-missing-java-daemons-on-startup)
- [Issue 6: Container Exit Codes (137, 143)](#issue-6-container-exit-codes-137-143)

---

## 🩺 Diagnostic Quick-Check

When experiencing issues, execute this diagnostic sequence:

```bash
# 1. Check container health status
docker compose ps

# 2. Check running Hadoop Java processes
docker compose exec hadoop jps

# 3. View latest container logs
docker compose logs hadoop --tail 100

# 4. Check HDFS admin health report
docker compose exec hadoop hdfs dfsadmin -report
```

---

## ⚠️ Issue 1: NameNode Stuck in SafeMode

### Symptoms
- Commands fail with `Cannot create file /... Name node is in safe mode.`
- Web UI shows `Safe mode is ON`.

### Root Cause
On startup, the NameNode enters SafeMode to wait for DataNodes to report their block status. If available resources or block thresholds are delayed, it remains locked.

### Solution
Force the NameNode to leave SafeMode:
```bash
docker compose exec hadoop hdfs dfsadmin -safemode leave
```

---

## ⚠️ Issue 2: DataNode Not Starting / ClusterID Mismatch

### Symptoms
- `jps` does not show `DataNode`.
- NameNode Web UI at `:9870` reports `0 Live DataNodes`.
- DataNode log contains: `java.io.IOException: Incompatible clusterIDs in /usr/local/hadoop/yarn_data/hdfs/datanode`.

### Root Cause
The NameNode was re-formatted while the DataNode volume still retained the old cluster ID from a previous format operation.

### Solution
Perform a full clean teardown to remove conflicting volume state, then re-launch:
```bash
make clean
make up
```

---

## ⚠️ Issue 3: YARN Containers Failing / Out of Memory

### Symptoms
- MapReduce jobs hang or fail with `Container killed by the ApplicationMaster for exceeding memory limits`.
- NodeManager logs show memory violations.

### Root Cause
Docker container memory limit or YARN virtual memory checks killed the task.

### Solution
1. In `config/yarn-site.xml`, ensure virtual/physical memory checks are disabled for local dev:
   ```xml
   <property>
       <name>yarn.nodemanager.vmem-check-enabled</name>
       <value>false</value>
   </property>
   ```
2. Allocate sufficient memory to Docker in Docker Desktop Settings (minimum 4GB, recommended 8GB).

---

## ⚠️ Issue 4: Host Port Conflicts

### Symptoms
- `docker compose up` fails with `Error response from daemon: driver failed programming external connectivity ... bind: address already in use`.

### Root Cause
Another service on your host (e.g. another local Hadoop instance, Spark, or web server) is occupying ports like `9870`, `8088`, or `9000`.

### Solution
Edit `.env` or set environment variables before starting to remap ports:
```bash
HADOOP_NAMENODE_PORT=19870
HADOOP_RESOURCEMANAGER_PORT=18088
HADOOP_HDFS_RPC_PORT=19000
```
Then run `docker compose up -d`.

---

## ⚠️ Issue 5: Missing Java Daemons on Startup

### Symptoms
- Running `docker compose exec hadoop jps` shows only 2-3 daemons instead of the expected 6 (`NameNode`, `DataNode`, `SecondaryNameNode`, `ResourceManager`, `NodeManager`, `JobHistoryServer`).

### Solution
Inspect specific daemon logs in `/usr/local/hadoop/logs/`:
```bash
# Check NameNode logs
docker compose exec hadoop tail -n 50 /usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.log

# Check ResourceManager logs
docker compose exec hadoop tail -n 50 /usr/local/hadoop/logs/yarn-hduser-resourcemanager-localhost.log

# Check DataNode logs
docker compose exec hadoop tail -n 50 /usr/local/hadoop/logs/hadoop-hduser-datanode-localhost.log
```

---

## ⚠️ Issue 6: Container Exit Codes (137, 143)

| Exit Code | Reason | Resolution |
| :--- | :--- | :--- |
| **137** | **OOMKilled (Out of Memory)** | The container exceeded host RAM limits. Increase Docker memory in Docker Desktop Settings to 6GB+. |
| **143** | **SIGTERM (Graceful Stop)** | Container was stopped intentionally via `docker compose down` or host shutdown. |
