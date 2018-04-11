# -*- coding: utf-8 -*-
"""Cisco UC AXL Generic Data Model"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

from builtins import *

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
import json

from ..exceptions import AXLAttributeError
from ..utils import sanitize_data_model_dict


class AXLDataModel(MutableMapping):
    """Model an AXL data object as a native Python object."""

    def __init__(self, axl_data):
        super(AXLDataModel, self).__init__()
        super(AXLDataModel, self).__setattr__('_axl_data', axl_data)

    @property
    def axl_data(self):
        """A copy of the AXL data object's attribute data as an dictionary."""
        return self._axl_data.copy()

    def __str__(self):
        """A human-readable string representation of this object."""
        return "{}:\n{}".format(self.__class__.__name__, self._axl_data)

    def __repr__(self):
        """A string representing this object as valid Python expression."""
        return "{}({})".format(self.__class__.__name__, self._axl_data)

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
        self._axl_data[key] = value

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

    def sanitize(self):
        return sanitize_data_model_dict(self._axl_data)
