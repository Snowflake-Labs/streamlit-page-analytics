# Development Workflow Guide

Complete guide for maintaining code quality with automated checks at every stage of development.

## Quick Setup

```bash
# 1. Install all dependencies
task install

# 2. Install Git hooks for automatic quality checks
task install-hooks

# 3. Test your setup
task test-hooks
```

## 🔄 Development Workflow

### Local Development

#### Before You Start Coding
```bash
# Ensure dependencies are up-to-date
task install
```

#### While Coding
```bash
# Quick feedback loop during development
task lint-quick

# Auto-fix formatting issues
task lint-fix
```

#### Before Committing
```bash
# Full code quality check
task lint

# If issues found, auto-fix what's possible
task lint-fix

# Commit (pre-commit hook will run automatically)
git add .
git commit -m "Your commit message"
```

### Automated Quality Gates

#### 1. Pre-Commit Hook
**Automatically runs before each commit**

```
Running pre-commit linting checks...
Running quick linters (black, flake8, isort)...
Pre-commit linting checks passed!
Commit proceeding...
```

**What it checks:**
- Code formatting (black)
- Import sorting (isort)
- Style compliance (flake8)

**If it fails:**
- Commit is blocked
- Shows how to fix issues
- Run `task lint-fix` to auto-fix

#### 2. GitHub Workflow
**Runs on push and pull requests**

**Comprehensive checks:**
- All 8 linters (black, isort, flake8, pylint, mypy, bandit, pydocstyle, vulture)
- Security vulnerability scanning
- Type checking
- Documentation standards

**Advanced features:**
- Detailed reports in GitHub Actions summary
- 💬 Automatic PR comments with results
- Artifact uploads for linting reports
- Critical security checks (mandatory)
- Style warnings (informational)

## Quality Gates Overview

| Stage      | Check              | Tools                | Action on Failure |
|------------|--------------------|----------------------|-------------------|
| **Local**  | Quick format check | black, isort, flake8 | Block commit      |
| **GitHub** | Security scan      | bandit               | Block PR          |
| **GitHub** | Type checking      | mypy                 | Report only       |
| **GitHub** | Style check        | pylint, pydocstyle   | Report only       |
| **GitHub** | Dead code          | vulture              | Report only       |

## Available Commands

### Linting Commands
```bash
# Run all linters (comprehensive)
task lint

# Auto-fix formatting issues
task lint-fix

# Quick checks (development)
task lint-quick

# Custom linter selection
task lint -- --only black flake8
task lint -- --skip pylint mypy
```

### Git Hook Commands
```bash
# Install pre-commit hooks
task install-hooks

# Test the hooks work
task test-hooks

# Bypass hooks (not recommended)
git commit --no-verify
```

### Development Commands
```bash
# Install/update dependencies
task install

# Run tests
task test

# Run tests with coverage report
task test-cov

# Clean build artifacts
task clean

# Show all commands
task help
```

## Troubleshooting

### Pre-Commit Hook Issues

**Problem: Hook not running**
```bash
# Reinstall hooks
task install-hooks
```

**Problem: Hook fails**
```bash
# Auto-fix issues
task lint-fix

# Check what's failing
task lint-quick

# Skip hook (emergency only)
git commit --no-verify
```

### GitHub Workflow Issues

**Problem: Workflow failing**
1. Check the GitHub Actions tab for detailed logs
2. Look at the job summary for specific linting results
3. Fix issues locally and push again

**Problem: Security check failure**
- This is critical and blocks PRs
- Review bandit output carefully
- Fix security issues before proceeding

## 📖 Configuration Details

### Linter Configurations
- **Main config**: `pyproject.toml`
- **Flake8 config**: `setup.cfg`
- **Consistent settings**: 88 char line length, black compatibility

### Git Hook Configuration
- **Location**: `.git/hooks/pre-commit`
- **Scope**: Quick linters only (fast feedback)
- **Bypass**: `git commit --no-verify`

### GitHub Workflow Configuration
- **File**: `.github/workflows/lint.yml`
- **Triggers**: Push to main/dev, PRs to main
- **Scope**: All linters (comprehensive)
- **Reports**: PR comments, job summaries, artifacts

## Best Practices

### Daily Development
1. **Start with clean state**: `task install`
2. **Code with quick feedback**: `task lint-quick`
3. **Fix before committing**: `task lint-fix`
4. **Let hooks guide you**: Don't bypass unless emergency

### Code Reviews
1. **Check GitHub Actions**: Ensure all checks pass
2. **Review PR comments**: Address linting suggestions
3. **Security first**: Never ignore bandit failures
4. **Style matters**: Consider pylint suggestions

### Team Workflow
1. **Consistent tooling**: Everyone uses same linter versions
2. **Shared configs**: All settings in version control
3. **Document exceptions**: Use `# noqa` comments sparingly
4. **Continuous improvement**: Update configs as needed

## Emergency Procedures

### Bypass Pre-Commit Hook
```bash
# Only in emergencies (hotfixes, etc.)
git commit --no-verify -m "Emergency fix: description"

# Follow up immediately
task lint-fix
git add .
git commit -m "Fix linting issues from emergency commit"
```

### Disable Specific Linters
```bash
# Temporarily skip problematic linters
task lint -- --skip pylint vulture

# For specific issues, use inline comments
# pylint: disable=line-too-long
# type: ignore
# noqa: F401
```

## Monitoring Code Quality

### GitHub Insights
- Check Actions tab for workflow success rates
- Review PR comments for common issues
- Monitor artifact downloads for detailed reports

### Local Metrics
```bash
# Full quality report
task lint

# Security-focused check
task lint -- --only bandit

# Type coverage check
task lint -- --only mypy

# Code coverage report
task test-cov
```

## Success Indicators

**Green commits**: Pre-commit hook passes
**Green PRs**: All GitHub workflows pass
**Clean reports**: Minimal linting issues
**Fast development**: No blocking on style issues
**Secure code**: Zero security vulnerabilities
**High coverage**: Code coverage above 90%

## 🔗 Related Documentation

- **[LINTING.md](./LINTING.md)** - Detailed linter configuration
- **[.github/workflows/lint.yml](./.github/workflows/lint.yml)** - GitHub workflow
- **[Taskfile](./Taskfile.yaml)** - Available commands
- **[pyproject.toml](./pyproject.toml)** - Tool configurations

---

**Your code is now protected by comprehensive quality gates at every stage!**
