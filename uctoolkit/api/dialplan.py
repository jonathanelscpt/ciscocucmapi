# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .abstract import AbstractAXLDeviceAPI, AbstractAXLAPI
from ..exceptions import AXLMethodDoesNotExist


class AarGroup(AbstractAXLAPI):

    _OBJECT_TYPE = 'aar_group'
    _RETURN_OBJECT_NAME = 'aarGroup'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
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


class CallPickupGroup(AbstractAXLAPI):

    _OBJECT_TYPE = 'call_pickup_group'
    _RETURN_OBJECT_NAME = 'callPickupGroup'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "pattern",
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


class CallPark(AbstractAXLAPI):

    _OBJECT_TYPE = 'call_park'
    _RETURN_OBJECT_NAME = 'callPark'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "callManagerName",
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


class CalledPartyTransformationPattern(AbstractAXLAPI):

    _OBJECT_TYPE = 'called_party_xform_pattern'
    _RETURN_OBJECT_NAME = 'calledPartyTransformationPattern'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
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


class CallingPartyTransformationPattern(AbstractAXLAPI):

    _OBJECT_TYPE = 'calling_party_xform_pattern'
    _RETURN_OBJECT_NAME = 'callingPartyTransformationPattern'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
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


class CmcInfo(AbstractAXLAPI):

    _OBJECT_TYPE = 'cmc'
    _RETURN_OBJECT_NAME = 'cmcInfo'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "code",
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


class Css(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'css'
    _RETURN_OBJECT_NAME = 'css'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name"
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

    def reset(self, **kwargs):
        # todo - refactor and improve abstract class design
        raise AXLMethodDoesNotExist(
            message="Reset method not available for RoutePartition api endpoint.  "
                    "'restartRoutePartition' and 'applyRoutePartition' methods do exist."
        )


class DirectedCallPark(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'directed_call_park'
    _RETURN_OBJECT_NAME = 'directedCallPark'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "retrievalPrefix"
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


class RoutePartition(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'route_partition'
    _RETURN_OBJECT_NAME = 'routePartition'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
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

    def reset(self, **kwargs):
        # todo - refactor and improve abstract class design
        raise AXLMethodDoesNotExist(
            message="Reset method not available for RoutePartition api endpoint.  "
                    "'restartRoutePartition' and 'applyRoutePartition' methods do exist."
        )


