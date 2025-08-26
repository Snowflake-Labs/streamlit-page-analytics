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

"""Tests for Streamlit widget wrappers using Streamlit's testing framework.

This module contains tests for all Streamlit widgets defined in config.py,
using the official Streamlit testing framework. Each test verifies both widget
functionality and logging behavior.
"""

import datetime

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


# pylint: disable=no-member
def test_button() -> None:
    """Test button widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a button
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.button(
                "Test Button",
                key="test_btn",
                on_click=lambda: (st.success("mypy safe success"), None)[1],
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the button widget
        button = at.button[0]

        # Verify button exists with expected label
        assert button.label == "Test Button"
        assert not button.value  # Default is False

        # Click the button
        button.click()

        # Run the app again to update the state
        at.run()

        # Verify that the developer_provided on_click worked
        assert at.success[0].value == "mypy safe success"

        # Get the button widget again
        button = at.button[0]

        # Verify button state after clicking
        assert button.value  # Button should be True after clicking

    # Expected log elements to verify
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

    run_widget_interaction_test(widget_interaction, expected_log)


def test_button_without_developer_provided_on_click_and_key() -> None:
    """Test button interaction without a developer provided on_click and key."""

    def widget_interaction() -> None:
        # pylint
        # Define a simple app that creates a button
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.button("Test Button Without Key")

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the button widget
        button = at.button[0]

        # Verify button exists with the expected label
        assert button.label == "Test Button Without Key"
        assert not button.value  # Default is False

        # Click the button
        button.click()

        # Run the app again to update the state
        at.run()

        # Get the button widget again
        button = at.button[0]

        # Verify the button state after clicking
        assert button.value  # Button should be True after clicking

    # Expected log elements to verify
    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "pg-trk-15113830",
                "type": "button",
                "label": "Test Button Without Key",
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_checkbox() -> None:
    """Test checkbox widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a checkbox
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.checkbox("Test Checkbox", key="test_cb")

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the checkbox widget
        checkbox = at.checkbox[0]

        # Verify checkbox exists with expected label
        assert checkbox.label == "Test Checkbox"
        assert not checkbox.value  # Default is False

        # Check the checkbox
        checkbox.check()

        # Run the app again to update the state
        at.run()

        # Get the checkbox widget again
        checkbox = at.checkbox[0]

        # Verify checkbox state after checking
        assert checkbox.value  # Checkbox should be True after checking

    # Expected log elements to verify
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

    run_widget_interaction_test(widget_interaction, expected_log)


def test_radio() -> None:
    """Test radio widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a radio button
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Option 1", "Option 2", "Option 3"]
            st.radio(
                "Test Radio",
                options=options,
                key="test_radio",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the radio widget
        radio = at.radio[0]

        # Verify radio exists with expected label and options
        assert radio.label == "Test Radio"
        assert radio.options == ["Option 1", "Option 2", "Option 3"]
        assert radio.value == "Option 1"  # Default is first option

        # Select different option
        radio.set_value("Option 2")

        # Run the app again to update the state
        at.run()

        # Get the radio widget again
        radio = at.radio[0]

        # Verify radio state after selection
        assert radio.value == "Option 2"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_radio",
                "type": "radio",
                "label": "Test Radio",
                "values": {"current": "Option 2"},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_selectbox() -> None:
    """Test selectbox widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a selectbox
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Choice 1", "Choice 2", "Choice 3"]
            st.selectbox(
                "Test Select",
                options=options,
                key="test_select",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the selectbox widget
        selectbox = at.selectbox[0]

        # Verify selectbox exists with expected label and options
        assert selectbox.label == "Test Select"
        assert selectbox.options == ["Choice 1", "Choice 2", "Choice 3"]
        assert selectbox.value == "Choice 1"  # Default is first option

        # Select different option
        selectbox.set_value("Choice 2")

        # Run the app again to update the state
        at.run()

        # Get the selectbox widget again
        selectbox = at.selectbox[0]

        # Verify selectbox state after selection
        assert selectbox.value == "Choice 2"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_select",
                "type": "selectbox",
                "label": "Test Select",
                "values": {"current": "Choice 2"},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_multiselect() -> None:
    """Test multiselect widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a multiselect
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Item 1", "Item 2", "Item 3"]
            st.multiselect(
                "Test Multi",
                options=options,
                key="test_multi",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the multiselect widget
        multiselect = at.multiselect[0]

        # Verify multiselect exists with expected label and options
        assert multiselect.label == "Test Multi"
        assert multiselect.options == ["Item 1", "Item 2", "Item 3"]
        assert multiselect.value == []  # Default is empty

        # Select multiple options
        multiselect.set_value(["Item 1", "Item 3"])

        # Run the app again to update the state
        at.run()

        # Get the multiselect widget again
        multiselect = at.multiselect[0]

        # Verify multiselect state after selection
        assert multiselect.value == ["Item 1", "Item 3"]

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_multi",
                "type": "multiselect",
                "label": "Test Multi",
                "values": {"current": ["Item 1", "Item 3"]},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_slider() -> None:
    """Test slider widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a slider
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.slider(
                "Test Slider",
                min_value=0,
                max_value=100,
                key="test_slider",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the slider widget
        slider = at.slider[0]

        # Verify slider exists with expected label and initial value
        assert slider.label == "Test Slider"
        assert slider.value == 0  # Default value

        # Change slider value
        slider.set_value(50)

        # Run the app again to update the state
        at.run()

        # Get the slider widget again
        slider = at.slider[0]

        # Verify slider state after change
        assert slider.value == 50

    # Expected log elements to verify
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

    run_widget_interaction_test(widget_interaction, expected_log)


def test_select_slider() -> None:
    """Test select slider widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a select slider
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Low", "Medium", "High"]
            st.select_slider(
                "Test Select Slider",
                options=options,
                key="test_sel_slider",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the select slider widget
        select_slider = at.select_slider[0]

        # Verify select slider exists with expected label and initial value
        assert select_slider.label == "Test Select Slider"
        assert select_slider.value == "Low"  # Default is first option

        # Change select slider value
        select_slider.set_value("High")

        # Run the app again to update the state
        at.run()

        # Get the select slider widget again
        select_slider = at.select_slider[0]

        # Verify select slider state after change
        assert select_slider.value == "High"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sel_slider",
                "type": "select_slider",
                "label": "Test Select Slider",
                "values": {"current": "High"},
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_text_input() -> None:
    """Test text input widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a text input
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.text_input("Test Text Input", key="test_text")

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the text input widget
        text_input = at.text_input[0]

        # Verify text input exists with expected label and initial value
        assert text_input.label == "Test Text Input"
        assert text_input.value == ""  # Default is empty

        # Enter text
        text_input.set_value("Hello World")

        # Run the app again to update the state
        at.run()

        # Get the text input widget again
        text_input = at.text_input[0]

        # Verify text input state after change
        assert text_input.value == "Hello World"

        text_input.set_value("Hello World 2")

        at.run()

        assert text_input.value == "Hello World 2"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_text",
                "type": "text_input",
                "label": "Test Text Input",
                "values": {
                    "current": "Hello World",
                },
            },
        },
        {
            "action": "change",
            "widget": {
                "id": "test_text",
                "type": "text_input",
                "label": "Test Text Input",
                "values": {
                    "current": "Hello World 2",
                },
            },
        },
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_text_input_without_user_provided_key() -> None:
    """Test text input widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a text input
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.text_input("Test Text Input without key")

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the text input widget
        text_input = at.text_input[0]

        # Verify text input exists with expected label and initial value
        assert text_input.label == "Test Text Input without key"
        assert text_input.value == ""  # Default is empty

        # Enter text
        text_input.set_value("Hello World without key")

        # Run the app again to update the state
        at.run()

        # Get the text input widget again
        text_input = at.text_input[0]

        # Verify text input state after change
        assert text_input.value == "Hello World without key"

        text_input.set_value("Hello World without key 2")

        at.run()

        assert text_input.value == "Hello World without key 2"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "pg-trk-1613747494",
                "type": "text_input",
                "label": "Test Text Input without key",
                "values": {
                    "current": "Hello World without key",
                },
            },
        },
        {
            "action": "change",
            "widget": {
                "id": "pg-trk-1613747494",
                "type": "text_input",
                "label": "Test Text Input without key",
                "values": {
                    "current": "Hello World without key 2",
                },
            },
        },
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_number_input() -> None:
    """Test number input widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a number input
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.number_input(
                "Test Number",
                min_value=0,
                max_value=100,
                key="test_num",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the number input widget
        number_input = at.number_input[0]

        # Verify number input exists with expected label and initial value
        assert number_input.label == "Test Number"
        assert number_input.value == 0  # Default value

        # Enter number
        number_input.set_value(42)

        # Run the app again to update the state
        at.run()

        # Get the number input widget again
        number_input = at.number_input[0]

        # Verify number input state after change
        assert number_input.value == 42

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_num",
                "type": "number_input",
                "label": "Test Number",
                "values": {
                    "current": 42,
                },
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_text_area() -> None:
    """Test text area widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a text area
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.text_area(
                "Test Text Area",
                key="test_area",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the text area widget
        text_area = at.text_area[0]

        # Verify text area exists with expected label and initial value
        assert text_area.label == "Test Text Area"
        assert text_area.value == ""  # Default is empty

        # Enter text
        text_area.set_value("Multiple\nlines\nof text")

        # Run the app again to update the state
        at.run()

        # Get the text area widget again
        text_area = at.text_area[0]

        # Verify text area state after change
        assert text_area.value == "Multiple\nlines\nof text"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_area",
                "type": "text_area",
                "label": "Test Text Area",
                "values": {
                    "current": "Multiple\nlines\nof text",
                },
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_date_input() -> None:
    """Test date input widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a date input
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.date_input(
                "Test Date",
                key="test_date",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the date input widget
        date_input = at.date_input[0]

        # Verify date input exists with expected label
        assert date_input.label == "Test Date"

        # Set date
        test_date = datetime.date(2024, 3, 14)
        date_input.set_value(test_date)

        # Run the app again to update the state
        at.run()

        # Get the date input widget again
        date_input = at.date_input[0]

        # Verify date input state after change
        assert date_input.value == datetime.date(2024, 3, 14)

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_date",
                "type": "date_input",
                "label": "Test Date",
                "values": {
                    "current": "2024-03-14",
                },
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_time_input() -> None:
    """Test time input widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a time input
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.time_input(
                "Test Time",
                key="test_time",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the time input widget
        time_input = at.time_input[0]

        # Verify time input exists with expected label
        assert time_input.label == "Test Time"

        # Set time
        test_time = datetime.time(14, 30)
        time_input.set_value(test_time)

        # Run the app again to update the state
        at.run()

        # Get the time input widget again
        time_input = at.time_input[0]

        # Verify time input state after change
        assert time_input.value == datetime.time(14, 30)

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_time",
                "type": "time_input",
                "label": "Test Time",
                "values": {
                    "current": "14:30:00",
                },
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)


def test_color_picker() -> None:
    """Test color picker widget interaction and logging."""

    def widget_interaction() -> None:
        # Define a simple app that creates a color picker
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.color_picker(
                "Test Color",
                key="test_color",
            )

        # Create the app test
        at = AppTest.from_function(app)
        at.run()

        # Get the color picker widget
        color_picker = at.color_picker[0]

        # Verify color picker exists with expected label and initial value
        assert color_picker.label == "Test Color"
        assert color_picker.value == "#000000"  # Default is black

        # Pick color
        color_picker.set_value("#FF0000")  # Red

        # Run the app again to update the state
        at.run()

        # Get the color picker widget again
        color_picker = at.color_picker[0]

        # Verify color picker state after change
        assert color_picker.value == "#FF0000"

    # Expected log elements to verify
    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_color",
                "type": "color_picker",
                "label": "Test Color",
                "values": {
                    "current": "#FF0000",
                },
            },
        }
    ]

    run_widget_interaction_test(widget_interaction, expected_log)
