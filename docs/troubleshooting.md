# 🔍 Apache Hadoop Docker Troubleshooting Runbook

This runbook provides diagnostic decision trees, root cause analyses, and verified solutions for common operational issues encountered when running Apache Hadoop on Docker across Linux, macOS, and Windows.

---

## 📑 Table of Contents

- [Diagnostic Decision Tree](#-diagnostic-decision-tree)
- [Diagnostic Quick-Check Command Sequence](#-diagnostic-quick-check-command-sequence)
- [Issue 1: NameNode Stuck in SafeMode](#-issue-1-namenode-stuck-in-safemode)
- [Issue 2: DataNode Not Starting / ClusterID Mismatch](#-issue-2-datanode-not-starting--clusterid-mismatch)
- [Issue 3: YARN Containers Failing / Out of Memory](#-issue-3-yarn-containers-failing--out-of-memory)
- [Issue 4: Host Port Conflicts](#-issue-4-host-port-conflicts)
- [Issue 5: Windows `WSAEACCES` / Hyper-V Port Exclusion Range (Port 2222)](#-issue-5-windows-wsaeacces--hyper-v-port-exclusion-range-port-2222)
- [Issue 6: Missing Java Daemons on Startup](#-issue-6-missing-java-daemons-on-startup)
- [Issue 7: Container Exit Codes (137, 143)](#-issue-7-container-exit-codes-137-143)
- [Issue 8: Docker Build Hang / WSL2 Inode Journaling Overhead](#-issue-8-docker-build-hang--wsl2-inode-journaling-overhead)
- [Issue 9: Non-Interactive Shell / Command Not Found](#-issue-9-non-interactive-shell--command-not-found)
- [Issue 10: Browser `ERR_EMPTY_RESPONSE` ("localhost didn't send any data")](#-issue-10-browser-err_empty_response-localhost-didnt-send-any-data)
- [Issue 11: Docker Engine Named Pipe 500 Error (`dockerDesktopLinuxEngine`)](#-issue-11-docker-engine-named-pipe-500-error-dockerdesktoplinuxengine)
- [Issue 12: Hyper-V VM Fails to Start (`0x800705AA` / `0x8007000E` - Insufficient System Resources)](#-issue-12-hyper-v-vm-fails-to-start-0x800705aa--0x8007000e---insufficient-system-resources)
- [Issue 13: Mouse Pointer Offset & Clicks Not Registering in Hyper-V Ubuntu Installer](#-issue-13-mouse-pointer-offset--clicks-not-registering-in-hyper-v-ubuntu-installer)
- [Issue 14: Hyper-V 1-vCPU Bottleneck & Input Stuttering](#-issue-14-hyper-v-1-vcpu-bottleneck--input-stuttering)
- [Issue 15: Hyper-V Linux VM Has No Internet on Wi-Fi Host (External Switch Trap)](#-issue-15-hyper-v-linux-vm-has-no-internet-on-wi-fi-host-external-switch-trap)

---

## 🧭 Diagnostic Decision Tree

```mermaid
flowchart TD
    Start["Issue Detected"] --> CheckPS["Run: <code>docker compose ps</code>"]
    CheckPS -->|Container Exited / Restarting| Logs["Run: <code>docker compose logs hadoop --tail 50</code>"]
    CheckPS -->|Container Running (Unhealthy)| CheckJPS["Run: <code>docker compose exec hadoop jps</code>"]

    Logs -->|Exit Code 137| FixOOM["Increase Docker RAM to 6GB+<br/>(Issue 7)"]
    Logs -->|bind: address already in use / forbidden| FixPort["Remap Host Ports in .env<br/>(Issues 4 & 5)"]

    CheckJPS -->|Missing NameNode/DataNode| CheckClusterID["Check for ClusterID divergence<br/>(Issue 2)"]
    CheckJPS -->|All 6 Daemons Running| CheckSafeMode["Check SafeMode status<br/><code>hdfs dfsadmin -safemode get</code> (Issue 1)"]

    classDef normal fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef fix fill:#0284c7,stroke:#0369a1,stroke-width:2px,color:#ffffff;
    class Start,CheckPS,CheckJPS normal;
    class FixOOM,FixPort,CheckClusterID,CheckSafeMode fix;
```

---

## 🩺 Diagnostic Quick-Check Command Sequence

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
- Commands fail with: `Cannot create file /... Name node is in safe mode.`
- Web UI at [http://localhost:9870](http://localhost:9870) displays `Safe mode is ON`.

### Root Cause
During startup, NameNode stays in SafeMode until DataNodes report their block state. If the block threshold takes time, SafeMode remains locked.

### Solution
```bash
docker compose exec hadoop hdfs dfsadmin -safemode leave
```

---

## ⚠️ Issue 2: DataNode Not Starting / ClusterID Mismatch

### Symptoms
- `jps` does not show `DataNode`.
- NameNode reports `0 Live DataNodes`.
- DataNode log contains: `java.io.IOException: Incompatible clusterIDs in /usr/local/hadoop/yarn_data/hdfs/datanode`.

### Root Cause
NameNode was formatted while old DataNode volume files still retained a previous cluster ID.

### Solution
Perform a full clean teardown to remove conflicting volume state:
```bash
make clean
make up
```

---

## ⚠️ Issue 3: YARN Containers Failing / Out of Memory

### Symptoms
- MapReduce jobs fail with `Container killed by the ApplicationMaster for exceeding memory limits`.

### Solution
1. In `config/yarn-site.xml`, ensure virtual memory checks are disabled:
   ```xml
   <property>
       <name>yarn.nodemanager.vmem-check-enabled</name>
       <value>false</value>
   </property>
   ```
2. Allocate at least 6GB RAM to Docker Desktop.

---

## ⚠️ Issue 4: Host Port Conflicts

### Symptoms
- `docker compose up` fails with `driver failed programming external connectivity ... bind: address already in use`.

### Solution
Create or edit `.env` and assign alternate host ports:
```bash
HADOOP_NAMENODE_PORT=19870
HADOOP_RESOURCEMANAGER_PORT=18088
HADOOP_HDFS_RPC_PORT=19000
```

---

## ⚠️ Issue 5: Windows `WSAEACCES` / Hyper-V Port Exclusion Range (Port 2222)

### Symptoms
- Starting container fails on Windows with:
  `listen tcp 0.0.0.0:2222: bind: An attempt was made to access a socket in a way forbidden by its access permissions.`

### Root Cause
Windows Hyper-V and WSL2 NAT service (`winnat`) reserve dynamic port exclusion ranges (e.g., `2180 - 2279`). Port `2222` falls inside this reserved block.

### Solution
Change `HADOOP_SSH_PORT` in `.env` or `docker-compose.yml` to an unreserved port such as **`22222`**:
```env
HADOOP_SSH_PORT=22222
```

---

## ⚠️ Issue 6: Missing Java Daemons on Startup

### Symptoms
- `jps` shows fewer than the 6 expected daemons (`NameNode`, `DataNode`, `SecondaryNameNode`, `ResourceManager`, `NodeManager`, `JobHistoryServer`).

### Solution
Inspect specific daemon logs in `/usr/local/hadoop/logs/`:
```bash
docker compose exec hadoop tail -n 50 /usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.log
docker compose exec hadoop tail -n 50 /usr/local/hadoop/logs/yarn-hduser-resourcemanager-localhost.log
```

---

## ⚠️ Issue 7: Container Exit Codes (137, 143)

| Exit Code | Cause | Resolution |
| :--- | :--- | :--- |
| **`137`** | **OOMKilled** (Host killed container due to memory starvation) | Increase Docker Desktop RAM allocation to 6GB+. |
| **`143`** | **SIGTERM** (Graceful termination) | Expected when stopping cluster via `docker compose down`. |

---

## ⚠️ Issue 8: Docker Build Hang / WSL2 Inode Journaling Overhead

### Root Cause
Hadoop binary distributions contain ~60,000 small Javadoc files. Recursively changing permissions triggers high ext4 journaling overhead on WSL2.

### Solution
Pruning documentation during Docker build (included in our Dockerfile) resolves this:
```dockerfile
RUN rm -rf ${HADOOP_HOME}/share/doc \
    && chown -R hduser:hadoop ${HADOOP_HOME} /app/hadoop
```

---

## ⚠️ Issue 9: Non-Interactive Shell / Command Not Found

### Root Cause
Non-interactive subshells (`su - hduser -c "..."`) exit early in default Ubuntu `.bashrc`.

### Solution
Environment variables are centralized in `/etc/profile.d/hadoop.sh` and explicitly loaded across all runner scripts.

---

## ⚠️ Issue 10: Browser `ERR_EMPTY_RESPONSE` ("localhost didn't send any data")

### Root Cause
Browsers auto-upgrade `localhost:port` to HTTPS. Hadoop Web UIs speak plain **HTTP**.

### Solution
Open an **Incognito Window** and navigate explicitly to:
- `http://127.0.0.1:9870`
- `http://127.0.0.1:8088`

---

## ⚠️ Issue 11: Docker Engine Named Pipe 500 Error (`dockerDesktopLinuxEngine`)

### Solution
Restart the WSL2 backend:
```powershell
wsl --shutdown
```
Then relaunch Docker Desktop.

---

## ⚠️ Issue 12: Hyper-V VM Fails to Start (`0x800705AA` / `0x8007000E` - Insufficient System Resources)

### Symptoms
`Unable to allocate 4096 MB of RAM: Insufficient system resources exist to complete the requested service. (0x800705AA)` or `Not enough memory resources are available to complete this operation. (0x8007000E)`.

### Root Cause
Hyper-V was configured with a static contiguous block of 4096 MB RAM, but the host operating system had less than 4 GB of unreserved memory available due to background processes (e.g., WSL holding memory).

### Solution
1. **Enable Dynamic Memory**:
   - In Hyper-V Manager, right-click the VM $\rightarrow$ **Settings** $\rightarrow$ **Memory**.
   - Change **Startup RAM** to `2048 MB`.
   - Check **"Enable Dynamic Memory"** (Minimum: `1024 MB`, Maximum: `4096 MB`).
2. **Reclaim Host Memory**:
   Run in PowerShell:
   ```powershell
   wsl --shutdown
   ```

---

## ⚠️ Issue 13: Mouse Pointer Offset & Clicks Not Registering in Hyper-V Ubuntu Installer

### Symptoms
When clicking buttons (e.g., "Install Ubuntu", "Next", "Continue") inside `vmconnect.exe`, the clicks do not trigger the button, or the mouse cursor seems offset.

### Root Cause
Before Ubuntu Guest Integration Services (`linux-vm-tools`) are installed, Hyper-V operates in **Basic Session** mode using a synthetic PS/2 mouse. High-DPI Windows display scaling creates a coordinate offset between the host cursor and the guest cursor.

### Solution
1. **Use Keyboard Navigation (Fastest & 100% Reliable)**:
   - Click inside the VM window to give it focus.
   - Press **`Tab`** (or `Shift + Tab`) to cycle through buttons. The active button will be outlined in orange/blue.
   - Press **`Spacebar`** to select checkboxes / radio buttons.
   - Press **`Enter`** to activate the button ("Next", "Install", "Continue").
2. **Switch to Full Screen Mode**:
   - In `vmconnect.exe`, click **View** $\rightarrow$ **Full Screen** (or press the Full Screen icon).
   - In Full Screen, the mouse coordinates synchronize 1:1 with the guest cursor.

---

## ⚠️ Issue 14: Hyper-V 1-vCPU Bottleneck & Input Stuttering

### Symptoms
Ubuntu Desktop runs extremely slowly, mouse movement stutters, and typing in terminal is delayed.

### Root Cause
Hyper-V defaults new virtual machines to only **1 virtual processor (1 vCPU)**. Running GNOME Mutter software rendering on a single core saturates 100% CPU.

### Solution
1. Turn off the VM.
2. Run our automated optimizer script:
   ```cmd
   Fix-Lag-And-Start-VM.bat
   ```
   *Or* in Hyper-V Manager: Right-click VM $\rightarrow$ **Settings** $\rightarrow$ **Processor** $\rightarrow$ increase from `1` to **`4` vCPUs**.

---

## ⚠️ Issue 15: Hyper-V Linux VM Has No Internet on Wi-Fi Host (External Switch Trap)

### Symptoms
Inside the Ubuntu VM, `curl` fails with `Could not resolve host` or `Network is unreachable`, `apt update` fails, and `ping 8.8.8.8` receives no response.

### Root Cause
An **External Virtual Switch** was created and bound to a Wi-Fi adapter (e.g. `Intel Wireless-AC`). Standard Wi-Fi (802.11) access points drop frames from any MAC address other than the authenticated host laptop, leaving the VM without a valid DHCP IP address or internet route.

### Solution
1. **Connect to Default Switch (NAT)**:
   - Double click `Fix-VM-Internet.bat` in the repository root.
   - *Or* in Hyper-V Manager: Right-click VM $\rightarrow$ **Settings** $\rightarrow$ **Network Adapter** $\rightarrow$ change Virtual switch to **"Default Switch"** $\rightarrow$ click **Apply**.
2. **Refresh DHCP inside Ubuntu**:
   In the Ubuntu terminal, run:
   ```bash
   sudo dhclient -r && sudo dhclient
   ping -c 2 8.8.8.8
   ```
