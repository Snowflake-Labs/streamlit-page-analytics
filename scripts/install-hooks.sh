#!/bin/bash
# Copyright 2025 Snowflake Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Install or update Git hooks for Streamlit Page Analytics

set -e

echo "🔧 Installing Git hooks..."

# Get the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.git/hooks"

# Ensure hooks directory exists
mkdir -p "$HOOKS_DIR"

# Install pre-commit hook
echo "📝 Installing pre-commit hook..."
cp "$REPO_ROOT/.git/hooks/pre-commit" "$HOOKS_DIR/pre-commit" 2>/dev/null || {
    echo "⚠️  Pre-commit hook file not found, creating from template..."
    cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
# Git pre-commit hook for Streamlit Page Analytics
# Runs quick linting checks before allowing commits

set -e  # Exit on any error

echo "🔍 Running pre-commit linting checks..."

# Change to repository root
cd "$(git rev-parse --show-toplevel)"

# Check if pipenv is available
if ! command -v pipenv &> /dev/null; then
    echo "❌ Error: pipenv is not installed or not in PATH"
    echo "Please install pipenv to run linting checks"
    exit 1
fi

# Check if virtual environment exists
if ! pipenv --venv &> /dev/null; then
    echo "❌ Error: pipenv virtual environment not found"
    echo "Please run 'pipenv install --dev' to set up the environment"
    exit 1
fi

# Run quick linting checks (black, flake8, isort)
echo "⚡ Running quick linters (black, flake8, isort)..."
if pipenv run python3 scripts/lint.py --only black flake8 isort --source streamlit_page_analytics; then
    echo "✅ Pre-commit linting checks passed!"
    echo "📝 Commit proceeding..."
else
    echo ""
    echo "❌ Pre-commit linting checks failed!"
    echo ""
    echo "💡 To fix formatting issues automatically, run:"
    echo "   make lint-fix"
    echo ""
    echo "💡 To skip this check (not recommended), run:"
    echo "   git commit --no-verify"
    echo ""
    exit 1
fi
EOF
}

# Make hooks executable
chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Git hooks installed successfully!"
echo ""
echo "📋 Installed hooks:"
echo "  - pre-commit: Runs quick linting checks before commits"
echo ""
echo "💡 Tips:"
echo "  - Test the hook: git commit --dry-run"
echo "  - Skip the hook: git commit --no-verify"
echo "  - Fix issues: make lint-fix"
echo ""
echo "🎉 Your repository is now protected by automated code quality checks!"
