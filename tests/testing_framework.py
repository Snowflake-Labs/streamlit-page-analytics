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

import io
import json
import logging
from typing import Any, Callable, Dict, Optional

from streamlit_page_analytics import StreamlitPageAnalytics

_TEST_SESSION_ID = "test-session"
_TEST_USER_ID = "test-user"
_TEST_APP_NAME = "test-app"


def _assert_equals(
    expected: Any, actual: Any, field_name: Optional[str] = None
) -> None:
    """Assert that two values are equal or raise an AssertionError."""
    error_msg = f"""Mismatch {field_name + '|' if field_name else ''}
    Expected: {expected}, Actual: {actual}
    """
    assert expected == actual, error_msg


def _filter_widget_logs(log_lines: list[str]) -> list[dict]:
    """Filter log lines to only include widget interaction logs (not start_tracking)."""
    result = []
    for line in log_lines:
        log_json = json.loads(line)
        if log_json.get("action") != "start_tracking":
            result.append(log_json)
    return result


def _has_widget_or_form_payload(log_json: dict) -> bool:
    """True if the log line has widget data or form snapshot / notice payload."""
    if log_json.get("widget"):
        return True
    if log_json.get("action") == "form_instrumentation_notice":
        return True
    extra = log_json.get("extra")
    if isinstance(extra, dict) and ("form_fields" in extra or "form_id" in extra):
        return True
    return False


def run_widget_interaction_test(  # pylint: disable=too-many-locals
    test_code: Callable[[], None],
    expected_log_lines: list[Dict[str, Any]],
    **analytics_kwargs: Any,
) -> None:
    """Run a test with StreamlitPageAnalytics and verify log output.

    Args:
        test_code: A callable that contains the test code to run
        expected_log_lines: The expected log lines to compare against
        **analytics_kwargs: Additional keyword arguments to pass to
            StreamlitPageAnalytics.track(). Supported options include:
            - mask_all_values: bool - Mask all widget values in logs
            - mask_text_input_values: bool - Mask text input values only
            - logger: logging.Logger - Custom logger (default: creates new one)
            - name: str - App name (default: "test-app")
            - session_id: str - Session ID (default: "test-session")
            - user_id: str - User ID (default: "test-user")
    """
    log_stream = io.StringIO()
    logger = analytics_kwargs.pop("logger", None)
    if logger is None:
        logger = logging.getLogger("test-logger")
    logger.handlers.clear()
    logger.addHandler(logging.StreamHandler(log_stream))
    logger.setLevel(logging.INFO)

    name = analytics_kwargs.pop("name", _TEST_APP_NAME)
    session_id = analytics_kwargs.pop("session_id", _TEST_SESSION_ID)
    user_id = analytics_kwargs.pop("user_id", _TEST_USER_ID)

    with StreamlitPageAnalytics.track(
        name=name,
        session_id=session_id,
        user_id=user_id,
        logger=logger,
        **analytics_kwargs,
    ):
        test_code()

    log_lines = log_stream.getvalue().splitlines()
    widget_logs = _filter_widget_logs(log_lines)

    assert len(widget_logs) == len(
        expected_log_lines
    ), f"Expected {len(expected_log_lines)} log lines, got {len(widget_logs)}"

    for log_json, expected_log_line in zip(widget_logs, expected_log_lines):
        assert _has_widget_or_form_payload(log_json), (
            "Each log line must include a widget or form payload (widget, "
            "form_instrumentation_notice, or extra with form_id/form_fields): "
            f"{log_json!r}"
        )

        _assert_equals(
            expected=session_id,
            actual=log_json["session_id"],
            field_name="session_id",
        )
        _assert_equals(
            expected=user_id,
            actual=log_json["user_id"],
            field_name="user_id",
        )

        if "action" in expected_log_line:
            _assert_equals(
                expected=expected_log_line["action"],
                actual=log_json["action"],
                field_name="action",
            )

        if "widget" in expected_log_line and "widget" in log_json:
            _assert_equals(
                expected=expected_log_line["widget"]["id"],
                actual=log_json["widget"]["id"],
                field_name="widget.id",
            )

            _assert_equals(
                expected=expected_log_line["widget"]["type"],
                actual=log_json["widget"]["type"],
                field_name="widget.type",
            )

            _assert_equals(
                expected=expected_log_line["widget"]["label"],
                actual=log_json["widget"]["label"],
                field_name="label",
            )

        if "extra" in expected_log_line:
            assert "extra" in log_json, "extra not found in log"
            for key, expected_val in expected_log_line["extra"].items():
                _assert_equals(
                    expected=expected_val,
                    actual=log_json["extra"][key],
                    field_name=f"extra.{key}",
                )

        widget = log_json.get("widget")
        if not widget:
            continue

        widget_vals = widget.get("values") or {}
        if "previous" in widget_vals:
            assert False, "previous found in element.values"

        exp_widget = expected_log_line.get("widget") or {}
        if "values" in exp_widget:
            assert "values" in widget, "values not found in element"

            if "previous" in exp_widget["values"]:
                assert (
                    "previous" in widget["values"]
                ), "previous not found in element.values"
                _assert_equals(
                    expected=exp_widget["values"]["previous"],
                    actual=widget["values"]["previous"],
                    field_name="element.values.previous",
                )

            if "current" in exp_widget["values"]:
                assert (
                    "current" in widget["values"]
                ), "current not found in element.values"
                _assert_equals(
                    expected=exp_widget["values"]["current"],
                    actual=widget["values"]["current"],
                    field_name="element.values.current",
                )
