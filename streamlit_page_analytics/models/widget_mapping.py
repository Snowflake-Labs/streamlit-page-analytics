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

from dataclasses import dataclass
from typing import Dict

from .user_event_action import UserEventAction
from .widget_attribute import WidgetAttribute


@dataclass
class WidgetMapping:
    """Mapping configuration for a specific Streamlit element type.

    This class defines how to extract analytics information from a specific
    type of Streamlit element (e.g., button, checkbox) including which
    attributes to extract and what type of action it represents.

    Attributes:
        st_widget_name: The name of the Streamlit element function
            (e.g., "button", "checkbox").
        extraction_attributes: A dictionary mapping attribute names to their
            ElementAttribute configurations for extraction.
        action_type: The type of user action this element represents
            (e.g., CLICK, CHANGE).
        documentation_url: URL to the official Streamlit documentation for this widget.
    """

    st_widget_name: str
    extraction_attributes: Dict[str, WidgetAttribute]
    action_type: UserEventAction
    documentation_url: str = ""
