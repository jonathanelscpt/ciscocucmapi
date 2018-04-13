# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args
from ..exceptions import AXLMethodDoesNotExist


class AarGroup(AbstractAXLAPI):
    _factory_descriptor = "aar_group"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class CallPickupGroup(AbstractAXLAPI):
    _factory_descriptor = "call_pickup_group"

    def add(self, name, pattern, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class CallPark(AbstractAXLAPI):
    _factory_descriptor = "call_park"

    def add(self, pattern, callManagerName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class CalledPartyTransformationPattern(AbstractAXLAPI):
    _factory_descriptor = "called_party_xform_pattern"

    def add(self, pattern, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class CallingPartyTransformationPattern(AbstractAXLAPI):
    _factory_descriptor = "calling_party_xform_pattern"

    def add(self, pattern, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class CmcInfo(AbstractAXLAPI):
    _factory_descriptor = "cmc"

    def add(self, code, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class Css(AbstractAXLAPI):
    _factory_descriptor = "css"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class DirectedCallPark(AbstractAXLDeviceAPI):
    _factory_descriptor = "directed_call_park"

    def add(self, pattern, retrievalPrefix, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class FacInfo(AbstractAXLAPI):
    _factory_descriptor = "fac"

    def add(self, name, code, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class HuntList(AbstractAXLDeviceAPI):
    _factory_descriptor = "hunt_list"

    def add(self, name, callManagerGroupName, routeListEnabled="true", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class HuntPilot(AbstractAXLAPI):
    _factory_descriptor = "hunt_pilot"

    def add(self, pattern, huntListName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class LineGroup(AbstractAXLAPI):
    _factory_descriptor = "line_group"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class LocalRouteGroup(AbstractAXLAPI):
    _factory_descriptor = "local_route_group"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class RoutePartition(AbstractAXLDeviceAPI):
    _factory_descriptor = "partition"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

    def reset(self, **kwargs):
        # edge case for devices that are restart-able but not reset-able
        # todo - refactor and improve abstract class design
        raise AXLMethodDoesNotExist(
            message="'Reset' method not available for {name} api endpoint.  "
                    "'Restart' and 'apply' methods exist.".format(
                        name=self.__class__.__name__
                    ))
