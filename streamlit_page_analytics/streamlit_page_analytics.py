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

"""A Streamlit component for page analytics.

This module provides the main StreamlitPageAnalytics class for tracking user
interactions with Streamlit applications. It wraps Streamlit elements to
automatically capture analytics events when users interact with them.
"""

import json
import logging
from typing import Any, Callable, Dict, Optional

import streamlit as st

from .config import MAPPINGS
from .models import UserEvent, WidgetMappingKey
from .utils import clean_values
from .widgets import WrappedWidget


class StreamlitPageAnalytics:
    """Main class for tracking analytics in Streamlit applications.

    This class provides functionality to automatically track user interactions
    with Streamlit UI elements. It wraps Streamlit functions to capture events
    when users click buttons, change values, or perform other actions.

    The class can be used as a context manager or by manually starting and
    stopping tracking. All captured events are logged using Python's logging
    framework with configurable log levels.

    Attributes:
        _logger: Internal logger instance for outputting captured events.
        _original_mappings: Storage for original Streamlit functions to restore later.
        _name: Name identifier for the analytics logger.
        _session_id: Unique identifier for the current user session.
        _user_id: Unique identifier for the current user.
        _log_level: Logging level for captured events.

    Example:
        Basic usage as a context manager:

        >>> with StreamlitPageAnalytics.track(
        ...     name="my_app",
        ...     session_id="session_123",
        ...     user_id="user_456"
        ... ):
        ...     st.button("Click me")  # This will be automatically tracked

        Manual usage:

        >>> analytics = StreamlitPageAnalytics(
        ...     name="my_app",
        ...     session_id="session_123",
        ...     user_id="user_456"
        ... )
        >>> analytics.start_tracking()
        >>> st.button("Click me")  # This will be tracked
        >>> analytics.stop_tracking()
    """

    _logger: logging.Logger
    _original_mappings: Dict[WidgetMappingKey, Callable]
    _name: str
    _session_id: str
    _user_id: str
    _log_level: int
    _mask_text_input_values: bool

    def __init__(
        self,
        name: str,
        session_id: str = "unknown",
        user_id: str = "unknown",
        *,  # Force keyword arguments
        log_level: int = logging.INFO,
        logger: Optional[logging.Logger] = None,
        mask_text_input_values: bool = False,
    ) -> None:
        """Initialize the StreamlitPageAnalytics instance.

        Args:
            name: Name identifier for the analytics logger. This will be used
                as the logger name in the Python logging framework.
            session_id: Unique identifier for the current user session.
                This should remain constant for a single user session.
            user_id: Unique identifier for the current user.
            log_level: Logging level for captured events. Defaults to logging.INFO.
                Can be any valid logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            logger: An optional logger for debugging wrapper operations.
                If not provided, a new logger will be created.
            mask_text_input_values: If True, text input and text area values will be
                replaced with "[REDACTED]" in the logs. Defaults to False.
        """
        self._original_mappings = {}
        self._session_id = session_id
        self._user_id = user_id
        self._log_level = log_level
        self._logger = logger if logger else logging.getLogger(name)
        self._logger.setLevel(log_level)
        self._mask_text_input_values = mask_text_input_values

    def __enter__(self) -> "StreamlitPageAnalytics":
        """Enter the context manager and start tracking.

        This method is called when entering a 'with' statement.
        It automatically starts tracking user interactions.

        Returns:
            The StreamlitPageAnalytics instance for use within the context.
        """
        self.start_tracking()
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        """Exit the context manager and stop tracking.

        This method is called when exiting a 'with' statement.
        It automatically stops tracking and restores original Streamlit functions.
        """
        self.stop_tracking()

    @staticmethod
    def track(
        name: str,
        session_id: str,
        user_id: str,
        *,  # Force keyword arguments
        log_level: int = logging.INFO,
        logger: Optional[logging.Logger] = None,
        mask_text_input_values: bool = False,
    ) -> "StreamlitPageAnalytics":
        """Create a new StreamlitPageAnalytics instance for use as a context manager.

        This is a convenience static method for creating instances that are
        intended to be used as context managers.

        Args:
            name: Name identifier for the analytics logger.
            session_id: Unique identifier for the current user session.
            user_id: Unique identifier for the current user.
            log_level: Logging level for captured events. Defaults to logging.INFO.
            logger: An optional logger for debugging wrapper operations.
                If not provided, a new logger will be created.
            mask_text_input_values: If True, text input and text area values will be
                replaced with "[REDACTED]" in the logs. Defaults to False.

        Returns:
            A new StreamlitPageAnalytics instance configured with the provided
            parameters.

        Example:
            >>> with StreamlitPageAnalytics.track(
            ...     "my_app",
            ...     "session_123",
            ...     "user_456"
            ... ):
            ...     st.button("Tracked button")  # This will be tracked
        """
        return StreamlitPageAnalytics(
            name=name,
            session_id=session_id,
            user_id=user_id,
            log_level=log_level,
            logger=logger,
            mask_text_input_values=mask_text_input_values,
        )

    def log_event(self, partial_event: UserEvent) -> None:
        """Log a user event or message.

        This method handles logging of user events by enriching them with
        session and user information, then outputting them via the logger.

        Args:
            partial_event: The event to log, will be enriched with session_id and
                           user details
        """
        if not isinstance(partial_event, UserEvent):
            raise TypeError(f"Expected UserEvent, got: {type(partial_event)}")

        cleaned_event = partial_event.with_session_id(self._session_id).with_user_id(
            self._user_id
        )

        self._logger.log(
            self._log_level,
            json.dumps(
                clean_values(cleaned_event.to_dict()),
                default=str,
                skipkeys=True,
            ),
        )

    def start_tracking(self) -> None:
        """Start tracking user interactions with Streamlit elements.

        This method wraps all configured Streamlit functions with analytics
        tracking functionality. After calling this method, interactions with
        supported Streamlit elements will automatically generate log events.

        Note:
            This method should be called before creating any Streamlit elements
            that you want to track.
        """
        self._wrap_st_functions()

    def stop_tracking(self) -> None:
        """Stop tracking user interactions and restore original Streamlit functions.

        This method unwraps all previously wrapped Streamlit functions,
        restoring them to their original state. After calling this method,
        interactions with Streamlit elements will no longer generate log events.

        Note:
            It's important to call this method to clean up and avoid interference
            with other parts of the application that may use Streamlit functions.
        """
        self.unwrap_st_functions()

    def set_user_id(self, user_id: str) -> None:
        """Set the user ID for the current session."""
        self._user_id = user_id

    def set_session_id(self, session_id: str) -> None:
        """Set the session ID for the current session."""
        self._session_id = session_id

    def _wrap_st_functions(self) -> None:
        """Wrap Streamlit functions with analytics tracking functionality.

        This method iterates through all configured element mappings and
        replaces the original Streamlit functions with wrapped versions
        that capture analytics events. The original functions are stored
        for later restoration.

        The wrapping process:
        1. Gets the original Streamlit function
        2. Creates a wrapped version of the function that captures events
        3. Stores the original function for later restoration
        4. Replaces the Streamlit function with the wrapped version
        """
        for mapping in MAPPINGS:
            for container, container_name in [
                (st, "st"),
                (st.sidebar, "st.sidebar"),
            ]:
                if not hasattr(container, mapping.st_widget_name):
                    continue

                original_element_fn = getattr(container, mapping.st_widget_name)

                if (
                    original_element_fn.__module__
                    == "streamlit_page_analytics.widgets.wrapped_widget"
                ):
                    # don't rewrap
                    continue

                wrapped_widget = WrappedWidget(
                    widget_mapping=mapping,
                    widget_fn=original_element_fn,
                    event_logger_fn=self.log_event,
                    # pylint: disable=unnecessary-lambda
                    session_state_fn=lambda: st.session_state.to_dict(),
                    mask_text_input_values=self._mask_text_input_values,
                )

                self._logger.debug(
                    "Wrapped %s.%s", container_name, mapping.st_widget_name
                )

                mapping_key = WidgetMappingKey(container_name, mapping.st_widget_name)
                self._original_mappings[mapping_key] = original_element_fn

                setattr(
                    container, mapping.st_widget_name, wrapped_widget.wrapped_widget_fn
                )

    def unwrap_st_functions(self) -> None:
        """Restore original Streamlit functions, removing analytics tracking.

        This method iterates through all previously wrapped Streamlit functions
        and restores them to their original state. This effectively disables
        analytics tracking for those elements.

        The unwrapping process:
        1. Iterates through stored original functions
        2. Restores each original function to the original Streamlit module function
        3. Clears the stored mappings
        """
        for (
            widget_mapping_key,
            original_st_widget_function,
        ) in self._original_mappings.items():

            if widget_mapping_key.container_name == "st":
                setattr(st, widget_mapping_key.widget_name, original_st_widget_function)
            elif widget_mapping_key.container_name == "st.sidebar":
                setattr(
                    st.sidebar,
                    widget_mapping_key.widget_name,
                    original_st_widget_function,
                )

        self._original_mappings.clear()
