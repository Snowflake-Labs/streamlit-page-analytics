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
from typing import Any, Callable, Dict, List, Literal

from streamlit import runtime
from streamlit.delta_generator_singletons import get_dg_singleton_instance
from streamlit.elements.lib.form_utils import current_form_id, is_in_form

from ..models import UserEvent, WidgetMapping
from ..utils import clean_values, copy_dict, copy_list
from .form_tracking import (
    log_form_submit_snapshots,
    register_form_field,
    warn_if_first_form_widget_skipped,
)
from .user_event_logger import UserEventLogger
from .widget_attribute_extractor import WidgetAttributeExtractor


class WrappedWidget:  # pylint: disable=too-many-instance-attributes
    """Logger wrapped streamlit widget creation function."""

    _widget_mapping: WidgetMapping
    _original_widget_function: Callable
    _logger: logging.Logger
    _event_logger_fn: Callable[[UserEvent], None]
    _session_state_fn: Callable[[], dict[str, Any]]
    _mask_text_input_values: bool
    _mask_all_values: bool
    _analytics_name: str
    _parent_logger: logging.Logger
    _streamlit_container_name: Literal["st", "st.sidebar"]

    def __init__(
        self,
        *,
        widget_mapping: WidgetMapping,
        widget_fn: Callable,
        event_logger_fn: Callable[[UserEvent], None],
        session_state_fn: Callable[[], dict[str, Any]],
        analytics_name: str,
        parent_logger: logging.Logger,
        streamlit_container_name: Literal["st", "st.sidebar"],
        mask_text_input_values: bool = False,
        mask_all_values: bool = False,
    ) -> None:
        """Initialize the WrappedWidget (all parameters are keyword-only)."""
        self._widget_mapping = widget_mapping
        self._original_widget_function = widget_fn
        self._logger = logging.getLogger(__name__)
        self._event_logger_fn = event_logger_fn
        self._session_state_fn = session_state_fn
        self._mask_text_input_values = mask_text_input_values
        self._mask_all_values = mask_all_values
        self._analytics_name = analytics_name
        self._parent_logger = parent_logger
        self._streamlit_container_name = streamlit_container_name

    def _active_delta_generator(self) -> Any:
        """Root DeltaGenerator for main or sidebar (public singleton API).

        ``form_utils.is_in_form`` / ``current_form_id`` walk ``context_dg_stack``
        from this root the same way as Streamlit's ``st`` / ``st.sidebar`` entrypoints.
        """
        dg = get_dg_singleton_instance()
        if self._streamlit_container_name == "st":
            return dg.main_dg
        return dg.sidebar_dg

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
        is_submit = self._widget_mapping.st_widget_name == "form_submit_button"

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

        in_form = runtime.exists() and is_in_form(self._active_delta_generator())

        if "action" in extraction_attributes:
            if in_form and not is_submit:
                warn_if_first_form_widget_skipped(
                    self._analytics_name, self._event_logger_fn
                )
                fid = current_form_id(self._active_delta_generator())
                register_form_field(
                    self._analytics_name,
                    fid,
                    extracted_widget.widget.id,
                    extracted_widget.widget.type,
                    extracted_widget.widget.label,
                    self._widget_mapping.action_type,
                )
            elif is_submit:
                # Capture while still inside ``with st.form()``; callbacks run
                # outside that context, so ``current_form_id`` would be "" in
                # the handler.
                form_id_for_submit = current_form_id(self._active_delta_generator())

                def _on_submit_wrapper(*cb_args: Any, **cb_kwargs: Any) -> Any:
                    return log_form_submit_snapshots(
                        analytics_name=self._analytics_name,
                        form_id=form_id_for_submit,
                        submit_widget=extracted_widget.widget,
                        log_event=self._event_logger_fn,
                        session_state_fn=self._session_state_fn,
                        mask_text_input_values=self._mask_text_input_values,
                        mask_all_values=self._mask_all_values,
                        user_on_click=extracted_widget.original_action_callback_fn,
                        callback_args=cb_args,
                        callback_kwargs=cb_kwargs,
                    )

                kwargs_to_use[extraction_attributes["action"].name] = _on_submit_wrapper
            else:
                user_event_logger = UserEventLogger(
                    widget=extracted_widget.widget,
                    action_type=self._widget_mapping.action_type,
                    original_element_callback=(
                        extracted_widget.original_action_callback_fn
                    ),
                    logger_fn=self._event_logger_fn,
                    session_state_fn=self._session_state_fn,
                    mask_text_input_values=self._mask_text_input_values,
                    mask_all_values=self._mask_all_values,
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
