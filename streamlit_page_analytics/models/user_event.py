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
from typing import Any, Dict, Optional, Union

from .user_event_action import UserEventAction
from .widget import Widget


@dataclass
class UserEvent:
    """Represents a user action that happened on the UI.

    This is the main event class that captures a complete user interaction,
    including context about the user, page, element, and action performed.

    Attributes:
        session_id: Unique identifier for the user session. Can be None if not set.
        user_id: Details about the user who performed the action. Can be None if
            not available.
        page_name: Name of the page where the event occurred. Can be None if not set.
        action: The type of action performed, either as a string or
            UserEventAction enum. Defaults to UserEventAction.OTHER.
        widget: Details about the UI element that was interacted with. Can be
            None if not available.
        extra: Additional event metadata as key-value pairs. Can be None if no
            extra data.
    """

    session_id: Optional[str] = None
    user_id: Optional[str] = None
    page_name: Optional[str] = None
    action: Union[str, UserEventAction] = UserEventAction.OTHER
    widget: Optional[Widget] = None
    extra: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Validate and normalize the user event after initialization.

        This method is automatically called after the dataclass is initialized.
        It ensures that string action values are converted to UserEventAction enums.

        Raises:
            ValueError: If the action string is not a valid UserEventAction value.
        """
        if isinstance(self.action, str):
            self.action = UserEventAction(self.action)

    def with_session_id(self, session_id: str) -> "UserEvent":
        """Create a new UserEvent instance with the specified session ID.

        Args:
            session_id: The session identifier to set for the new event.

        Returns:
            A new UserEvent instance identical to this one but with the
            specified session_id value.
        """
        new = UserEvent(**self.__dict__)
        new.session_id = session_id
        return new

    def with_user_id(self, user_id: str) -> "UserEvent":
        """Create a new UserEvent instance with the specified user details.

        Args:
            user_id: The UserDetails object containing user information.

        Returns:
            A new UserEvent instance identical to this one but with the
            specified user details.
        """
        new = UserEvent(**self.__dict__)
        new.user_id = user_id
        return new

    def with_page_name(self, page_name: Optional[str]) -> "UserEvent":
        """Create a new UserEvent instance with the specified page name.

        Args:
            page_name: The name of the page where the event occurred.

        Returns:
            A new UserEvent instance identical to this one but with the
            specified page_name value.
        """
        new = UserEvent(**self.__dict__)
        new.page_name = page_name
        return new

    def to_dict(self) -> Dict[str, Any]:
        """Convert the UserEvent instance to a dictionary representation.

        This method creates a dictionary suitable for JSON serialization,
        with proper handling of nested objects and enum values.

        Returns:
            A dictionary containing all event details with keys matching
            the attribute names. Nested objects are converted to dictionaries,
            and enum values are converted to their string representations.
        """
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "page_name": self.page_name,
            "action": (
                self.action.value
                if isinstance(self.action, UserEventAction)
                else self.action
            ),
            "widget": self.widget.to_dict() if self.widget else None,
            "extra": self.extra if self.extra else None,
        }
