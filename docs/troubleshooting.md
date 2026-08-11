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
- [Issue 7: Docker Build Hang / High Inode Journal Overhead on WSL2](#issue-7-docker-build-hang--high-inode-journal-overhead-on-wsl2)
- [Issue 8: Non-Interactive Shell / Command Not Found (`hdfs: command not found`)](#issue-8-non-interactive-shell--command-not-found-hdfs-command-not-found)
- [Issue 9: Browser `ERR_EMPTY_RESPONSE` ("localhost didn't send any data") on Web UIs](#issue-9-browser-err_empty_response-localhost-didnt-send-any-data-on-web-uis)
- [Issue 10: Docker Engine Pipe 500 Internal Server Error (`dockerDesktopLinuxEngine`)](#issue-10-docker-engine-pipe-500-internal-server-error-dockerdesktoplinuxengine)

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

---

## ⚠️ Issue 7: Docker Build Hang / High Inode Journal Overhead on WSL2

### Symptoms
- `docker compose build` hangs or takes 15+ minutes on `chown -R` / `chmod -R` or `exporting layers`.

### Root Cause
The official Hadoop tarball contains ~60,000 small Javadoc/API HTML files under `share/doc`. Performing recursive metadata operations on ext4 filesystems in virtualized WSL2 environments triggers massive journaling overhead.

### Solution
Prune the documentation directory during image build (already implemented in the Dockerfile):
```dockerfile
RUN rm -rf ${HADOOP_HOME}/share/doc \
    && chown -R hduser:hadoop ${HADOOP_HOME} /app/hadoop
```
If BuildKit layer export hangs, build with classic builder:
```powershell
$env:DOCKER_BUILDKIT=0; docker compose build
```

---

## ⚠️ Issue 8: Non-Interactive Shell / Command Not Found (`hdfs: command not found`)

### Symptoms
- Executing commands via `su - hduser -c "hdfs ..."` or CI runners fails with `hdfs: command not found`.

### Root Cause
Non-interactive subshells in Debian/Ubuntu terminate `.bashrc` early before user exports are loaded (`case $- in *i*) ;; *) return;; esac`).

### Solution
Environment variables are now centralized in `/etc/profile.d/hadoop.sh` and explicitly wrapped in scripts (`entrypoint.sh`, `healthcheck.sh`, `test-cluster.sh`):
```bash
export JAVA_HOME=/usr/local/java
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

---

## ⚠️ Issue 9: Browser `ERR_EMPTY_RESPONSE` ("localhost didn't send any data") on Web UIs

### Symptoms
- Opening `http://localhost:9870` or `http://localhost:8088` in Chrome/Edge displays:
  `This page isn’t working`
  `localhost didn’t send any data.`
  `ERR_EMPTY_RESPONSE`

### Root Cause
1. **Browser HTTPS Auto-Upgrade**: Modern browsers (Chrome, Edge, Brave) frequently auto-upgrade typed `localhost:port` addresses to `https://...` (via HSTS policies or browser omnibox). Because Hadoop Web UIs run on plain **HTTP**, receiving an SSL/TLS handshake on an HTTP port causes Hadoop to drop the socket connection immediately.
2. **HDFS Startup / SafeMode Window**: On initial container startup, the NameNode waits ~30 seconds in SafeMode while DataNodes register their block reports.

### Solution
1. Open an **Incognito / Private Window** (which bypasses cached HTTPS redirects) and explicitly navigate to:
   - **HDFS NameNode**: `http://127.0.0.1:9870` *(or `http://localhost:9870`)*
   - **YARN ResourceManager**: `http://127.0.0.1:8088` *(or `http://localhost:8088`)*
   - **MapReduce JobHistory**: `http://127.0.0.1:19888` *(or `http://localhost:19888`)*
2. If Chrome continues redirecting to HTTPS:
   - Navigate to `chrome://net-internals/#hsts` in Chrome.
   - Under **Delete domain security policies**, type `localhost` and click **Delete**.
   - Repeat for `127.0.0.1`.

---

## ⚠️ Issue 10: Docker Engine Pipe 500 Internal Server Error (`dockerDesktopLinuxEngine`)

### Symptoms
- Running Docker commands fails with:
  `request returned 500 Internal Server Error for API route and version http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/...`

### Root Cause
The Docker Desktop Linux daemon / WSL2 backend IPC named pipe encountered a deadlock or became unresponsive in Windows.

### Solution
Restart the WSL2 daemon and Docker Desktop:
```powershell
wsl --shutdown
```
Then launch Docker Desktop from the Start Menu and wait for the engine status to show green.

