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

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from .widget import Widget


@dataclass
class ExtractedWidget:
    """Extracted widget information from a Streamlit widget creation call."""

    widget: Widget
    unextracted_args: List[Any]
    unextracted_kwargs: Dict[str, Any]
    original_action_callback_fn: Optional[Callable] = None
