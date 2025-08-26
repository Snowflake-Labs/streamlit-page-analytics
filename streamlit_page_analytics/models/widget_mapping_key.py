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

import zlib
from dataclasses import dataclass


@dataclass
class WidgetMappingKey:
    """Key for storing the original widget function in mapping."""

    container_name: str
    widget_name: str

    def __eq__(self, other: object) -> bool:
        """Check if two keys are equal."""
        if not isinstance(other, WidgetMappingKey):
            return NotImplemented
        return (
            self.container_name == other.container_name
            and self.widget_name == other.widget_name
        )

    def __hash__(self) -> int:
        """Calculate consistent-hash of the key."""
        key: str = str.format("%s.%s", self.container_name, self.widget_name)
        return zlib.crc32(str(key).encode()) & 0xFFFFFFFF
