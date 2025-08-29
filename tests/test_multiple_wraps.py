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

"""Tests for multiple widget wrappers due to multiple user interactions."""

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


# pylint: disable=no-member,duplicate-code
def test_button_multi_click() -> None:
    """Test button widget interaction and logging with multiple clicks."""
    num_click_iterations = 3

    def widget_interaction_basic_button() -> None:

        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.button(
                "Test Button",
                key="test_btn",
                on_click=lambda: (st.success("mypy safe success"), None)[1],
            )

        at = AppTest.from_function(app)
        at.run()

        # Run the app multiple times to simulate multiple user interactions
        for _ in range(num_click_iterations):
            button = at.button[0]
            button.click()
            at.run()

    run_widget_interaction_test(
        widget_interaction_basic_button,
        [
            {
                "action": "click",
                "widget": {
                    "id": "test_btn",
                    "type": "button",
                    "label": "Test Button",
                },
            }
        ]
        * num_click_iterations,
    )
