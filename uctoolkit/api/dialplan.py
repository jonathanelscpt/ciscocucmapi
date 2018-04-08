# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .abstract import AbstractAXLDeviceAPI, AbstractAXLAPI
from ..exceptions import AXLMethodDoesNotExist


class RoutePartition(AbstractAXLDeviceAPI):
    """Cisco CUCM RoutePartition API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'route_partition'
    _RETURN_OBJECT_NAME = 'routePartition'
    _IDENTIFIERS = (
        "uuid",
        "name",
    )
    _LIST_API_SEARCH_CRITERIA = (
        "name",
    )
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
    )

    def __init__(self, client, object_factory):
        """Initialize a new RoutePartition object with the provided AXL client.

        :param client: zeep SOAP AXL client for API calls to CUCM's SOAP interface
        :param object_factory: factory function for instantiating data models objects
        :raises TypeError: If parameter types are invalid.
        """
        super(RoutePartition, self).__init__(client, object_factory)

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

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist(
            message="Reset method not available for RoutePartition api endpoint.  "
                    "'restartRoutePartition' and 'applyRoutePartition' methods do exist."
        )


class CallPickupGroup(AbstractAXLAPI):
    """Cisco CUCM Line API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'call_pickup_group'
    _RETURN_OBJECT_NAME = 'callPickupGroup'
    _IDENTIFIERS = (
        "uuid",
        "name",
        (
            "pattern",
            "routePartitionName"
        )
    )
    _LIST_API_SEARCH_CRITERIA = (
        "pattern",
        "description",
        "routePartitionName"
    )
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "pattern",
    )

    def __init__(self, client, object_factory):
        """Initialize a new CallPickupGroup object with the provided AXL client.

        :param client: zeep SOAP AXL client for API calls to CUCM's SOAP interface
        :param object_factory: factory function for instantiating data models objects
        :raises TypeError: If parameter types are invalid.
        """
        super(CallPickupGroup, self).__init__(client, object_factory)

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
