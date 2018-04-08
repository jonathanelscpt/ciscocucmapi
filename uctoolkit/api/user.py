# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .abstract import AbstractAXLAPI


class User(AbstractAXLAPI):
    """Cisco CUCM User API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'user'
    _RETURN_OBJECT_NAME = 'user'
    _IDENTIFIERS = (
        "uuid",
        "userid"
    )
    _LIST_API_SEARCH_CRITERIA = (
        "firstName",
        "lastName",
        "userid",
        "department"
    )
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "userid",
        "lastName"
        "presenceGroupName"
    )

    def __init__(self, client, object_factory):
        """Initialize a new User object with the provided AXL client.

        :param client: zeep SOAP AXL client for API calls to CUCM's SOAP interface
        :param object_factory: factory function for instantiating data models objects
        :raises TypeError: If parameter types are invalid.
        """
        super(User, self).__init__(client, object_factory)

    @classmethod
    def object_type(cls):
        return cls._OBJECT_TYPE

    @classmethod
    def return_object_name(cls):
        return cls._RETURN_OBJECT_NAME

    @classmethod
    def add_api_mandatory_attributes(cls):
        return cls._ADD_API_MANDATORY_ATTRIBUTES

    @classmethod
    def list_api_search_criteria(cls):
        return cls._LIST_API_SEARCH_CRITERIA

    @classmethod
    def identifiers(cls):
        return cls._IDENTIFIERS
