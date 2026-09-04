# 🗄️ HDFS Command-Line Interface (CLI) Guide & Automation

This tutorial provides a complete, runnable guide to mastering the Hadoop Distributed File System (HDFS) command line interface (`hdfs dfs`).

---

## ⚡ Quick Start: Running the Interactive Demo

You can execute the end-to-end HDFS operations demonstration script directly inside the container:

```bash
# Execute directly inside the Hadoop container
docker compose exec hadoop bash -c "bash /usr/local/hadoop/demo-hdfs-operations.sh"
# or if mounted/copied locally:
docker compose exec hadoop bash < examples/hdfs-cli/demo-hdfs-operations.sh
```

---

## 📖 Essential HDFS Command Reference

The `hdfs dfs` command is the standard client interface for interacting with HDFS. It mirrors standard POSIX / UNIX shell utilities.

### 1. Directory Management

```bash
# Create directory (with parent folders if missing)
hdfs dfs -mkdir -p /user/hadoop/analytics

# List files and directories
hdfs dfs -ls /user/hadoop

# Recursive directory listing
hdfs dfs -ls -R /user/hadoop
```

### 2. Ingestion & Data Movement

```bash
# Upload local file to HDFS
hdfs dfs -put /path/to/local/data.csv /user/hadoop/data.csv

# Upload with overwrite flag
hdfs dfs -put -f /path/to/local/data.csv /user/hadoop/data.csv

# Download file from HDFS to local machine
hdfs dfs -get /user/hadoop/data.csv /tmp/downloaded_data.csv

# Copy file within HDFS
hdfs dfs -cp /user/hadoop/data.csv /user/hadoop/backup.csv

# Move / Rename file within HDFS
hdfs dfs -mv /user/hadoop/backup.csv /user/hadoop/archive.csv
```

### 3. File Viewing & Inspection

```bash
# Display entire file contents to stdout
hdfs dfs -cat /user/hadoop/data.csv

# View first 1KB of file
hdfs dfs -head /user/hadoop/data.csv

# View last 1KB of file
hdfs dfs -tail /user/hadoop/data.csv

# View file metadata (replication, block size, modification date)
hdfs dfs -stat "Replication: %r | BlockSize: %o bytes | Date: %y" /user/hadoop/data.csv
```

### 4. Storage & Health Inspection

```bash
# Check disk space used by a directory
hdfs dfs -du -h /user/hadoop

# Count directories, files, and total bytes
hdfs dfs -count -q -h /user/hadoop

# Verify MD5/SHA checksum
hdfs dfs -checksum /user/hadoop/data.csv

# Change replication factor of an HDFS file
hdfs dfs -setrep -w 1 /user/hadoop/data.csv
```

### 5. Deletion & Cleanup

```bash
# Delete a single file
hdfs dfs -rm /user/hadoop/data.csv

# Delete directory recursively (moves to .Trash if enabled)
hdfs dfs -rm -r /user/hadoop/analytics

# Permanently bypass Trash and delete immediately
hdfs dfs -rm -r -skipTrash /user/hadoop/analytics
```

---

## 🛡️ Administrative Inspection (`hdfs dfsadmin`)

```bash
# Display cluster storage capacity and active DataNode health report
hdfs dfsadmin -report

# Inspect SafeMode status
hdfs dfsadmin -safemode get

# Force NameNode to exit SafeMode (e.g. after unexpected shutdown)
hdfs dfsadmin -safemode leave
```
