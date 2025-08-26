#!/usr/bin/env python3
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

"""Comprehensive Linting Script.

Runs comprehensive code quality checks on the codebase.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Colors:
    """Color codes for terminal output."""

    # Only use colors if we're in a terminal that supports them
    USE_COLORS = sys.stdout.isatty()

    @classmethod
    def _wrap(cls, code: str, text: str) -> str:
        """Wrap text with color code if colors are enabled."""
        if cls.USE_COLORS:
            return f"\033[{code}m{text}\033[0m"
        return text

    @classmethod
    def green(cls, text: str) -> str:
        """Green text."""
        return cls._wrap("92", text)

    @classmethod
    def yellow(cls, text: str) -> str:
        """Yellow text."""
        return cls._wrap("93", text)

    @classmethod
    def red(cls, text: str) -> str:
        """Red text."""
        return cls._wrap("91", text)

    @classmethod
    def blue(cls, text: str) -> str:
        """Blue text."""
        return cls._wrap("94", text)

    @classmethod
    def bold(cls, text: str) -> str:
        """Bold text."""
        return cls._wrap("1", text)


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.blue(Colors.bold('='*60))}")
    print(f"{Colors.blue(Colors.bold(text.center(60)))}")
    print(f"{Colors.blue(Colors.bold('='*60))}\n")


def print_step(text: str) -> None:
    """Print a step description."""
    print(f"{Colors.yellow('>> ' + text)}")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.green('[PASS] ' + text)}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.red('[FAIL] ' + text)}")


def run_command(
    cmd: List[str],
    description: str,  # noqa: F841  # vulture: ignore - used for documentation
    cwd: Optional[Path] = None,
) -> Tuple[bool, str]:
    """Run a command and return success status and output.

    Args:
        cmd: The command to run as a list of strings.
        description: Description of what the command does.
        cwd: Working directory to run the command in.

    Returns:
        A tuple of (success, output) where success is a boolean indicating
        whether the command succeeded, and output is the command output
        (stdout if successful, stderr if failed).
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=False,  # We handle the return code ourselves
        )

        if result.returncode == 0:
            return True, result.stdout

        return False, result.stderr or result.stdout

    except subprocess.TimeoutExpired:
        return False, "Command timed out after 5 minutes"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"
    except Exception as e:  # pylint: disable=broad-except
        return False, str(e)


def check_trailing_whitespace(source_path: str) -> bool:
    """Check for trailing whitespace in files.

    Args:
        source_path: Path to check for trailing whitespace.

    Returns:
        True if no trailing whitespace found, False otherwise.
    """
    # Define directories to ignore
    ignore_dirs = [
        ".git",
        "dist",
        "__pycache__",
        "*.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        "build",
        ".venv",
        ".tox",
    ]

    # Build grep command with exclude dirs
    cmd = ["grep", "-r", "-l", "[[:space:]]$"]
    for d in ignore_dirs:
        cmd.extend(["--exclude-dir", d])
    cmd.append(source_path)

    _, output = run_command(cmd, "trailing whitespace check")

    # grep returns 0 when it finds matches (which is bad for us)
    # and 1 when it doesn't find matches (which is good for us)
    if output.strip():
        print_error("Found files with trailing whitespace:")
        for file in output.strip().split("\n"):
            print(f"  {file}")
        return False
    return True


def get_ignore_patterns() -> List[str]:
    """Get common ignore patterns for linters.

    Returns:
        List of ignore patterns for command line tools.
    """
    return [
        "--exclude",
        "*.git/*",
        "--exclude",
        "dist/*",
        "--exclude",
        "build/*",
        "--exclude",
        "__pycache__/*",
        "--exclude",
        "*.egg-info/*",
        "--exclude",
        ".pytest_cache/*",
        "--exclude",
        ".mypy_cache/*",
        "--exclude",
        ".venv/*",
        "--exclude",
        ".tox/*",
    ]


def get_linter_commands(fix_mode: bool = False) -> Dict[str, List[str]]:
    """Get linter commands based on mode.

    Args:
        fix_mode: Whether to return commands in fix mode.

    Returns:
        Dictionary of linter names to commands.
    """
    ignore_patterns = get_ignore_patterns()

    linters = {
        "isort": ["pipenv", "run", "isort", "--check-only", "--diff"],
        "black": ["pipenv", "run", "black", "--check", "--diff"],
        "flake8": ["pipenv", "run", "flake8"] + ignore_patterns,
        "pylint": ["pipenv", "run", "pylint"],
        "mypy": ["pipenv", "run", "mypy"],
        "pydocstyle": ["pipenv", "run", "pydocstyle"],
    }

    if fix_mode:
        linters["isort"] = ["pipenv", "run", "isort"]
        linters["black"] = ["pipenv", "run", "black"]
        linters["whitespace"] = [
            "find",
            ".",
            "!",
            "-path",
            "./.git/*",
            "!",
            "-path",
            "./dist/*",
            "!",
            "-path",
            "./__pycache__/*",
            "!",
            "-path",
            "./*.egg-info/*",
            "!",
            "-path",
            "./.pytest_cache/*",
            "!",
            "-path",
            "./.mypy_cache/*",
            "!",
            "-path",
            "./build/*",
            "!",
            "-path",
            "./.venv/*",
            "!",
            "-path",
            "./.tox/*",
            "-type",
            "f",
            "-exec",
            "sed",
            "-i",
            "s/[[:space:]]*$//",
            "{}",
            "+",
        ]
    else:
        linters["whitespace"] = ["echo", "Using custom whitespace check"]

    return linters


def print_summary(results: Dict[str, bool]) -> int:
    """Print linting summary and return exit code.

    Args:
        results: Dictionary of linter names to success status.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print_header("LINTING SUMMARY")

    passed = sum(1 for success in results.values() if success)
    failed = len(results) - passed

    for name, success in results.items():
        status = Colors.green("PASS") if success else Colors.red("FAIL")
        print(f"  {name:<12} {status}")

    print(f"\n{Colors.bold('Results:')}")
    print(f"  [PASS] {Colors.green(str(passed))}")
    print(f"  [FAIL] {Colors.red(str(failed))}")

    if failed == 0:
        print(
            f"\n{Colors.green(Colors.bold('All linters passed! Code quality is excellent!'))}"
        )
        return 0

    print(
        f"\n{Colors.red(Colors.bold(f'{failed} linter(s) failed. Please fix the issues above.'))}"
    )
    return 1


def run_linter(name: str, cmd: List[str], source_path: str) -> bool:
    """Run a single linter and return success status.

    Args:
        name: Name of the linter.
        cmd: Command to run the linter.
        source_path: Path to the source code to lint.

    Returns:
        True if the linter passed, False otherwise.
    """
    print_step(f"Running {name}")

    # Add source path to command
    full_cmd = cmd + [source_path]

    success, output = run_command(full_cmd, name)

    if success:
        print_success(f"{name} passed")
        if output.strip():
            print(f"  Output: {output.strip()}")
    else:
        print_error(f"{name} failed")
        if output.strip():
            print(f"  Output: {output.strip()}")

    print()  # Add spacing
    return success


def filter_linters(
    linters: Dict[str, List[str]],
    only: Optional[List[str]] = None,
    skip: Optional[List[str]] = None,
    source_path: str = ".",
) -> Dict[str, List[str]]:
    """Filter linters based on command line arguments.

    Args:
        linters: Dictionary of linter names to commands.
        only: List of linters to run exclusively.
        skip: List of linters to skip.
        source_path: Source path being linted.

    Returns:
        Filtered dictionary of linter commands.
    """
    if only:
        return {k: v for k, v in linters.items() if k in only}
    if skip:
        return {k: v for k, v in linters.items() if k not in skip}

    # No special handling needed for test files
    # All linters should be applied to test files as well

    return linters


def main() -> None:
    """Main linting function."""
    parser = argparse.ArgumentParser(
        description="Run comprehensive code quality checks"
    )
    parser.add_argument(
        "--source",
        default=".",
        help="Source directory to lint (default: .)",
    )
    parser.add_argument(
        "--skip", nargs="+", help="Linters to skip (e.g., --skip pylint mypy)"
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="Only run specific linters (e.g., --only black flake8)",
    )
    parser.add_argument(
        "--fix", action="store_true", help="Auto-fix issues where possible"
    )

    args = parser.parse_args()

    # Verify source path exists
    source_path = Path(args.source)
    if not source_path.exists():
        print_error(f"Source path does not exist: {source_path}")
        sys.exit(1)

    print_header("CODE QUALITY CHECK")
    print(f"Source directory: {Colors.bold(str(source_path))}")
    print(f"Python version: {Colors.bold(sys.version.split()[0])}")

    if args.fix:
        print(f"{Colors.yellow('Auto-fix mode enabled')}\n")

    # Get and filter linter commands
    linters = get_linter_commands(args.fix)
    linters = filter_linters(linters, args.only, args.skip, str(source_path))

    # Run all linters
    results: Dict[str, bool] = {}
    for name, cmd in linters.items():
        if name == "whitespace":
            results[name] = check_trailing_whitespace(str(source_path))
        else:
            results[name] = run_linter(name, cmd, str(source_path))

    # Print summary and exit
    sys.exit(print_summary(results))


if __name__ == "__main__":
    main()
