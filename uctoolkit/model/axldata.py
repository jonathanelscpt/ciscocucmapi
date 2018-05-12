# -*- coding: utf-8 -*-
"""Cisco UC AXL Generic Data Model"""

from collections.abc import MutableMapping

from ..exceptions import AXLAttributeError
from ..helpers import sanitize_model_dict, to_csv, filter_dict_to_target_model


class AXLDataModel(MutableMapping):
    """Model an AXL data object as a native Python object."""

    def __init__(self, axl_data):
        super().__init__()
        # for k, v in axl_data.items():
        #     if isinstance(v, MutableMapping):
        #         axl_data[k] = AXLDataModel(v)
        super().__setattr__('_axl_data', axl_data)

    @property
    def axl_data(self):
        """A copy of the AXL data object's attribute data as an dictionary."""
        return self._axl_data.copy()

    def __str__(self):
        """A human-readable string representation of this object."""
        return f"{self.__class__.__name__}:\n{self._axl_data}"

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        return f"{self.__class__.__name__}({self._axl_data})"

    def __eq__(self, other):
        """AXL objects equality using on uuid"""
        return (isinstance(other, self.__class__)
                and self._axl_data.__eq__(other))

    def __ne__(self, other):
        """AXL objects non-equality using uuid"""
        return not self.__eq__(other)

    def __iter__(self):
        """Iterable of AXL attribute dict"""
        return iter(self._axl_data)

    def __len__(self):
        """Length of AXL attribute dict"""
        return len(self._axl_data)

    def __getitem__(self, key):
        """Get item from AXL attribute dict"""
        try:
            return self._axl_data[key]
        except KeyError:
            raise AXLAttributeError(f"Unknown AXL attribute for API endpoint: {key}")

    def __setitem__(self, key, value):
        """Set item in AXL attribute dict"""
        # if isinstance(value, MutableMapping):
        #     self._axl_data[key] = AXLDataModel(value)
        # else:
        #     self._axl_data[key] = value
        self._axl_data[key] = value

    def __delitem__(self, key):
        """Delete item from AXL attribute dict"""
        try:
            del self._axl_data[key]
        except KeyError:
            raise AXLAttributeError(f"Unknown AXL attribute for API endpoint: {key}")

    def __getattr__(self, key):
        """Get attribute from AXL attribute dict"""
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def sanitize(self):
        """Sanitize data model

        Removes nested references to '_value_1', where python-zeep has interpreted the
        AXL schema's inclusion of uuid attributes.

        :return: sanitized dictionary
        """
        # return sanitize_model_dict(self._axl_data)
        super().__setattr__('_axl_data', sanitize_model_dict(self._axl_data))
        return self

    def filter(self, target_model):
        """Filter model data against a target API model schema

        Useful for assured processing of list/add or get/add transaction paradigms.

        :param target_model: empty API model called from API's model() method
        :return: filtered dictionary
        """
        # return filter_dict_to_target_model(self._axl_data, target_model)
        super().__setattr__('_axl_data', filter_dict_to_target_model(self._axl_data, target_model))
        return self


class ThinAXLDataModel(AXLDataModel):
    """Cisco CUCM Thin AXL data model."""

    @property
    def sql_response(self):
        """Friendly name for sql response"""
        return self.axl_data

    def csv(self, destination_path):
        """Write to csv in familiar table format"""
        # todo - test for single and duplicate base cases
        to_csv(self._axl_data, destination_path)
