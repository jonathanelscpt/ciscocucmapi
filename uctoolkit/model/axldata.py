# -*- coding: utf-8 -*-
"""Cisco UC AXL Generic Data Model"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

from builtins import *
from past.builtins import basestring

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
import json

from ..exceptions import AXLAttributeError
from .._internal_utils import to_json_dict


class AXLDataModel(MutableMapping):
    """Model an AXL data object as a native Python object."""

    def __init__(self, axl_data):
        super(AXLDataModel, self).__init__()
        super(AXLDataModel, self).__setattr__('_axl_data', axl_data)

    @property
    def axl_data(self):
        """A copy of the AXL data object's attribute data as an dictionary."""
        return self.axl_data.copy()

    def __str__(self):
        """A human-readable string representation of this object."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._axl_data, indent=2)
        return "{}:\n{}".format(class_str, json_str)

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        class_str = self.__class__.__name__
        json_str = json.dumps(self._axl_data, ensure_ascii=False)
        return "{}({})".format(class_str, json_str)

    def __eq__(self, other):
        """AXL objects equality using on uuid"""
        return (isinstance(other, self.__class__)
                and self._axl_data)

    def __ne__(self, other):
        """AXL objects non-equality using uuid"""
        return not self.__eq__(other)

    def __iter__(self):
        return iter(self._axl_data)

    def __len__(self):
        return len(self._axl_data)

    def __getitem__(self, key):
        try:
            return self._axl_data[key]
        except KeyError:
            raise AXLAttributeError(
                "Unknown AXL attribute for API endpoint: {key}".format(key=key)
            )

    def __setitem__(self, key, value):
        try:
            self._axl_data[key] = value
        except KeyError:
            raise AXLAttributeError(
                "Unknown AXL attribute for API endpoint: {key}".format(key=key)
            )

    def __delitem__(self, key):
        try:
            del self._axl_data[key]
        except KeyError:
            raise AXLAttributeError(
                "Unknown AXL attribute for API endpoint: {key}".format(key=key)
            )

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def to_dict(self):
        """Convert the AXL data to a dictionary."""
        return dict(self._axl_data)

    def to_json(self, **kwargs):
        """Convert the AXL data to JSON for export or transit purposes.
        Any keyword arguments provided are passed through the native
        Python JSON encoder.
        """
        return json.dumps(self._axl_data, **kwargs)


# class AXLDataModel(object):
#     """Model an AXL data object as a native Python object."""
#
#     def __init__(self, axl_data):
#         super(AXLDataModel, self).__init__()
#         # self._axl_data = json_dict(axl_data)
#         self._axl_data = axl_data
#
#     def __getattr__(self, item):
#         """Provide native attribute access to the AXL API object attributes.
#         This method is called when attempting to access a object attribute that
#         hasn't been defined for the object.  For example trying to access
#         object.attribute1 when attribute1 hasn't been defined.
#         __getattr__() checks the original object to see if the attribute exists,
#         and if it does, it returns the attribute's value from the original object.
#         This provides native access to all of the object's attributes.
#
#         :param item: (str) Name of the Attribute being accessed.
#         :return: attribute
#         :raises AttributeError: f the AXL object does not contain the attribute requested.
#         """
#         if item in list(self._axl_data.keys()):
#             item_data = self._axl_data[item]
#             if isinstance(item_data, dict):
#                 return AXLDataModel(item_data)
#             else:
#                 return item_data
#         else:
#             raise AttributeError(
#                 "'{}' object has no attribute '{}'"
#                 "".format(self.__class__.__name__, item)
#             )
#
#     def __str__(self):
#         """A human-readable string representation of this object."""
#         class_str = self.__class__.__name__
#         json_str = json.dumps(self._axl_data, indent=2)
#         return "{}:\n{}".format(class_str, json_str)
#
#     def __repr__(self):
#         """A string representing this object as valid Python expression."""
#         class_str = self.__class__.__name__
#         json_str = json.dumps(self._axl_data, ensure_ascii=False)
#         return "{}({})".format(class_str, json_str)
#
#     def __eq__(self, other):
#         """AXL objects equality using on uuid"""
#         return (isinstance(other, self.__class__)
#                 and self.uuid == other.uuid)
#
#     def __ne__(self, other):
#         """AXL objects non-equality using uuid"""
#         return not self.__eq__(other)
#
#     @property
#     def axl_data(self):
#         """A copy of the AXL data object's attribute data as an dictionary."""
#         return self.axl_data.copy()
#
#     @property
#     def uuid(self):
#         """The AXL object uuid.  Available for all AXL objects"""
#         return self._axl_data.get('uuid')
#
#     def to_dict(self):
#         """Convert the AXL data to a dictionary."""
#         return dict(self._axl_data)
#
#     def to_json(self, **kwargs):
#         """Convert the AXL data to JSON for export or transit purposes.
#         Any keyword arguments provided are passed through the native
#         Python JSON encoder.
#         """
#         return json.dumps(self._axl_data, **kwargs)
