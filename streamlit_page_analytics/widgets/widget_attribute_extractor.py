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

from typing import Any, Dict, List, Tuple, Union

from ..models import ExtractedWidget, Widget, WidgetAttribute, WidgetValues
from ..utils import copy_dict, copy_list, get_crc32_hash

_DEFAULT_ELEMENT_ID_PREFIX: str = "pg-trk-"


class WidgetAttributeExtractor:
    """Extract attributes from the widget creation call."""

    _widget_type: str
    _extraction_attributes: Dict[str, WidgetAttribute]
    _arguments: List[Any]
    _kwarguments: Dict[str, Any]

    def __init__(
        self,
        *,
        widget_type: str,
        extraction_attributes: Dict[str, WidgetAttribute],
        arguments: Union[List[Any], Tuple[List, ...]],
        kwarguments: Dict[str, Any],
    ):
        """Initialize the WidgetAttributeExtractor."""
        self._widget_type = widget_type
        self._extraction_attributes = extraction_attributes
        self._arguments = copy_list(arguments)
        self._kwarguments = copy_dict(kwarguments)

    def extract_widget(self, extra: Dict) -> ExtractedWidget:
        """Extract a widget from actual call arguments."""
        remaining_args, remaining_kwargs, extracted_attributes = (
            self._extract_all_attributes()
        )

        widget_id = extracted_attributes[
            "key"
        ] or "" + _DEFAULT_ELEMENT_ID_PREFIX + get_crc32_hash(
            extracted_attributes["label"]
        )

        widget = Widget(
            # pylint: disable=protected-access
            # this is an inner class of and hence should be allowed
            type=self._widget_type,
            id=widget_id,
            label=extracted_attributes["label"],
            values=WidgetValues(current=extracted_attributes.get("value", None)),
            extra=extra,
        )
        return ExtractedWidget(
            widget=widget,
            original_action_callback_fn=extracted_attributes.get("action", None),
            unextracted_args=remaining_args,
            unextracted_kwargs=remaining_kwargs,
        )

    def _extract_all_attributes(
        self,
    ) -> Tuple[List[Any], Dict[str, Any], Dict[str, Any]]:
        """Extract all attributes from function arguments."""
        return (
            self._arguments,
            self._kwarguments,
            {
                attr_name: self.check_and_get_attribute(attr_name)
                for attr_name in self._extraction_attributes.keys()
            },
        )

    def check_and_get_attribute(self, attribute_name: str) -> Any:
        """Extract an attribute value from function arguments.

        This method extracts specific attribute values from either
        positional or keyword arguments based on the ElementAttribute
        configuration. It also removes the extracted values from the
        argument lists to prevent duplication.

        Args:
            attribute_name: the name of the ElementAttribute to extract.

        Returns:
            The extracted attribute value, or the result of default_value_factory
            if the attribute is not found.

        Note:
            This method modifies the arguments and kwarguments lists by removing
            extracted values to prevent them from being passed to the original
            function.
        """
        attribute = self._extraction_attributes[attribute_name]

        if attribute.name in self._kwarguments:
            ret_value = self._kwarguments[attribute.name]
            del self._kwarguments[attribute.name]
            return ret_value

        if (
            self._arguments
            and attribute.index is not None
            and len(self._arguments) > attribute.index
            and self._arguments[attribute.index] is not None
        ):
            ret_value = self._arguments[attribute.index]
            del self._arguments[attribute.index]
            return ret_value

        return None
