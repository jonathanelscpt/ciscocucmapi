# -*- coding: utf-8 -*-
"""CUCM AXL User APIs."""

from .base import AbstractAXLAPI


class User(AbstractAXLAPI):
    """Cisco CUCM User API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "userid",
        "lastName"
        "presenceGroupName"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES
