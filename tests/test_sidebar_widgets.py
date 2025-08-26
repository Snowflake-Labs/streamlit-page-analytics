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

import datetime

from streamlit.testing.v1 import AppTest
from testing_framework import run_widget_interaction_test


def test_sidebar_button() -> None:
    """Test sidebar button widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.button(
                "Test Sidebar Button",
                key="test_sidebar_btn",
                on_click=lambda: (st.success("mypy safe success"), None)[1],
            )

        at = AppTest.from_function(app)
        at.run()
        button = at.sidebar.button[0]
        assert button.label == "Test Sidebar Button"
        assert not button.value
        button.click()
        at.run()

        # assert at.success[0].value == "mypy safe success"

    expected_log = [
        {
            "action": "click",
            "widget": {
                "id": "test_sidebar_btn",
                "type": "button",
                "label": "Test Sidebar Button",
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_checkbox() -> None:
    """Test sidebar checkbox widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.checkbox("Test Sidebar Checkbox", key="test_sidebar_cb")

        at = AppTest.from_function(app)
        at.run()
        checkbox = at.sidebar.checkbox[0]
        assert checkbox.label == "Test Sidebar Checkbox"
        assert not checkbox.value
        checkbox.check()
        at.run()
        checkbox = at.sidebar.checkbox[0]
        assert checkbox.value

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_cb",
                "type": "checkbox",
                "label": "Test Sidebar Checkbox",
                "values": {"current": True},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_radio() -> None:
    """Test sidebar radio widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Option 1", "Option 2", "Option 3"]
            st.sidebar.radio(
                "Test Sidebar Radio",
                options=options,
                key="test_sidebar_radio",
            )

        at = AppTest.from_function(app)
        at.run()
        radio = at.sidebar.radio[0]
        assert radio.label == "Test Sidebar Radio"
        assert radio.options == ["Option 1", "Option 2", "Option 3"]
        assert radio.value == "Option 1"
        radio.set_value("Option 2")
        at.run()
        radio = at.sidebar.radio[0]
        assert radio.value == "Option 2"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_radio",
                "type": "radio",
                "label": "Test Sidebar Radio",
                "values": {"current": "Option 2"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_selectbox() -> None:
    """Test sidebar selectbox widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Choice 1", "Choice 2", "Choice 3"]
            st.sidebar.selectbox(
                "Test Sidebar Select",
                options=options,
                key="test_sidebar_select",
            )

        at = AppTest.from_function(app)
        at.run()
        selectbox = at.sidebar.selectbox[0]
        assert selectbox.label == "Test Sidebar Select"
        assert selectbox.options == ["Choice 1", "Choice 2", "Choice 3"]
        assert selectbox.value == "Choice 1"
        selectbox.set_value("Choice 2")
        at.run()
        selectbox = at.sidebar.selectbox[0]
        assert selectbox.value == "Choice 2"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_select",
                "type": "selectbox",
                "label": "Test Sidebar Select",
                "values": {"current": "Choice 2"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_multiselect() -> None:
    """Test sidebar multiselect widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Item 1", "Item 2", "Item 3"]
            st.sidebar.multiselect(
                "Test Sidebar Multi",
                options=options,
                key="test_sidebar_multi",
            )

        at = AppTest.from_function(app)
        at.run()
        multiselect = at.sidebar.multiselect[0]
        assert multiselect.label == "Test Sidebar Multi"
        assert multiselect.options == ["Item 1", "Item 2", "Item 3"]
        assert multiselect.value == []
        multiselect.set_value(["Item 1", "Item 3"])
        at.run()
        multiselect = at.sidebar.multiselect[0]
        assert multiselect.value == ["Item 1", "Item 3"]

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_multi",
                "type": "multiselect",
                "label": "Test Sidebar Multi",
                "values": {"current": ["Item 1", "Item 3"]},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_slider() -> None:
    """Test sidebar slider widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.slider(
                "Test Sidebar Slider",
                min_value=0,
                max_value=100,
                key="test_sidebar_slider",
            )

        at = AppTest.from_function(app)
        at.run()
        slider = at.sidebar.slider[0]
        assert slider.label == "Test Sidebar Slider"
        assert slider.value == 0
        slider.set_value(50)
        at.run()
        slider = at.sidebar.slider[0]
        assert slider.value == 50

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_slider",
                "type": "slider",
                "label": "Test Sidebar Slider",
                "values": {"current": 50},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_select_slider() -> None:
    """Test sidebar select_slider widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            options = ["Low", "Medium", "High"]
            st.sidebar.select_slider(
                "Test Sidebar Select Slider",
                options=options,
                key="test_sidebar_sel_slider",
            )

        at = AppTest.from_function(app)
        at.run()
        select_slider = at.sidebar.select_slider[0]
        assert select_slider.label == "Test Sidebar Select Slider"
        assert select_slider.value == "Low"
        select_slider.set_value("High")
        at.run()
        select_slider = at.sidebar.select_slider[0]
        assert select_slider.value == "High"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_sel_slider",
                "type": "select_slider",
                "label": "Test Sidebar Select Slider",
                "values": {"current": "High"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_text_input() -> None:
    """Test sidebar text_input widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.text_input("Test Sidebar Text Input", key="test_sidebar_text")

        at = AppTest.from_function(app)
        at.run()
        text_input = at.sidebar.text_input[0]
        assert text_input.label == "Test Sidebar Text Input"
        assert text_input.value == ""
        text_input.set_value("Hello Sidebar")
        at.run()
        text_input = at.sidebar.text_input[0]
        assert text_input.value == "Hello Sidebar"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_text",
                "type": "text_input",
                "label": "Test Sidebar Text Input",
                "values": {"current": "Hello Sidebar"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_number_input() -> None:
    """Test sidebar number_input widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.number_input(
                "Test Sidebar Number",
                min_value=0,
                max_value=100,
                key="test_sidebar_num",
            )

        at = AppTest.from_function(app)
        at.run()
        number_input = at.sidebar.number_input[0]
        assert number_input.label == "Test Sidebar Number"
        assert number_input.value == 0
        number_input.set_value(42)
        at.run()
        number_input = at.sidebar.number_input[0]
        assert number_input.value == 42

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_num",
                "type": "number_input",
                "label": "Test Sidebar Number",
                "values": {"current": 42},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_text_area() -> None:
    """Test sidebar text_area widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.text_area(
                "Test Sidebar Text Area",
                key="test_sidebar_area",
            )

        at = AppTest.from_function(app)
        at.run()
        text_area = at.sidebar.text_area[0]
        assert text_area.label == "Test Sidebar Text Area"
        assert text_area.value == ""
        text_area.set_value("Multiple\nlines\nof sidebar text")
        at.run()
        text_area = at.sidebar.text_area[0]
        assert text_area.value == "Multiple\nlines\nof sidebar text"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_area",
                "type": "text_area",
                "label": "Test Sidebar Text Area",
                "values": {"current": "Multiple\nlines\nof sidebar text"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_date_input() -> None:
    """Test sidebar date_input widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.date_input(
                "Test Sidebar Date",
                key="test_sidebar_date",
            )

        at = AppTest.from_function(app)
        at.run()
        date_input = at.sidebar.date_input[0]
        assert date_input.label == "Test Sidebar Date"
        test_date = datetime.date(2024, 3, 14)
        date_input.set_value(test_date)
        at.run()
        date_input = at.sidebar.date_input[0]
        assert date_input.value == datetime.date(2024, 3, 14)

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_date",
                "type": "date_input",
                "label": "Test Sidebar Date",
                "values": {"current": "2024-03-14"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_time_input() -> None:
    """Test sidebar time_input widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.time_input(
                "Test Sidebar Time",
                key="test_sidebar_time",
            )

        at = AppTest.from_function(app)
        at.run()
        time_input = at.sidebar.time_input[0]
        assert time_input.label == "Test Sidebar Time"
        test_time = datetime.time(14, 30)
        time_input.set_value(test_time)
        at.run()
        time_input = at.sidebar.time_input[0]
        assert time_input.value == datetime.time(14, 30)

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_time",
                "type": "time_input",
                "label": "Test Sidebar Time",
                "values": {"current": "14:30:00"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)


def test_sidebar_color_picker() -> None:
    """Test sidebar color_picker widget interaction and logging."""

    def widget_interaction() -> None:
        def app() -> None:
            # pylint: disable=import-outside-toplevel
            # required for running individual tests
            import streamlit as st

            st.sidebar.color_picker(
                "Test Sidebar Color",
                key="test_sidebar_color",
            )

        at = AppTest.from_function(app)
        at.run()
        color_picker = at.sidebar.color_picker[0]
        assert color_picker.label == "Test Sidebar Color"
        assert color_picker.value == "#000000"
        color_picker.set_value("#FF0000")
        at.run()
        color_picker = at.sidebar.color_picker[0]
        assert color_picker.value == "#FF0000"

    expected_log = [
        {
            "action": "change",
            "widget": {
                "id": "test_sidebar_color",
                "type": "color_picker",
                "label": "Test Sidebar Color",
                "values": {"current": "#FF0000"},
            },
        }
    ]
    run_widget_interaction_test(widget_interaction, expected_log)
