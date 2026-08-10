# Contributing to Apache Hadoop Docker

Thank you for your interest in contributing to this project! We welcome contributions from big data practitioners, students, developers, and educators. This guide outlines the development standards, Git workflows, and pull request procedures for this repository.

---

## 📑 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Git Workflow & Branching Strategy](#git-workflow--branching-strategy)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Security Vulnerabilities](#security-vulnerabilities)

---

## 🤝 Code of Conduct

All contributors and maintainers are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating in discussions or opening pull requests.

---

## 💡 How Can I Contribute?

You can contribute in multiple ways:

1. **Reporting Bugs**: File detailed bug reports via [GitHub Issues](https://github.com/your-username/docker-hadoop/issues/new?template=bug_report.md) with reproduction steps and container logs.
2. **Proposing Enhancements**: Suggest performance improvements, ecosystem integrations (e.g. Hive, Spark, Presto), or Docker optimizations via [Feature Requests](https://github.com/your-username/docker-hadoop/issues/new?template=feature_request.md).
3. **Improving Documentation**: Fix typos, add examples, enhance architecture diagrams, or write troubleshooting guides.
4. **Submitting Code**: Submit bug fixes, script improvements, or configuration tuning via Pull Requests.

---

## 🛠️ Development Setup

### Prerequisites

Ensure you have the following installed locally:
- [Git](https://git-scm.com/) (v2.30+)
- [Docker Engine](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)
- [Make](https://www.gnu.org/software/make/) (optional, for developer shortcuts)

### Fork and Clone

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/docker-hadoop.git
   cd docker-hadoop
   ```
3. Set the upstream remote:
   ```bash
   git remote add upstream https://github.com/your-username/docker-hadoop.git
   ```

### Local Build & Run

```bash
# Build the Docker image locally
docker compose build

# Start the cluster in detached mode
docker compose up -d

# Verify daemon status
docker compose exec hadoop jps
```

---

## 🌿 Git Workflow & Branching Strategy

We follow a **feature branch workflow** based on Git Flow:

- `main` / `master`: Production-ready branch containing tested releases.
- `feat/<feature-name>`: For new features and enhancements (e.g., `feat/add-spark-support`).
- `fix/<bug-name>`: For bug fixes (e.g., `fix/namenode-safemode-timeout`).
- `docs/<topic>`: For documentation updates (e.g., `docs/mapreduce-tuning`).
- `refactor/<module>`: For code restructuring without behavior changes.

### Creating a Branch

Always branch off the latest `main` branch:
```bash
git checkout main
git pull upstream main
git checkout -b feat/my-new-feature
```

---

## 💬 Commit Message Conventions

We enforce the [Conventional Commits](https://www.conventionalcommits.org/) standard. Commit messages must follow this structure:

```text
<type>(<optional scope>): <short summary in imperative mood>

[optional body explaining motivation and context]

[optional footer(s) such as Closes #123]
```

### Supported Types

| Type | Purpose | Example |
| :--- | :--- | :--- |
| `feat` | A new feature or capability | `feat(docker): add multi-stage build caching` |
| `fix` | A bug fix | `fix(entrypoint): prevent infinite loop on NameNode format` |
| `docs` | Documentation only changes | `docs(readme): add Spark integration guide` |
| `refactor` | Code change that neither fixes a bug nor adds a feature | `refactor(scripts): streamline healthcheck daemon checks` |
| `perf` | A code change that improves performance | `perf(yarn): optimize node manager container allocation` |
| `test` | Adding or modifying tests | `test(ci): add Python streaming MapReduce integration test` |
| `chore` | Build process, auxiliary tools, or dependency updates | `chore(deps): bump base Ubuntu image digest` |

---

## 🚀 Pull Request Guidelines

Before submitting your PR:

1. **Keep PRs Focused**: A pull request should address a single concern or feature.
2. **Run Local Tests**: Execute `make test` or `docker compose exec hadoop /test-cluster.sh` to ensure all daemons and MapReduce jobs succeed.
3. **Update Documentation**: If you modify configuration parameters or container scripts, update the relevant files in `docs/` and `README.md`.
4. **Fill Out the PR Template**: Provide a concise summary, test evidence, and reference related issues (e.g., `Resolves #42`).

### Pull Request Lifecycle

```text
Fork & Branch ➡️ Make Changes ➡️ Local Test ➡️ Open PR ➡️ CI Automated Checks ➡️ Code Review ➡️ Merge
```

---

## 🧪 Testing & Quality Assurance

All PRs must pass automated CI checks. You should verify your changes locally before pushing:

```bash
# 1. Start clean cluster
make clean
make build
make up

# 2. Run automated test suite
make test

# 3. Test MapReduce Pi calculation
docker compose exec hadoop yarn jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.2.jar pi 2 5

# 4. Verify Web UIs respond
curl -f -s http://localhost:9870 > /dev/null && echo "NameNode UI OK"
curl -f -s http://localhost:8088 > /dev/null && echo "ResourceManager UI OK"
```

---

## 🔒 Security Vulnerabilities

If you discover a security vulnerability, please do **not** open a public issue. Review our [Security Policy](SECURITY.md) for instructions on responsible disclosure.
