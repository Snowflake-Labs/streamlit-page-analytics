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

"""Tests for the mask_text_input_values feature.

This module contains tests that verify text input and text area values
are properly masked when mask_text_input_values=True is set.
"""

import io
import json
import logging

from streamlit.testing.v1 import AppTest

from streamlit_page_analytics import StreamlitPageAnalytics


def _filter_widget_logs(log_lines: list[str]) -> list[dict]:
    """Filter log lines to only include widget interaction logs (not start_tracking)."""
    result = []
    for line in log_lines:
        log_json = json.loads(line)
        if log_json.get("action") != "start_tracking":
            result.append(log_json)
    return result


# pylint: disable=no-member
def test_text_input_masked_when_enabled() -> None:
    """Test that text input values are masked when mask_text_input_values=True."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.text_input("Sensitive Input", key="sensitive_text")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-mask-text-input")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_text_input_values=True,
    ):
        at = AppTest.from_function(app)
        at.run()

        text_input = at.text_input[0]
        text_input.set_value("my secret password")
        at.run()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)
    assert len(widget_logs) == 1, f"Expected 1 widget log, got {len(widget_logs)}"

    log_json = widget_logs[0]

    # Verify the value is redacted, not the actual input
    assert log_json["widget"]["values"]["current"] == "[REDACTED]"
    assert "my secret password" not in log_stream.getvalue()


def test_text_area_masked_when_enabled() -> None:
    """Test that text area values are masked when mask_text_input_values=True."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.text_area("Sensitive Text Area", key="sensitive_area")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-mask-text-area")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_text_input_values=True,
    ):
        at = AppTest.from_function(app)
        at.run()

        text_area = at.text_area[0]
        text_area.set_value("confidential information\nwith multiple lines")
        at.run()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)
    assert len(widget_logs) == 1, f"Expected 1 widget log, got {len(widget_logs)}"

    log_json = widget_logs[0]

    # Verify the value is redacted, not the actual input
    assert log_json["widget"]["values"]["current"] == "[REDACTED]"
    assert "confidential information" not in log_stream.getvalue()


def test_text_input_not_masked_when_disabled() -> None:
    """Test text input values are NOT masked when mask_text_input_values=False."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.text_input("Normal Input", key="normal_text")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-no-mask-text-input")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_text_input_values=False,
    ):
        at = AppTest.from_function(app)
        at.run()

        text_input = at.text_input[0]
        text_input.set_value("visible text value")
        at.run()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)
    assert len(widget_logs) == 1, f"Expected 1 widget log, got {len(widget_logs)}"

    log_json = widget_logs[0]

    # Verify the actual value is logged
    assert log_json["widget"]["values"]["current"] == "visible text value"


def test_other_widgets_not_affected_by_masking() -> None:
    """Test that other widgets (selectbox) are not affected by masking."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.selectbox("Choose Option", options=["Option A", "Option B"], key="select")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-other-widgets")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_text_input_values=True,
    ):
        at = AppTest.from_function(app)
        at.run()

        selectbox = at.selectbox[0]
        selectbox.set_value("Option B")
        at.run()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)
    assert len(widget_logs) == 1, f"Expected 1 widget log, got {len(widget_logs)}"

    log_json = widget_logs[0]

    # Verify selectbox value is NOT masked
    assert log_json["widget"]["values"]["current"] == "Option B"
