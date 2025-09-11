# Comprehensive Code Quality Setup

This project includes a comprehensive local linting setup with multiple tools working together to ensure high code quality. All linters are configured to work together harmoniously.

## Included Linters

| Tool | Purpose | Config |
|------|---------|--------|
| **black** | Code formatting | `pyproject.toml` |
| **isort** | Import sorting | `pyproject.toml` |
| **flake8** | Style guide enforcement | `setup.cfg` |
| **pylint** | Code analysis | `pyproject.toml` |
| **mypy** | Static type checking | `pyproject.toml` |
| **bandit** | Security checks | `pyproject.toml` |
| **pydocstyle** | Docstring style | `pyproject.toml` |
| **vulture** | Dead code detection | `pyproject.toml` |

## Quick Start

```bash
# Run all linters
task lint

# Run with auto-fix (where supported)
task lint-fix

# Run specific linters
task lint -- --only black isort

# Skip specific linters
task lint -- --skip pylint mypy
```

## Sample Output

```
=============================================================
CODE QUALITY CHECK
=============================================================

Source directory: streamlit_page_analytics
Python version: 3.10.0

Running black: PASS
Running isort: PASS
Running flake8: PASS
Running pylint: PASS
Running mypy: PASS
Running bandit: PASS
Running pydocstyle: PASS
Running vulture: PASS

=============================================================
LINTING SUMMARY
=============================================================

  black        PASS
  isort        PASS
  flake8       PASS
  pylint       PASS
  mypy         PASS
  bandit       PASS
  pydocstyle   PASS
  vulture      PASS

Results:
  Passed: 8
  Failed: 0

All linters passed! Code quality is excellent!
```

## Configuration

Each linter is configured in either `pyproject.toml` or `setup.cfg`:

### Black
```toml
[tool.black]
line-length = 88
target-version = ['py310']
```

### isort
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
```

### Pylint
```toml
[tool.pylint.messages_control]
disable = [
    "C0103",  # Invalid name
    "C0114",  # Missing module docstring
]
```

### mypy
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
disallow_untyped_defs = true
```

### bandit
```toml
[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]
```

### pydocstyle
```toml
[tool.pydocstyle]
convention = "google"
```

### vulture
```toml
[tool.vulture]
min_confidence = 60
```

## 🔄 Pre-commit Integration

The linting setup is integrated with Git pre-commit hooks:

```bash
# Install hooks
task install-hooks

# Test hooks
task test-hooks
```

## Tips

1. Run `task lint-fix` first to auto-fix formatting issues
2. Use `task lint -- --only <tool>` to run specific linters
3. Configure your editor to run black/isort on save
4. Review the configuration in `pyproject.toml` for customization

This setup provides comprehensive code quality checks while maintaining flexibility and ease of use!
