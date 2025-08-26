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

"""A Streamlit component for page analytics.

This package provides tools for tracking user interactions with Streamlit
applications. It automatically captures analytics events when users interact
with UI elements like buttons, checkboxes, and other components.

The main class is StreamlitPageAnalytics, which can be used as a context
manager or manually controlled to wrap Streamlit functions with analytics
tracking capabilities.

Example:
    Basic usage:

    >>> from streamlit_page_analytics import StreamlitPageAnalytics
    >>> with StreamlitPageAnalytics.track("my_app", "session_123", "user_456"):
    ...     st.button("Click me")  # This will be automatically tracked
"""

from .streamlit_page_analytics import StreamlitPageAnalytics

try:
    from ._version import __version__
except ImportError:
    # Fallback for development installations
    from importlib.metadata import version

    __version__ = version("streamlit-page-analytics")

__all__ = ["StreamlitPageAnalytics"]
