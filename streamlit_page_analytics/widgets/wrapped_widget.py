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

"""Class that encapsulates a streamlit widget with logging wrapper callbacks."""

import logging
from typing import Any, Callable, Dict, List

from ..models import UserEvent, WidgetMapping
from ..utils import clean_values, copy_dict, copy_list
from .user_event_logger import UserEventLogger
from .widget_attribute_extractor import WidgetAttributeExtractor


class WrappedWidget:
    """Logger wrapped streamlit widget creation function."""

    _widget_mapping: WidgetMapping
    _original_widget_function: Callable
    _logger: logging.Logger
    _event_logger_fn: Callable[[UserEvent], None]
    _session_state_fn: Callable[[], dict[str, Any]]

    def __init__(
        self,
        widget_mapping: WidgetMapping,
        widget_fn: Callable,
        event_logger_fn: Callable[[UserEvent], None],
        session_state_fn: Callable[[], dict[str, Any]],
    ) -> None:
        """Initialize the WrappedWidget."""
        self._widget_mapping = widget_mapping
        self._original_widget_function = widget_fn
        self._logger = logging.getLogger(__name__)
        self._event_logger_fn = event_logger_fn
        self._session_state_fn = session_state_fn

    def wrapped_widget_fn(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        """Wrapper function that adds analytics to widget interactions.

        This function replaces the original Streamlit function for creating a
        widget. It extracts analytics information from the function arguments,
        creates appropriate UserEvent objects, and wraps any user callbacks to log
        events when triggered.

        Args:
            *args: Positional arguments passed to the original function.
            **kwargs: Keyword arguments passed to the original function.

        Returns:
            The return value from the original Streamlit function.
        """
        extraction_attributes = self._widget_mapping.extraction_attributes

        extractor = WidgetAttributeExtractor(
            widget_type=self._widget_mapping.st_widget_name,
            extraction_attributes=extraction_attributes,
            arguments=args,
            kwarguments=kwargs,
        )
        extracted_widget = extractor.extract_widget(
            extra={
                "args": clean_values(copy_list(args)),
                "kwargs": clean_values(copy_dict(kwargs)),
            }
        )

        args_to_use = [
            extracted_widget.widget.label
        ] + extracted_widget.unextracted_args
        kwargs_to_use = dict(extracted_widget.unextracted_kwargs)

        # Force the widget to use a fixed key for value extraction
        kwargs_to_use["key"] = extracted_widget.widget.id

        if "action" in extraction_attributes:
            user_event_logger = UserEventLogger(
                widget=extracted_widget.widget,
                action_type=self._widget_mapping.action_type,
                original_element_callback=extracted_widget.original_action_callback_fn,
                logger_fn=self._event_logger_fn,
                session_state_fn=self._session_state_fn,
            )
            kwargs_to_use[extraction_attributes["action"].name] = (
                user_event_logger.logging_callback_fn
            )

        self._logger.debug(
            "Created wrapped element: %s (id:%s)",
            extracted_widget.widget.type,
            extracted_widget.widget.id,
        )

        return self._original_widget_function(
            *tuple(args_to_use),
            **kwargs_to_use,
        )
