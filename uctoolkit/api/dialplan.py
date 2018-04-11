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

    _OBJECT_TYPE = 'route_partition'
    _RETURN_OBJECT_NAME = 'routePartition'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
    )

    def __init__(self, client, object_factory):
        super(RoutePartition, self).__init__(client, object_factory)

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def reset(self, **kwargs):
        # todo - refactor and improve abstract class design
        raise AXLMethodDoesNotExist(
            message="Reset method not available for RoutePartition api endpoint.  "
                    "'restartRoutePartition' and 'applyRoutePartition' methods do exist."
        )


class CallPickupGroup(AbstractAXLAPI):

    _OBJECT_TYPE = 'call_pickup_group'
    _RETURN_OBJECT_NAME = 'callPickupGroup'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "pattern",
    )

    def __init__(self, client, object_factory):
        super(CallPickupGroup, self).__init__(client, object_factory)

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

