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

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


# pylint: disable=no-member
def test_text_input_masked_when_enabled() -> None:
    """Test that text input values are masked when mask_text_input_values=True."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.text_input("Sensitive Input", key="sensitive_text")

        at = AppTest.from_function(app)
        at.run()

        text_input = at.text_input[0]
        text_input.set_value("my secret password")
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "sensitive_text",
                "type": "text_input",
                "label": "Sensitive Input",
                "values": {"current": "[REDACTED]"},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction, expected_log, mask_text_input_values=True
    )


def test_text_area_masked_when_enabled() -> None:
    """Test that text area values are masked when mask_text_input_values=True."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.text_area("Sensitive Text Area", key="sensitive_area")

        at = AppTest.from_function(app)
        at.run()

        text_area = at.text_area[0]
        text_area.set_value("confidential information\nwith multiple lines")
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "sensitive_area",
                "type": "text_area",
                "label": "Sensitive Text Area",
                "values": {"current": "[REDACTED]"},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction, expected_log, mask_text_input_values=True
    )


def test_text_input_not_masked_when_disabled() -> None:
    """Test text input values are NOT masked when mask_text_input_values=False."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.text_input("Normal Input", key="normal_text")

        at = AppTest.from_function(app)
        at.run()

        text_input = at.text_input[0]
        text_input.set_value("visible text value")
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "normal_text",
                "type": "text_input",
                "label": "Normal Input",
                "values": {"current": "visible text value"},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction, expected_log, mask_text_input_values=False
    )


def test_other_widgets_not_affected_by_masking() -> None:
    """Test that other widgets (selectbox) are not affected by masking."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.selectbox(
                "Choose Option", options=["Option A", "Option B"], key="select"
            )

        at = AppTest.from_function(app)
        at.run()

        selectbox = at.selectbox[0]
        selectbox.set_value("Option B")
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "select",
                "type": "selectbox",
                "label": "Choose Option",
                "values": {"current": "Option B"},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction, expected_log, mask_text_input_values=True
    )
