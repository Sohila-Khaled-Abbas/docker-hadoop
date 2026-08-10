# Security Policy

The maintainers of **Apache Hadoop Docker** take security seriously. This document outlines our supported versions, reporting procedures for security vulnerabilities, and security best practices for running Apache Hadoop in containerized environments.

---

## 🛡️ Supported Versions

We provide security updates and patches for the following versions:

| Version | Supported | Notes |
| :--- | :---: | :--- |
| `3.1.x` | ✅ | Current active development & maintenance branch |
| `< 3.1.0` | ❌ | End of Life (EOL) |

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow responsible disclosure guidelines:

1. **Do NOT file a public issue.**
2. Send a confidential report to the maintainers or create a **Private Security Advisory** on GitHub via `Security > Advisories > New draft advisory`.
3. In your report, please include:
   - A detailed description of the vulnerability.
   - Steps to reproduce the issue (including any PoC scripts or configurations).
   - Potential impact and affected components (e.g. HDFS RPC, Web UIs, SSH, Container isolation).
   - Any suggested mitigations or patches.

### Response Timeline

- **Initial Acknowledgement**: Within 48 hours.
- **Triage & Assessment**: Within 5 business days.
- **Fix & Advisory Release**: Coordinated with the reporter following testing.

---

## 🔒 Security Best Practices for Containerized Hadoop

When deploying or experimenting with this container, please note the following security considerations:

### 1. Non-Root Execution
- Hadoop daemons in this container execute under a dedicated non-privileged user (`hduser`) and group (`hadoop`).
- Avoid running container processes directly as `root` in production environments.

### 2. Network Exposure & Firewalls
- By default, `docker-compose.yml` binds ports to `0.0.0.0` (accessible from `localhost` and local networks).
- For staging or multi-tenant servers, bind ports explicitly to `127.0.0.1` in your `.env` or `docker-compose.yml` file to prevent unauthorized network access.

### 3. SSH Credentials & Keys
- The default image contains pre-generated SSH host and client keys intended solely for **local single-node development and CI testing**.
- **Never deploy this container to a public-facing network** without changing the default passwords and rotating the SSH keys.

### 4. HDFS Permissions & Kerberos
- In this development setup, `dfs.permissions.enabled` is set to `false` for ease of local experimentation and learning.
- For production enterprise clusters, enable HDFS ACLs, POSIX permissions, and Kerberos authentication (`hadoop.security.authentication = kerberos`).
