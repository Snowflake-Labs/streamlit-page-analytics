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

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

from .widget_values import WidgetValues


@dataclass
class Widget:
    """Represents a UI element that was interacted with.

    This class captures detailed information about the specific UI element
    that the user interacted with, such as buttons, sliders, or input fields.

    Attributes:
        id: Unique identifier for the element. Defaults to "unknown".
        type: Type of the UI element (e.g., "button", "slider").
            Defaults to "unknown".
        label: Visible label or text of the element. Defaults to "unknown".
        extra: Additional element metadata as key-value pairs. Can be None if
            no extra data.
    """

    id: str = "unknown"
    type: str = "unknown"
    label: str = "unknown"
    # pylint: disable=unnecessary-lambda
    # required for empty initialisation
    values: WidgetValues = field(default_factory=lambda: WidgetValues())
    extra: Optional[Dict[str, Any]] = None

    def update_value(self, new_value: Any) -> None:
        """Update the values.current value and values.previous of the widget."""
        self.values.previous = self.values.current
        self.values.current = new_value

    def to_dict(self) -> Dict[str, Any]:
        """Convert the UserEventElement instance to a dictionary representation.

        Returns:
            A dictionary containing all element details with keys matching
            the attribute names and values as their corresponding values.
        """
        return asdict(self)
