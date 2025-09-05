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

# Comprehensive linting script
set -e

# Change to project root directory
cd "$(dirname "$0")/.." || exit 1

# Color codes
if [[ -t 1 ]]; then
    RED='\033[91m'
    GREEN='\033[92m'
    YELLOW='\033[93m'
    BLUE='\033[94m'
    BOLD='\033[1m'
    NC='\033[0m'  # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    BOLD=''
    NC=''
fi

# Print functions
print_header() {
    echo -e "\n${BOLD}$1${NC}"
}

print_step() {
    echo -e "Running $1..."
}

print_success() {
    echo -e "${GREEN}$1: PASS${NC}"
}

print_error() {
    echo -e "${RED}$1: FAIL${NC}"
}

# Default values
SOURCE_DIR="."
FIX_MODE=false
ONLY_LINTERS=()
SKIP_LINTERS=()
FAILED_LINTERS=()
PASSED_LINTERS=()

# All available linters
ALL_LINTERS=(isort black flake8 pylint mypy pydocstyle whitespace)

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE_DIR="$2"
            shift 2
            ;;
        --fix)
            FIX_MODE=true
            shift
            ;;
        --only)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                ONLY_LINTERS+=("$1")
                shift
            done
            ;;
        --skip)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                SKIP_LINTERS+=("$1")
                shift
            done
            ;;
        --help|-h)
            echo "Usage: $0 [options] [source_dir]"
            echo "Options:"
            echo "  --source DIR    Source directory to lint (default: .)"
            echo "  --fix          Auto-fix issues where possible"
            echo "  --only LINTERS Run only specified linters"
            echo "  --skip LINTERS Skip specified linters"
            echo "  --help         Show this help message"
            echo ""
            echo "Available linters: ${ALL_LINTERS[*]}"
            exit 0
            ;;
        *)
            if [[ ! "$1" =~ ^-- ]]; then
                SOURCE_DIR="$1"
            fi
            shift
            ;;
    esac
done

# Check if source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    print_error "Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Determine which linters to run
LINTERS_TO_RUN=()
if [[ ${#ONLY_LINTERS[@]} -gt 0 ]]; then
    LINTERS_TO_RUN=("${ONLY_LINTERS[@]}")
else
    LINTERS_TO_RUN=("${ALL_LINTERS[@]}")
    # Remove skipped linters
    for skip in "${SKIP_LINTERS[@]}"; do
        LINTERS_TO_RUN=("${LINTERS_TO_RUN[@]/$skip}")
    done
fi

# Function to run a linter
run_linter() {
    local linter="$1"
    local result=0
    
    print_step "$linter"
    
    local output
    case "$linter" in
        isort)
            if [[ "$FIX_MODE" == true ]]; then
                output=$(uv run isort "$SOURCE_DIR" 2>&1) || result=$?
            else
                output=$(uv run isort --check-only --diff "$SOURCE_DIR" 2>&1) || result=$?
            fi
            ;;
        black)
            if [[ "$FIX_MODE" == true ]]; then
                output=$(uv run black "$SOURCE_DIR" 2>&1) || result=$?
            else
                output=$(uv run black --check --diff "$SOURCE_DIR" 2>&1) || result=$?
            fi
            ;;
        flake8)
            output=$(uv run flake8 "$SOURCE_DIR" 2>&1) || result=$?
            ;;
        pylint)
            output=$(uv run pylint "$SOURCE_DIR" 2>&1) || result=$?
            ;;
        mypy)
            output=$(uv run mypy "$SOURCE_DIR" 2>&1) || result=$?
            ;;
        pydocstyle)
            output=$(uv run pydocstyle "$SOURCE_DIR" 2>&1) || result=$?
            ;;
        whitespace)
            if [[ "$FIX_MODE" == true ]]; then
                # Fix trailing whitespace using git ls-files (respects .gitignore)
                if [[ "$SOURCE_DIR" == "." ]]; then
                    # Use git ls-files for whole repo
                    git ls-files "*.py" | xargs -r sed -i '' 's/[[:space:]]*$//' || result=$?
                else
                    # For specific directories, use git ls-files with path filter
                    git ls-files "$SOURCE_DIR/*.py" 2>/dev/null | xargs -r sed -i '' 's/[[:space:]]*$//' || result=$?
                fi
            else
                # Check for trailing whitespace using git ls-files (respects .gitignore)
                local files_with_whitespace
                if [[ "$SOURCE_DIR" == "." ]]; then
                    # Use git ls-files for whole repo
                    files_with_whitespace=$(git ls-files "*.py" | xargs -r grep -l '[[:space:]]$' 2>/dev/null || true)
                else
                    # For specific directories, use git ls-files with path filter
                    files_with_whitespace=$(git ls-files "$SOURCE_DIR/*.py" 2>/dev/null | xargs -r grep -l '[[:space:]]$' 2>/dev/null || true)
                fi
                
                if [[ -n "$files_with_whitespace" ]]; then
                    echo "Files with trailing whitespace:"
                    echo "$files_with_whitespace"
                    result=1
                fi
            fi
            ;;
    esac
    
    if [[ $result -eq 0 ]]; then
        print_success "$linter"
        PASSED_LINTERS+=("$linter")
    else
        print_error "$linter"
        # Show error output, but filter out emoji messages from tools
        if [[ -n "$output" ]]; then
            # Filter out emoji-heavy messages from black and other tools
            filtered_output=$(echo "$output" | grep -v "All done!.*✨" | grep -v "Oh no!.*💥")
            if [[ -n "$filtered_output" ]]; then
                echo "$filtered_output"
            fi
        fi
        FAILED_LINTERS+=("$linter")
    fi
    return $result
}

# Main execution
print_header "Linting $SOURCE_DIR"
if [[ "$FIX_MODE" == true ]]; then
    echo "Auto-fix mode enabled"
fi

# Run linters
for linter in "${LINTERS_TO_RUN[@]}"; do
    [[ -n "$linter" ]] && run_linter "$linter"
done

# Print summary
if [[ ${#FAILED_LINTERS[@]} -eq 0 ]]; then
    echo -e "\n${GREEN}All ${#PASSED_LINTERS[@]} linters passed${NC}"
    exit 0
else
    echo -e "\n${RED}${#FAILED_LINTERS[@]} linter(s) failed:${NC} ${FAILED_LINTERS[*]}"
    exit 1
fi