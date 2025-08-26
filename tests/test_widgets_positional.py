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

"""Tests for Streamlit widgets using positional arguments.

This module contains tests for all Streamlit widgets defined in config.py,
using the official Streamlit testing framework. Each test verifies both widget
functionality and logging behavior.
"""

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


def test_radio_with_positional_args() -> None:
    """Test radio widget with positional arguments for non-extracted parameters."""

    def widget_interaction() -> None:
        # Define a simple app that creates a radio button using positional args
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            # Use positional arguments for options and
            # index (parameters that aren't extracted)
            # while keeping key as keyword since the wrapper needs to extract it
            options = ["Option A", "Option B", "Option C"]
            st.radio(
                "Test Radio Positional",
                options,  # positional argument for 'options'
                1,  # positional argument for 'index' (default selection)
                key="test_radio_pos",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the radio widget
        radio = at.radio[0]

        # Verify radio exists with expected label and options
        # pylint: disable=no-member
        assert radio.label == "Test Radio Positional"
        assert radio.options == ["Option A", "Option B", "Option C"]
        assert radio.value == "Option B"  # Index 1 = "Option B"

        # Select a different option
        radio.set_value("Option C")

        # Run the app again to update the state
        at.run()

        # Get the radio widget again
        radio = at.radio[0]

        # Verify radio state after selection
        assert radio.value == "Option C"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_radio_pos",
                "type": "radio",
                "label": "Test Radio Positional",
                "values": {"current": "Option C"},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_slider_with_positional_args() -> None:
    """Test slider widget with positional arguments for non-extracted parameters."""

    def widget_interaction() -> None:
        # Define a simple app that creates a slider using positional args
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            # Use positional arguments for min_value, max_value, value, step
            # while keeping key as keyword since the wrapper needs to extract it
            st.slider(
                "Test Slider Positional",
                0,  # positional argument for 'min_value'
                100,  # positional argument for 'max_value'
                25,  # positional argument for 'value' (initial value)
                5,  # positional argument for 'step'
                key="test_slider_pos",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the slider widget
        slider = at.slider[0]

        # Verify slider exists with expected label and initial value
        # pylint: disable=no-member
        assert slider.label == "Test Slider Positional"
        assert slider.value == 25  # Initial value set to 25

        # Change slider value
        slider.set_value(75)

        # Run the app again to update the state
        at.run()

        # Get the slider widget again
        slider = at.slider[0]

        # Verify slider state after change
        assert slider.value == 75

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_slider_pos",
                "type": "slider",
                "label": "Test Slider Positional",
                "values": {"current": 75},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)
