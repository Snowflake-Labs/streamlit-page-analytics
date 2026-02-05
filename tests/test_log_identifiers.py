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

"""Tests for verifying session_id and user_id are correctly logged.

This module contains tests that verify the provided session_id and user_id
values are correctly included in all log entries.
"""

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


def test_custom_session_id_in_logs() -> None:
    """Test that a custom session_id is correctly included in logs."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.button("Test Button", key="test_btn")

        at = AppTest.from_function(app)
        at.run()

        button = at.button[0]
        button.click()
        at.run()

    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "test_btn",
                "type": "button",
                "label": "Test Button",
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        session_id="custom-session-abc123",
    )


def test_custom_user_id_in_logs() -> None:
    """Test that a custom user_id is correctly included in logs."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.checkbox("Test Checkbox", key="test_cb")

        at = AppTest.from_function(app)
        at.run()

        checkbox = at.checkbox[0]
        checkbox.check()
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_cb",
                "type": "checkbox",
                "label": "Test Checkbox",
                "values": {"current": True},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        user_id="user-xyz-789",
    )


def test_custom_session_id_and_user_id_in_logs() -> None:
    """Test that both custom session_id and user_id are correctly included."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.slider("Test Slider", min_value=0, max_value=100, key="test_slider")

        at = AppTest.from_function(app)
        at.run()

        slider = at.slider[0]
        slider.set_value(50)
        at.run()

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_slider",
                "type": "slider",
                "label": "Test Slider",
                "values": {"current": 50},
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        session_id="session-unique-456",
        user_id="user-unique-123",
    )


def test_multiple_interactions_have_consistent_ids() -> None:
    """Test that session_id and user_id remain consistent across multiple interactions."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.button("Button 1", key="btn1")
            st.button("Button 2", key="btn2")

        at = AppTest.from_function(app)
        at.run()

        at.button[0].click()
        at.run()

        at.button[1].click()
        at.run()

    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "btn1",
                "type": "button",
                "label": "Button 1",
            },
        },
        {
            "action": "click",
            "widget": {
                "id": "btn2",
                "type": "button",
                "label": "Button 2",
            },
        },
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        session_id="persistent-session",
        user_id="persistent-user",
    )


def test_special_characters_in_session_id() -> None:
    """Test that session_id with special characters is handled correctly."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.button("Test Button", key="test_btn")

        at = AppTest.from_function(app)
        at.run()

        button = at.button[0]
        button.click()
        at.run()

    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "test_btn",
                "type": "button",
                "label": "Test Button",
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        session_id="session_with-special.chars@123",
    )


def test_special_characters_in_user_id() -> None:
    """Test that user_id with special characters is handled correctly."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            import streamlit as st

            st.button("Test Button", key="test_btn")

        at = AppTest.from_function(app)
        at.run()

        button = at.button[0]
        button.click()
        at.run()

    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "test_btn",
                "type": "button",
                "label": "Test Button",
            },
        }
    ]

    run_widget_interaction_test(
        widget_interaction,
        expected_log,
        user_id="user@example.com",
    )
