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

# Constants for testing
_TEST_SESSION_ID = "test-session"
_TEST_USER_ID = "test-user"
_TEST_APP_NAME = "test-app"


def _assert_equals(
    expected: Any, actual: Any, field_name: Optional[str] = None
) -> None:
    """Assert that two values are equal or raise an AssertionError."""
    error_msg = f"""Mismatch {field_name + '|'  if field_name else ''}
    Expected: {expected}, Actual: {actual}
    """
    assert expected == actual, error_msg


def run_widget_interaction_test(
    test_code: Callable[[], None], expected_log_lines: list[Dict[str, Any]]
) -> None:
    """Run a test with StreamlitPageAnalytics and verify log output.

    Args:
        test_code: A callable that contains the test code to run
        expected_log_lines: The expected log lines to compare against
    """
    log_stream = io.StringIO()
    logger = logging.getLogger("test-logger")
    logger.addHandler(logging.StreamHandler(log_stream))

    with StreamlitPageAnalytics.track(
        name=_TEST_APP_NAME,
        session_id=_TEST_SESSION_ID,
        user_id=_TEST_USER_ID,
        logger=logger,
    ):
        test_code()

    log_lines = log_stream.getvalue().splitlines()
    assert len(log_lines) == len(
        expected_log_lines
    ), f"Expected {len(expected_log_lines)} log lines, got {len(log_lines)}"

    # For each log line, verify that it contains the expected elements
    # rather than requiring an exact match
    for log_line, expected_log_line in zip(log_lines, expected_log_lines):
        log_json = json.loads(log_line)

        # Verify session_id and user_id
        _assert_equals(
            expected=_TEST_SESSION_ID,
            actual=log_json["session_id"],
            field_name="session_id",
        )
        _assert_equals(
            expected=_TEST_USER_ID,
            actual=log_json["user_id"],
            field_name="user_id",
        )

        # Verify action if specified in expected_elements
        if "action" in expected_log_line:
            _assert_equals(
                expected=expected_log_line["action"],
                actual=log_json["action"],
                field_name="action",
            )

        # Verify element_id, element_type, and label if specified in expected_elements
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
