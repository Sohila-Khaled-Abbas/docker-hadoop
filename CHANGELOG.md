# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **5GB RAM & 11-Port High-Performance VM Profile (`scripts/virtualbox-setup.ps1`)**: Upgraded VirtualBox VM memory to 5120 MB (5GB) and added port forwardings for YARN NodeManager (`8042`), HDFS RPC (`9000`), Apache Spark UI (`4040`), Spark History Server (`18080`), HiveServer2 (`10000`), and Hive Web UI (`10002`).
- **Headless VM Mode & VS Code Remote SSH (`make vm-start-headless`)**: Added background headless launch switch to `virtualbox-setup.ps1` and `Makefile`, saving ~1GB RAM and CPU rendering overhead for terminal-centric Big Data development.
- **Linux Kernel & JVM Sizing Optimizations (`scripts/install-hadoop-ubuntu.sh`)**: Added automated OS kernel tuning (`vm.swappiness=1`, ulimits `65536`, THP disabling) and G1GC low-latency garbage collection flags (`-XX:+UseG1GC`) across all daemon JVM heaps.
- **Oracle VirtualBox Provisioner (`scripts/virtualbox-setup.ps1`)**: Automated provisioning script featuring 4 vCPUs, UEFI/EFI 64-bit firmware, native Full HD (`1920x1080`) GOP graphics resolution, Hyper-V paravirtualization clock sync, USB low-latency input controller, dynamic window auto-resize, and complete Big Data NAT forwarding.
- **Rootless User-Space Installer (`scripts/install-hadoop-user.sh`)**: Zero-sudo automated installer deploying Apache Hadoop 3.3.6 directly into `~/hadoop` and `~/hadoopdata` with passwordless SSH, memory heap tuning, and automated daemon startup.
- **Ubuntu & VirtualBox Deployment Guide (`docs/virtualbox-ubuntu-guide.md`)**: Comprehensive documentation covering hardware requirements, automated/manual VM creation, unscaled 1:1 display tuning, dynamic window resizing shortcuts, cluster verification, and troubleshooting runbooks.
- **Automated Ubuntu Bare-Metal/VM Installer (`scripts/install-hadoop-ubuntu.sh`)**: End-to-end automated script installing OpenJDK 11, passwordless SSH, Apache Hadoop 3.3.6, cluster XMLs, environment profiles, formatting NameNode, and launching all daemons including MapReduce JobHistory server.
- Comprehensive architecture documentation with Mermaid component and sequence diagrams in `docs/architecture.md`.
- In-depth MapReduce programming and tuning guide in `docs/mapreduce-guide.md`.
- Troubleshooting runbook and diagnostic matrix in `docs/troubleshooting.md`.
- Ecosystem integration guides for Apache Spark, PySpark, and Apache Hive in `docs/ecosystem-integration.md`.
- Configuration and performance tuning guide in `docs/configuration-tuning.md`.
- Python Hadoop Streaming MapReduce sample (`mapper.py`, `reducer.py`, `run.sh`) in `examples/mapreduce-python/`.
- Java MapReduce WordCount example with compilation script in `examples/mapreduce-java/`.
- PySpark HDFS integration script in `examples/spark-pyspark/`.
- Software engineering governance standards: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`.
- GitHub issue templates for bug reports and feature requests, plus structured PR template.
- Expanded Makefile targets for MapReduce testing, SafeMode management, and HDFS reporting.

### Changed
- **VirtualBox 4-vCPU & USB Input Latency Optimization**: Upgraded default VM processor allocation from 2 to 4 vCPUs and switched to `--keyboard usb --mouse usbtablet`, eliminating GNOME Mutter LLVMpipe software rendering overhead and input polling lag.
- **Resolved `VERR_UNRESOLVED_ERROR` (0x80004005)**: Configured `--large-pages off` on Windows hosts to avoid missing `SeLockMemoryPrivilege` (`MEM_LARGE_PAGES`) security policy failures during VM memory allocation.
- **VirtualBox Stability & Timer Synchronization**: Switched VM clock paravirtualization to `hyperv`, eliminating Windows WHPX/Hyper-V timer drift and watchdog soft lockup kernel panics during live ISO boots.
- **VirtualBox Display Optimization**: Configured EFI GOP resolution (`VBoxInternal2/EfiGraphicsResolution = 1920x1080`), VMSVGA graphics controller with 128 MB VRAM, 1.0 scale factor, and `AutoResizeGuest` to dynamically fill the window without pixel distortion or black borders.
- **Dockerfile Build Optimization**: Added automated pruning of `/usr/local/hadoop/share/doc` (~60,000 redundant documentation and Javadoc files) before recursive `chown`/`chmod` operations, resolving WSL2/ext4 inode journal overhead and speeding up image builds.
- **Environment & PATH Resolution**: Configured `/etc/profile.d/hadoop.sh` and multi-shell profile exports (`.bashrc`, `.profile`) for system-wide and user-level Hadoop/Java discovery.
- **Automation Scripts Hardening**: Upgraded `entrypoint.sh`, `healthcheck.sh`, and `test-cluster.sh` with explicit environment variable wrappers (`run_hduser`) to ensure resilient non-interactive daemon execution and command-line interactions.
- **Dynamic Configuration & Script Mounts**: Mounted `config/*.xml`, `config/hadoop-env.sh`, and `scripts/*.sh` as read-only volumes in `docker-compose.yml` for instant zero-rebuild iteration.
- **Extended Troubleshooting Runbook**: Added comprehensive runbooks for Browser `ERR_EMPTY_RESPONSE` HTTPS auto-upgrade resolution (Issue 9) and Docker Desktop engine pipe recovery (Issue 10) in `docs/troubleshooting.md`.

---

## [1.0.0] - 2026-08-10

### Added
- Multi-stage Docker image packaging Apache Hadoop 3.1.2 on Ubuntu 20.04 with OpenJDK 8.
- Single-node daemon stack: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager, and JobHistory Server.
- Non-root execution model using dedicated `hduser` user and `hadoop` group.
- Container health checks for NameNode (9870) and ResourceManager (8088).
- Docker Compose configuration with 4 named persistent volumes (`hadoop_namenode_data`, `hadoop_datanode_data`, `hadoop_tmp_data`, `hadoop_logs_data`).
- Environment variable template `.env.example` for configurable port mappings.
- Automated integration test script `scripts/test-cluster.sh` verifying HDFS and MapReduce Pi calculation.
- Automated GitHub Actions CI workflow for building and testing on Ubuntu latest.
- Developer Makefile with container lifecycle shortcuts (`build`, `up`, `down`, `test`, `bash`, `clean`).
- Base README with port table, quick start, and basic HDFS CLI instructions.
