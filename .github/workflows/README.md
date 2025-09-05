# GitHub Workflows for Distribution Building

This directory contains GitHub Actions workflows for automatically building and distributing the `streamlit-page-analytics` package.

## Workflows

### 🚀 `build-distributions.yml` - Release Build & Upload

**Purpose**: Automatically builds and uploads distributions when a release is published.

**Triggers**:
- ✅ **Automatic**: When a GitHub release is published
- ⚡ **Manual**: Can be triggered manually from the Actions tab

**What it builds**:
- 📦 **Wheel** (`.whl`) - Binary distribution for fast installation
- 🗜️ **ZIP** (`.zip`) - Source distribution in ZIP format
- 📁 **TAR.GZ** (`.tar.gz`) - Source distribution in compressed tar format

**Outputs**:
- Uploads all three formats to the GitHub release as downloadable assets
- Stores distributions as workflow artifacts (90-day retention)
- Provides a detailed summary with file sizes

**Usage**:
1. Create a GitHub release with a tag (e.g., `v1.0.0`)
2. The workflow automatically triggers and builds distributions
3. Downloads become available on the release page

### 🧪 `test-build.yml` - Build Validation

**Purpose**: Validates that distributions can be built successfully on PRs and pushes.

**Triggers**:
- Pull requests to `main` branch
- Pushes to `main` and `develop` branches

**What it does**:
- Builds all three distribution formats
- Verifies each format was created successfully
- Stores test artifacts (7-day retention)
- Fails the workflow if any build issues occur

## Manual Trigger

You can manually run the release workflow:

1. Go to **Actions** tab in your GitHub repository
2. Select **"Build and Release Distributions"**
3. Click **"Run workflow"**
4. Choose whether to upload to the latest release (if available)

## File Formats Explained

| Format | Extension | Description | Use Case |
|--------|-----------|-------------|----------|
| Wheel | `.whl` | Pre-built binary distribution | Fast installation via `pip install` |
| ZIP | `.zip` | Source code in ZIP archive | Source distribution, easy extraction |
| TAR.GZ | `.tar.gz` | Source code in compressed tar | Traditional Unix/Linux source format |

## Installation Examples

```bash
# Install from wheel (fastest)
pip install streamlit_page_analytics-1.0.0-py3-none-any.whl

# Install from source (ZIP)
pip install streamlit_page_analytics-1.0.0.zip

# Install from source (TAR.GZ)
pip install streamlit_page_analytics-1.0.0.tar.gz
```

## Requirements

- Python 3.10+
- uv for dependency management
- setuptools and build tools
