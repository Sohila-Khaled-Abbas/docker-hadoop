## 📝 Description

Please provide a summary of the changes introduced in this pull request and the rationale behind them.

- **Related Issue**: Resolves # <!-- e.g., Resolves #12 -->

---

## 📌 Type of Change

Please mark the applicable option:
- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] ✨ New feature (non-breaking change adding functionality)
- [ ] ⚡ Performance improvement
- [ ] 🔨 Refactoring / Code cleanup
- [ ] 📚 Documentation update
- [ ] 🧪 Test addition or update
- [ ] 📦 Dependency update / CI configuration
- [ ] ⚠️ Breaking change (fix or feature causing existing functionality to break)

---

## 🧪 Testing Plan & Evidence

Please describe the tests executed to verify your changes and paste relevant output or logs.

### Verification Steps:
1. `make build` / `docker compose build`
2. `make up` / `docker compose up -d`
3. `make test` / `docker compose exec hadoop /test-cluster.sh`

### Test Output:
```text
<!-- Paste terminal test output or jps logs here -->
```

---

## ✅ Pull Request Checklist

- [ ] My code follows the project's style guidelines.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have updated corresponding documentation in `README.md` or `docs/`.
- [ ] My changes generate no new Docker build warnings or daemon runtime errors.
- [ ] All automated tests and health checks pass locally.
- [ ] I have read and agree to the [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).
