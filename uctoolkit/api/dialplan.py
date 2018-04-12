# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from ..exceptions import AXLMethodDoesNotExist


class AarGroup(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class CallPickupGroup(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "pattern",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class CallPark(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "callManagerName",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class CalledPartyTransformationPattern(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class CallingPartyTransformationPattern(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class CmcInfo(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "code",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class Css(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class DirectedCallPark(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "retrievalPrefix"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class FacInfo(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "code",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class HuntList(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "callManagerGroupName"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            routeListEnabled="true",
            **kwargs):
        default_kwargs = {
            "routeListEnabled": routeListEnabled,
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)


class LineGroup(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class HuntPilot(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "huntListName",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class RoutePartition(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def reset(self, **kwargs):
        # edge case for devices that are restart-able but not reset-able
        # todo - refactor and improve abstract class design
        raise AXLMethodDoesNotExist(
            message="'Reset' method not available for {name} api endpoint.  "
                    "'Restart' and 'apply' methods exist.".format(
                        name=self.__class__.__name__
                    )
        )
