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

"""Mappings from Streamlit elements to analytics events.

This module defines the configuration mappings that specify how different
Streamlit UI elements should be wrapped for analytics tracking. Each mapping
defines which attributes to extract and what type of user action the element represents.
"""

from .models import UserEventAction, WidgetAttribute, WidgetMapping

# Configuration mappings for Streamlit elements to analytics tracking
MAPPINGS = [
    # https://docs.streamlit.io/develop/api-reference/widgets/st.button
    WidgetMapping(
        st_widget_name="button",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=1, name="key"),
            "action": WidgetAttribute(index=3, name="on_click"),
        },
        action_type=UserEventAction.CLICK,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.checkbox
    WidgetMapping(
        st_widget_name="checkbox",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=2, name="key"),
            "action": WidgetAttribute(index=4, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.radio
    WidgetMapping(
        st_widget_name="radio",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
    WidgetMapping(
        st_widget_name="selectbox",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect
    WidgetMapping(
        st_widget_name="multiselect",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.slider
    WidgetMapping(
        st_widget_name="slider",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=6, name="key"),
            "action": WidgetAttribute(index=8, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.select_slider
    WidgetMapping(
        st_widget_name="select_slider",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.text_input
    WidgetMapping(
        st_widget_name="text_input",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=3, name="key"),
            "action": WidgetAttribute(index=7, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.number_input
    WidgetMapping(
        st_widget_name="number_input",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=6, name="key"),
            "action": WidgetAttribute(index=8, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.text_area
    WidgetMapping(
        st_widget_name="text_area",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
    WidgetMapping(
        st_widget_name="date_input",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=4, name="key"),
            "action": WidgetAttribute(index=6, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.time_input
    WidgetMapping(
        st_widget_name="time_input",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=2, name="key"),
            "action": WidgetAttribute(index=4, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
    WidgetMapping(
        st_widget_name="file_uploader",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=3, name="key"),
            "action": WidgetAttribute(index=5, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
    # https://docs.streamlit.io/develop/api-reference/widgets/st.color_picker
    WidgetMapping(
        st_widget_name="color_picker",
        extraction_attributes={
            "label": WidgetAttribute(index=0, name="label"),
            "key": WidgetAttribute(index=2, name="key"),
            "action": WidgetAttribute(index=4, name="on_change"),
        },
        action_type=UserEventAction.CHANGE,
    ),
]
