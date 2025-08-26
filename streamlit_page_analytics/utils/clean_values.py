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

from typing import Any, Dict


def _check_if_empty_or_none(value: Any) -> bool:
    """Check if a value is empty or None."""
    return (
        value is None
        or value == ""
        or value == "[]"
        or value == "{}"
        or value == []
        or value == {}
        or value == ()
    )


def clean_values(d: Dict[str, Any] | Any) -> Dict[str, Any] | Any:
    """Clean dictionary values by removing empty or None values.

    Args:
        d: Input dictionary or any other value

    Returns:
        If input is a dictionary: A new dictionary with empty/None values removed
        If input is a list: A new list with empty/None values removed from its elements
        Otherwise: The input value unchanged
    """
    match d:
        case dict():
            return {
                k: clean_values(v)
                for k, v in d.items()
                if not _check_if_empty_or_none(v)
            }
        case list():
            return [clean_values(v) for v in d]
        case _:
            return d
