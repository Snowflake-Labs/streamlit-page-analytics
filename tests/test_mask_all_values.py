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

"""Tests for the mask_all_values feature.

This module contains tests that verify all widget values
are properly masked when mask_all_values=True is set.
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
def test_text_input_masked_when_mask_all_values_enabled() -> None:
    """Test that text input values are masked when mask_all_values=True."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.text_input("Sensitive Input", key="sensitive_text")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-mask-all-text-input")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_all_values=True,
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

    assert log_json["widget"]["values"]["current"] == "[REDACTED]"
    assert "my secret password" not in log_stream.getvalue()


def test_selectbox_masked_when_mask_all_values_enabled() -> None:
    """Test that selectbox values are masked when mask_all_values=True."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.selectbox("Choose Option", options=["Option A", "Option B"], key="select")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-mask-all-selectbox")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_all_values=True,
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

    assert log_json["widget"]["values"]["current"] == "[REDACTED]"
    assert "Option B" not in json.dumps(log_json["widget"]["values"])


def test_slider_masked_when_mask_all_values_enabled() -> None:
    """Test that slider values are masked when mask_all_values=True."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.slider("Choose Value", min_value=0, max_value=100, value=50, key="slider")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-mask-all-slider")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_all_values=True,
    ):
        at = AppTest.from_function(app)
        at.run()

        slider = at.slider[0]
        slider.set_value(75)
        at.run()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)
    assert len(widget_logs) == 1, f"Expected 1 widget log, got {len(widget_logs)}"

    log_json = widget_logs[0]

    assert log_json["widget"]["values"]["current"] == "[REDACTED]"


def test_widgets_not_masked_when_mask_all_values_disabled() -> None:
    """Test that widget values are NOT masked when mask_all_values=False."""

    def app() -> None:
        # pylint: disable=import-outside-toplevel
        import streamlit as st

        st.selectbox("Choose Option", options=["Option A", "Option B"], key="select")

    log_stream = io.StringIO()
    logger = logging.getLogger("test-no-mask-all")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name="test-app",
        session_id="test-session",
        user_id="test-user",
        logger=logger,
        mask_all_values=False,
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

    assert log_json["widget"]["values"]["current"] == "Option B"
