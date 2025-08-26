#!/bin/bash
#
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
#


# Get version from the generated _version.py file (created by setuptools_scm)
if [ -f "streamlit_page_analytics/_version.py" ]; then
    VERSION=$(python -c "import sys; sys.path.insert(0, '.'); from streamlit_page_analytics._version import __version__; print(__version__)" 2>/dev/null)
fi

# Fallback: try to get version from installed package
if [ -z "$VERSION" ]; then
    VERSION=$(python -c "from importlib.metadata import version; print(version('streamlit-page-analytics'))" 2>/dev/null)
fi

# Final fallback
if [ -z "$VERSION" ]; then
    VERSION="0.0.0"
fi

# Create dist directory if it doesn't exist
mkdir -p dist

# Create zip file with the package directory structure
zip -r "dist/streamlit_page_analytics-${VERSION}.zip" streamlit_page_analytics -i "*.py"