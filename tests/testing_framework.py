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


def run_widget_interaction_test(
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
        logger.addHandler(logging.StreamHandler(log_stream))

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

    assert len(widget_logs) == len(expected_log_lines), (
        f"Expected {len(expected_log_lines)} log lines, got {len(widget_logs)}"
    )

    for log_json, expected_log_line in zip(widget_logs, expected_log_lines):
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

        if "previous" in log_json["widget"]["values"]:
            assert False, "previous found in element.values"

        if "values" in expected_log_line["widget"]:
            assert "values" in log_json["widget"], "values not found in element"

            if "previous" in expected_log_line["widget"]["values"]:
                assert (
                    "previous" in log_json["widget"]["values"]
                ), "previous not found in element.values"
                _assert_equals(
                    expected=expected_log_line["widget"]["values"]["previous"],
                    actual=log_json["widget"]["values"]["previous"],
                    field_name="element.values.previous",
                )

            if "current" in expected_log_line["widget"]["values"]:
                assert (
                    "current" in log_json["widget"]["values"]
                ), "current not found in element.values"
                _assert_equals(
                    expected=expected_log_line["widget"]["values"]["current"],
                    actual=log_json["widget"]["values"]["current"],
                    field_name="element.values.current",
                )
