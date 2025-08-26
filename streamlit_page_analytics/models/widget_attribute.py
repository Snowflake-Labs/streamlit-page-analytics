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


@dataclass
class WidgetAttribute:
    """Configuration for extracting attributes from Streamlit element arguments.

    This class defines how to extract specific attributes from Streamlit element
    function calls, either by positional index or keyword argument name.

    Attributes:
        index: The positional argument index where this attribute can be found.
            Can be None if the attribute is only available as a keyword argument.
        name: The keyword argument name where this attribute can be found.
            Can be None if the attribute is only available as a positional argument.
    """

    index: int
    name: str
