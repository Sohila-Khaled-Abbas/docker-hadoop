# Configuration & Performance Tuning Guide

This document details the configuration files within the `config/` directory and offers optimization strategies for running Apache Hadoop workloads.

---

## 📑 Table of Contents

- [Configuration Files Overview](#configuration-files-overview)
- [`core-site.xml` Parameters](#core-sitexml-parameters)
- [`hdfs-site.xml` Parameters](#hdfs-sitexml-parameters)
- [`yarn-site.xml` Parameters](#yarn-sitexml-parameters)
- [`mapred-site.xml` Parameters](#mapred-sitexml-parameters)
- [`hadoop-env.sh` JVM Sizing](#hadoop-envsh-jvm-sizing)
- [Performance Tuning Recommendations](#performance-tuning-recommendations)

---

## 📁 Configuration Files Overview

| File | Primary Scope | Key Managed Settings |
| :--- | :--- | :--- |
| `config/core-site.xml` | Global Hadoop Core | Default filesystem URI (`fs.defaultFS`), temporary storage path (`hadoop.tmp.dir`), I/O buffer sizing. |
| `config/hdfs-site.xml` | HDFS Storage Subsystem | Block replication, NameNode/DataNode data paths, Web UI ports, permissions. |
| `config/yarn-site.xml` | YARN Resource Management | Shuffle service, ResourceManager host/ports, NodeManager memory & vcore limits. |
| `config/mapred-site.xml` | MapReduce Framework | Runtime framework (`yarn`), JobHistory server addresses, map/reduce container memory. |
| `config/hadoop-env.sh` | Java & Process Environment | `JAVA_HOME`, JVM Heap options, daemon user bindings (`HDFS_NAMENODE_USER`, etc.). |

---

## ⚙️ `core-site.xml` Parameters

```xml
<configuration>
    <!-- Base directory for Hadoop temporary storage -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/app/hadoop/tmp</value>
    </property>

    <!-- Default filesystem URI -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>

    <!-- Stream buffer size (default 4KB, 64KB recommended for high throughput) -->
    <property>
        <name>io.file.buffer.size</name>
        <value>65536</value>
    </property>
</configuration>
```

---

## ⚙️ `hdfs-site.xml` Parameters

```xml
<configuration>
    <!-- Replication factor (1 for single-node development, 3 for multi-node production) -->
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <!-- HDFS Block size (default 128MB) -->
    <property>
        <name>dfs.blocksize</name>
        <value>134217728</value>
    </property>

    <!-- NameNode metadata storage directory -->
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/yarn_data/hdfs/namenode</value>
    </property>

    <!-- DataNode block storage directory -->
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/yarn_data/hdfs/datanode</value>
    </property>
</configuration>
```

---

## ⚙️ `yarn-site.xml` Parameters

```xml
<configuration>
    <!-- Total physical memory (MB) available for YARN containers on this node -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
    </property>

    <!-- Minimum and maximum container allocation size -->
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>512</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>4096</value>
    </property>

    <!-- Number of vcores allocated to NodeManager -->
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>
</configuration>
```

---

## ⚙️ `mapred-site.xml` Parameters

```xml
<configuration>
    <property>
        <name>mapred.framework.name</name>
        <value>yarn</value>
    </property>

    <!-- Container memory for Map tasks -->
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>1024</value>
    </property>

    <!-- Container memory for Reduce tasks -->
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>2048</value>
    </property>
</configuration>
```

---

## ☕ `hadoop-env.sh` JVM Sizing

You can configure daemon heap sizes directly in `config/hadoop-env.sh`:

```bash
# NameNode Heap Size
export HDFS_NAMENODE_OPTS="-Xms512m -Xmx1024m"

# DataNode Heap Size
export HDFS_DATANODE_OPTS="-Xms256m -Xmx512m"

# ResourceManager Heap Size
export YARN_RESOURCEMANAGER_OPTS="-Xms512m -Xmx1024m"

# NodeManager Heap Size
export YARN_NODEMANAGER_OPTS="-Xms256m -Xmx512m"
```

---

## 🚀 Performance Tuning Recommendations

1. **Avoid Small Files**: Thousands of tiny files consume NameNode memory disproportionately (each metadata object occupies ~150 bytes in NameNode RAM). Use Hadoop Archives (HAR) or SequenceFiles for small files.
2. **Use Combiners**: In MapReduce jobs, enable local combiners (`job.setCombinerClass(...)`) to minimize intermediate network shuffle volume.
3. **Tune Compression**: Use Snappy or Gzip compression for intermediate Map outputs to reduce disk I/O and network transfer times.
