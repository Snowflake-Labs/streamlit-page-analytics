# Copyright 2025 Snowflake Inc.
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

"""Tests for page tracking functionality in StreamlitPageAnalytics.

This module contains tests verifying that start_tracking() correctly logs
page visits only when the page name changes.
"""

import io
import json
import logging
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock, patch

import pytest

from streamlit_page_analytics import StreamlitPageAnalytics

# Constants for testing
_TEST_SESSION_ID = "test-session"
_TEST_USER_ID = "test-user"
_TEST_APP_NAME = "test-app"


@pytest.fixture
def mock_session_state() -> MagicMock:
    """Create a mock session state that behaves like a dict."""
    state: Dict[str, Any] = {}

    def get(key: str, default: Any = None) -> Any:
        return state.get(key, default)

    mock = MagicMock()
    mock.get = get
    mock.__setitem__ = lambda _, key, value: state.__setitem__(key, value)
    mock.__getitem__ = lambda _, key: state[key]
    mock.to_dict = state.copy
    return mock


def _create_analytics_with_logger() -> Tuple[StreamlitPageAnalytics, io.StringIO]:
    """Create a StreamlitPageAnalytics instance with a captured log stream."""
    log_stream = io.StringIO()
    logger = logging.getLogger("test-page-tracking")
    logger.handlers = []  # Clear any existing handlers
    logger.addHandler(logging.StreamHandler(log_stream))
    logger.setLevel(logging.INFO)

    analytics = StreamlitPageAnalytics(
        name=_TEST_APP_NAME,
        session_id=_TEST_SESSION_ID,
        user_id=_TEST_USER_ID,
        logger=logger,
    )
    return analytics, log_stream


def _get_log_lines(log_stream: io.StringIO) -> List[Dict[str, Any]]:
    """Parse log lines from the log stream."""
    log_stream.seek(0)
    return [json.loads(line) for line in log_stream.getvalue().splitlines() if line]


class TestPageTracking:
    """Tests for page tracking functionality."""

    def test_start_tracking_with_page_name_logs_on_first_call(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that start_tracking with page_name logs on first call."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()
            analytics.start_tracking(page_name="Home")

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 1
            assert log_lines[0]["action"] == "start_tracking"
            assert log_lines[0]["extra"]["page_name"] == "Home"
            assert log_lines[0]["session_id"] == _TEST_SESSION_ID
            assert log_lines[0]["user_id"] == _TEST_USER_ID

    def test_start_tracking_same_page_does_not_log_again(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that calling start_tracking with same page_name does not log again."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # First call - should log
            analytics.start_tracking(page_name="Home")

            # Second call with same page - should NOT log
            analytics.start_tracking(page_name="Home")

            # Third call with same page - should NOT log
            analytics.start_tracking(page_name="Home")

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 1  # Only one log entry
            assert log_lines[0]["extra"]["page_name"] == "Home"

    def test_start_tracking_different_page_logs_again(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that changing page_name triggers a new log."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # First call - logs "Home"
            analytics.start_tracking(page_name="Home")

            # Second call with different page - logs "Settings"
            analytics.start_tracking(page_name="Settings")

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 2
            assert log_lines[0]["extra"]["page_name"] == "Home"
            assert log_lines[1]["extra"]["page_name"] == "Settings"

    def test_start_tracking_page_navigation_sequence(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test a realistic page navigation sequence."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # Simulate user navigating: Home -> Settings -> Home -> Settings
            analytics.start_tracking(page_name="Home")  # Log
            analytics.start_tracking(page_name="Home")  # No log (same page)
            analytics.start_tracking(page_name="Settings")  # Log
            analytics.start_tracking(page_name="Settings")  # No log (same page)
            analytics.start_tracking(page_name="Home")  # Log (back to Home)
            analytics.start_tracking(page_name="Settings")  # Log

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 4
            assert [line["extra"]["page_name"] for line in log_lines] == [
                "Home",
                "Settings",
                "Home",
                "Settings",
            ]

    def test_start_tracking_without_page_name_does_not_log(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that start_tracking without page_name does not log any event."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # Call without page_name - should NOT log
            analytics.start_tracking()

            # Second call without page_name - should NOT log
            analytics.start_tracking()

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 0  # No log entries

    def test_start_tracking_mixed_page_name_and_no_page_name(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test behavior when mixing calls with and without page_name."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # Call without page_name first - no log
            analytics.start_tracking()

            # Call with page_name - logs
            analytics.start_tracking(page_name="Home")

            # Call with same page_name - no log
            analytics.start_tracking(page_name="Home")

            # Call without page_name again - no log
            analytics.start_tracking()

            # Call with different page_name - logs
            analytics.start_tracking(page_name="Settings")

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 2
            assert log_lines[0]["extra"]["page_name"] == "Home"
            assert log_lines[1]["extra"]["page_name"] == "Settings"

    def test_separate_analytics_instances_have_independent_tracking(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that different analytics instances track independently."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            # Create two separate analytics instances with different names
            log_stream1 = io.StringIO()
            logger1 = logging.getLogger("test-page-tracking-1")
            logger1.handlers = []
            logger1.addHandler(logging.StreamHandler(log_stream1))
            logger1.setLevel(logging.INFO)
            analytics1 = StreamlitPageAnalytics(
                name="app1",
                session_id=_TEST_SESSION_ID,
                user_id=_TEST_USER_ID,
                logger=logger1,
            )

            log_stream2 = io.StringIO()
            logger2 = logging.getLogger("test-page-tracking-2")
            logger2.handlers = []
            logger2.addHandler(logging.StreamHandler(log_stream2))
            logger2.setLevel(logging.INFO)
            analytics2 = StreamlitPageAnalytics(
                name="app2",
                session_id=_TEST_SESSION_ID,
                user_id=_TEST_USER_ID,
                logger=logger2,
            )

            # Each instance should log independently
            analytics1.start_tracking(page_name="Home")
            analytics2.start_tracking(page_name="Home")

            log_lines1 = _get_log_lines(log_stream1)
            log_lines2 = _get_log_lines(log_stream2)

            assert len(log_lines1) == 1
            assert len(log_lines2) == 1

    def test_start_tracking_with_empty_string_page_name_does_not_log(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that empty string page name does not trigger logging."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            # Empty string should not log
            analytics.start_tracking(page_name="")
            analytics.start_tracking(page_name="")

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 0  # No log entries for empty page name

    def test_start_tracking_page_name_is_case_sensitive(
        self, mock_session_state: MagicMock
    ) -> None:
        """Test that page names are case sensitive."""
        with patch("streamlit_page_analytics.streamlit_page_analytics.st") as mock_st:
            mock_st.session_state = mock_session_state

            analytics, log_stream = _create_analytics_with_logger()

            analytics.start_tracking(page_name="Home")
            analytics.start_tracking(page_name="home")  # Different - should log
            analytics.start_tracking(page_name="HOME")  # Different - should log

            log_lines = _get_log_lines(log_stream)
            assert len(log_lines) == 3
            assert [line["extra"]["page_name"] for line in log_lines] == [
                "Home",
                "home",
                "HOME",
            ]
