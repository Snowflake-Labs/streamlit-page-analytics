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

"""Helpers for tracking widget values inside ``st.form()`` on submit."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

import streamlit as st
from streamlit import runtime

from ..models import UserEvent, UserEventAction, Widget
from ..utils import clean_values

_TEXT_WIDGET_TYPES = frozenset({"text_input", "text_area"})


def _registry_key(analytics_name: str) -> str:
    return f"_streamlit_page_analytics_{analytics_name}_form_registry"


def _warning_key(analytics_name: str) -> str:
    return f"_streamlit_page_analytics_{analytics_name}_form_callback_warning_shown"


_FORM_INSTRUMENTATION_MESSAGE = (
    "Widgets inside st.form() cannot attach on_change/on_click "
    "(Streamlit restriction). Field values are recorded when "
    "st.form_submit_button is pressed. Developer-provided "
    "on_change/on_click on form widgets are not invoked. "
    "See package documentation."
)


def warn_if_first_form_widget_skipped(
    analytics_name: str,
    log_event: Callable[[UserEvent], None],
) -> None:
    """Emit one-time notice when per-widget callbacks are skipped inside a form."""
    if not runtime.exists():
        return
    key = _warning_key(analytics_name)
    if st.session_state.get(key):
        return
    st.session_state[key] = True
    log_event(
        UserEvent(
            action=UserEventAction.FORM_INSTRUMENTATION_NOTICE,
            extra=clean_values({"message": _FORM_INSTRUMENTATION_MESSAGE}),
        )
    )


def register_form_field(  # pylint: disable=too-many-positional-arguments
    analytics_name: str,
    form_id: str,
    widget_key: str,
    widget_type: str,
    label: str,
    action_type: UserEventAction,
) -> None:
    """Remember a tracked widget so its session-state value can be logged on submit."""
    if not form_id or not runtime.exists():
        return
    reg = st.session_state.setdefault(_registry_key(analytics_name), {})
    reg.setdefault(form_id, {})[widget_key] = {
        "type": widget_type,
        "label": label,
        "action_type": action_type.value,
    }


def log_form_submit_snapshots(  # pylint: disable=too-many-locals
    *,
    analytics_name: str,
    form_id: str,
    submit_widget: Widget,
    log_event: Callable[[UserEvent], None],
    session_state_fn: Callable[[], Dict[str, Any]],
    mask_text_input_values: bool,
    mask_all_values: bool,
    user_on_click: Optional[Callable[..., Any]],
    callback_args: Any,
    callback_kwargs: Any,
) -> Any:
    """Log one SUBMIT with field snapshots; clear the form registry for ``form_id``."""
    reg = st.session_state.get(_registry_key(analytics_name))
    field_meta: Dict[str, Dict[str, Any]] = {}
    if reg and form_id in reg:
        field_meta = dict(reg[form_id])
        del reg[form_id]

    ss = session_state_fn()
    form_fields: List[Dict[str, Any]] = []
    for wkey, meta in field_meta.items():
        try:
            raw_val = ss[wkey]
        except (KeyError, TypeError):
            raw_val = None
        val: Any = raw_val
        if mask_all_values or (
            mask_text_input_values and meta["type"] in _TEXT_WIDGET_TYPES
        ):
            val = "[REDACTED]"
        form_fields.append(
            {
                "id": wkey,
                "type": meta["type"],
                "label": meta["label"],
                "value": val,
            }
        )

    log_event(
        UserEvent(
            action=UserEventAction.SUBMIT,
            widget=submit_widget,
            extra=clean_values(
                {
                    "form_id": form_id,
                    "form_fields": form_fields,
                    "args": callback_args,
                    "kwargs": callback_kwargs,
                }
            ),
        )
    )

    if user_on_click is not None:
        return user_on_click(*callback_args, **callback_kwargs)
    return None
