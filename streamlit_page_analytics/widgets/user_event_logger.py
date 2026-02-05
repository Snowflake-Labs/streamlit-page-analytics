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

import logging
from typing import Any, Callable, Dict, List, Optional

from streamlit_page_analytics.models import UserEvent, UserEventAction, Widget


class UserEventLogger:
    """Class that encapsulates a user event callback with logging wrapper callbacks."""

    _logger: logging.Logger = logging.getLogger(__name__)

    _widget: Widget
    _action_type: UserEventAction
    _original_element_callback: Optional[Callable] = None
    _logger_fn: Optional[Callable[[UserEvent], None]] = None
    _session_state_fn: Optional[Callable[[], dict[str, Any]]] = None
    _mask_text_input_values: bool = False
    _mask_all_values: bool = False

    # Widget types that should have their values masked when masking is enabled
    _TEXT_INPUT_WIDGET_TYPES = frozenset({"text_input", "text_area"})

    def __init__(
        self,
        *,
        widget: Widget,
        action_type: UserEventAction,
        original_element_callback: Optional[Callable] = None,
        logger_fn: Optional[Callable] = None,
        session_state_fn: Optional[Callable[[], dict[str, Any]]] = None,
        mask_text_input_values: bool = False,
        mask_all_values: bool = False,
    ) -> None:
        """Initialize the UserEventLoggerFn."""
        self._widget = widget
        self._action_type = action_type
        self._original_element_callback = original_element_callback
        self._logger_fn = logger_fn
        self._session_state_fn = session_state_fn
        self._mask_text_input_values = mask_text_input_values
        self._mask_all_values = mask_all_values

    def logging_callback_fn(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        """Log user action and calls the original callback if present."""
        self._extract_and_update_widget_value()

        if self._logger_fn is not None:
            self._logger_fn(
                UserEvent(
                    action=self._action_type,
                    widget=self._widget,
                    extra={"args": args, "kwargs": kwargs},
                )
            )

        # Run the developer-provided callback if present
        if self._original_element_callback is not None:
            return self._original_element_callback(*args, **kwargs)

        return None

    def _extract_and_update_widget_value(self) -> None:
        """Extract the value of the widget from the session state."""
        if (
            self._action_type == UserEventAction.CHANGE
            and self._session_state_fn is not None
        ):
            # Extract the widget value from the widget
            try:
                widget_value = self._session_state_fn()[self._widget.id]
                if widget_value is not None:
                    # Mask text input values if enabled
                    if self._mask_all_values or (
                        self._mask_text_input_values
                        and self._widget.type in self._TEXT_INPUT_WIDGET_TYPES
                    ):
                        widget_value = "[REDACTED]"
                    self._widget.update_value(widget_value)

            except (KeyError, TypeError) as err:
                self._logger.warning(
                    "extracting widget value %s\nerror: %s", self._widget, err
                )
