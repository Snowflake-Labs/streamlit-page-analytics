# Streamlit Page Analytics Makefile
# Provides convenient commands for development workflow

.PHONY: help lint lint-fix lint-quick lint-tests install test test-cov clean deep-clean install-hooks test-hooks license build-wheel build-zip build-tar build-all

# Build wheel distribution
build-wheel: clean
	@echo "🔨 Building wheel distribution..."
	pipenv run python -m build --wheel

# Build zip source distribution
build-zip: clean
	@echo "🔨 Building zip source distribution..."
	./scripts/make_zip_dist.sh

# Build tar.gz source distribution
build-tar: clean
	@echo "🔨 Building tar.gz source distribution..."
	pipenv run python -m build --sdist

# Build all distributions
build-all: clean
	@echo "🔨 Building all distributions..."
	pipenv run python -m build --wheel
	pipenv run python -m build --sdist
	./scripts/make_zip_dist.sh

# Default target
help:
	@echo "🚀 Streamlit Page Analytics Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  lint         - Run all linters on source and tests"
	@echo "  lint-fix     - Run linters with auto-fix enabled"
	@echo "  lint-quick   - Run only fast linters (black, flake8, isort)"
	@echo "  license      - Add/update license headers in all files"
	@echo "  install      - Install package in development mode"
	@echo "  install-hooks- Install Git pre-commit hooks"
	@echo "  test-hooks   - Test the pre-commit hook"
	@echo "  test         - Run tests (matches CI environment)"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  clean        - Remove build artifacts and caches"
	@echo "  deep-clean   - Remove all generated files including virtual env"
	@echo "  build-wheel  - Build wheel distribution"
	@echo "  build-zip    - Build zip source distribution"
	@echo "  build-tar    - Build tar.gz source distribution"
	@echo "  build-all    - Build all distribution formats"
	@echo ""
	@echo "Examples:"
	@echo "  make lint                     # Full linting suite"
	@echo "  make lint-fix                # Fix formatting issues"
	@echo "  make lint ARGS='--only black flake8'  # Run specific linters"
	@echo "  make install-hooks           # Set up Git hooks"
	@echo "  make build-all              # Build all distribution formats"

# Run comprehensive linting (matches CI)
lint:
	@echo "🔍 Running comprehensive linting suite..."
	pipenv run python3 scripts/lint.py --source streamlit_page_analytics $(ARGS)
	pipenv run python3 scripts/lint.py --source tests $(ARGS)

# Run linters with auto-fix
lint-fix:
	@echo "🔧 Running linters with auto-fix..."
	-pipenv run python3 scripts/lint.py --source streamlit_page_analytics --fix
	-pipenv run python3 scripts/lint.py --source tests --fix
	@echo "✅ Linting completed. Fix any remaining issues manually."

# Add/update license headers
license:
	@echo "📝 Adding/updating license headers..."
	./scripts/add_license.sh

# Run only fast linters for quick feedback
lint-quick:
	@echo "⚡ Running quick linters..."
	pipenv run python3 scripts/lint.py --source streamlit_page_analytics --only black flake8 isort
	pipenv run python3 scripts/lint.py --source tests --only black flake8 isort

# Install dependencies (matches CI environment)
install:
	@echo "📦 Installing dependencies..."
	python -m pip install --upgrade pip
	pip install pipenv
	pipenv install --dev
	pipenv run pip install -e .

# Install Git hooks
install-hooks:
	@echo "🔧 Installing Git hooks..."
	./scripts/install-hooks.sh

# Test pre-commit hook
test-hooks:
	@echo "🧪 Testing pre-commit hook..."
	@if [ -f .git/hooks/pre-commit ]; then \
		echo "Running pre-commit hook test..."; \
		./.git/hooks/pre-commit; \
	else \
		echo "❌ Pre-commit hook not found. Run 'make install-hooks' first."; \
		exit 1; \
	fi

# Run tests (matches CI environment)
test:
	@echo "🧪 Running tests..."
	pipenv run pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "🧪 Running tests with coverage..."
	pipenv run pytest tests/ -v --cov=streamlit_page_analytics --cov-report=term-missing --cov-report=html --cov-report=xml
	@echo "✅ Coverage report generated in HTML format at htmlcov/index.html"
	@echo "✅ Coverage report generated in XML format at coverage.xml"

# Clean build artifacts and caches
clean:
	@echo "🧹 Cleaning build artifacts and caches..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	find . -type d -name ".eggs" -exec rm -rf {} +
	find . -type f -name "*.egg" -delete
	@echo "✨ Clean complete!"

# Deep clean - removes everything including virtual environment
deep-clean: clean
	@echo "🧹 Deep cleaning - removing all generated files..."
	rm -rf .venv/
	rm -rf Pipfile.lock
	@echo "⚠️  Virtual environment removed. Run 'make install' to recreate it."
	@echo "✨ Deep clean complete!"
