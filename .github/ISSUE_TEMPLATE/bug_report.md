---
name: 🐛 Bug Report
about: Create a report to help us reproduce and fix an issue
title: '[BUG]: '
labels: ['bug', 'triage']
assignees: ''
---

## 🐛 Bug Description
A clear and concise description of what the bug is.

---

## 🔁 Reproduction Steps

Steps to reproduce the behavior:
1. Run command `...`
2. Open URL `http://localhost:...`
3. Execute HDFS/YARN command `...`
4. See error output:

---

## 💻 Expected Behavior
A clear and concise description of what you expected to happen.

---

## 📋 Environment & Versions

- **Host Operating System**: [e.g. Ubuntu 22.04, macOS 14 (M-series / Intel), Windows 11 WSL2]
- **Docker Version**: [e.g. 24.0.7 (`docker --version`)]
- **Docker Compose Version**: [e.g. 2.23.0 (`docker compose version`)]
- **Hadoop Version**: 3.1.2

---

## 📜 Logs & Daemon Diagnostics

Please attach or paste output from the following diagnostic commands:

<details>
<summary><code>docker compose ps</code></summary>

```text
<!-- Paste output here -->
```
</details>

<details>
<summary><code>docker compose exec hadoop jps</code></summary>

```text
<!-- Paste running Java daemons here -->
```
</details>

<details>
<summary><code>docker compose logs hadoop --tail 50</code></summary>

```text
<!-- Paste container logs here -->
```
</details>

---

## 📌 Additional Context
Add any other context about the problem here (e.g. customized ports in `.env`, custom XML configuration properties, host resource limits).
