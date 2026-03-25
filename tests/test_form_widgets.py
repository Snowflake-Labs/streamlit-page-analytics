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

# Nested imports in app(); AppTest types are incomplete for pylint.
# pylint: disable=import-outside-toplevel,no-member
"""Tests for st.form() instrumentation and submit-time value logging."""

import io
import logging

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test

from streamlit_page_analytics import StreamlitPageAnalytics


def test_form_text_input_and_submit_logs_values() -> None:
    """Form fields do not use on_change; submit emits one event with field values."""

    def app() -> None:
        import streamlit as st

        with st.form("my_form"):
            st.text_input("Email", key="em")
            st.form_submit_button("Send", key="sub")

    def interaction() -> None:
        at = AppTest.from_function(app)
        at.run()

        at.text_input[0].set_value("user@example.com")
        at.button[0].click()
        at.run()

    run_widget_interaction_test(
        interaction,
        [
            {"action": "form_instrumentation_notice"},
            {
                "action": "submit",
                "widget": {
                    "id": "sub",
                    "type": "form_submit_button",
                    "label": "Send",
                },
                "extra": {
                    "form_id": "my_form",
                    "form_fields": [
                        {
                            "id": "em",
                            "type": "text_input",
                            "label": "Email",
                            "value": "user@example.com",
                        }
                    ],
                },
            },
        ],
        logger=logging.getLogger("tests.form.submit_values"),
        name="form-test-app",
        session_id="session-f",
        user_id="user-f",
    )


def test_form_one_time_info_warning() -> None:
    """First instrumented widget inside a form logs a single INFO explanation."""

    def app() -> None:
        import streamlit as st

        with st.form("f"):
            st.text_input("A", key="a")
            st.text_input("B", key="b")
            st.form_submit_button("Go", key="go")

    log_stream = io.StringIO()
    logger = logging.getLogger("tests.form.info_warning")
    logger.handlers.clear()
    logger.addHandler(logging.StreamHandler(log_stream))
    logger.setLevel(logging.INFO)

    def interaction() -> None:
        at = AppTest.from_function(app)
        at.run()

        assert log_stream.getvalue().count("form_instrumentation_notice") == 1

        log_stream.truncate(0)
        log_stream.seek(0)

        at.text_input[0].set_value("x")
        at.text_input[1].set_value("y")
        at.button[0].click()
        at.run()

        assert "form_instrumentation_notice" not in log_stream.getvalue()

    with StreamlitPageAnalytics.track(
        name="warn-app",
        session_id="s",
        user_id="u",
        logger=logger,
    ):
        interaction()
