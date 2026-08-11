# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
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
- **Dockerfile Build Optimization**: Added automated pruning of `/usr/local/hadoop/share/doc` (~60,000 redundant documentation and Javadoc files) before recursive `chown`/`chmod` operations, resolving WSL2/ext4 inode journal overhead and speeding up image builds.
- **Environment & PATH Resolution**: Configured `/etc/profile.d/hadoop.sh` and multi-shell profile exports (`.bashrc`, `.profile`) for system-wide and user-level Hadoop/Java discovery.
- **Automation Scripts Hardening**: Upgraded `entrypoint.sh`, `healthcheck.sh`, and `test-cluster.sh` with explicit environment variable wrappers (`run_hduser`) to ensure resilient non-interactive daemon execution and command-line interactions.


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
