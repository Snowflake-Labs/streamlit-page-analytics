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

from enum import Enum


class UserEventAction(Enum):
    """Represents the type of action that happened on the UI.

    This enum defines the various types of user interactions that can be
    tracked within a Streamlit application.

    Attributes:
        CLICK: User clicked on an element (e.g., button, link).
        CHANGE: User changed a value (e.g., slider, input field).
        SUBMIT: User submitted a form or triggered a submission action.
        OTHER: Any other type of action not covered by the above categories.
    """

    START_TRACKING = "start_tracking"
    CLICK = "click"
    CHANGE = "change"
    SUBMIT = "submit"  # noqa: F841  # vulture: ignore - used in form submissions
    OTHER = "other"
