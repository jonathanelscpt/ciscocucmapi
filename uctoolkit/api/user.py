# -*- coding: utf-8 -*-
"""CUCM AXL User APIs."""

from .abstract import AbstractAXLAPI


class User(AbstractAXLAPI):
    """Cisco CUCM User API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'user'
    _RETURN_OBJECT_NAME = 'user'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "userid",
        "lastName"
        "presenceGroupName"
    )

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES
