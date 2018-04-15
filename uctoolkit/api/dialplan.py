# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args
from ..exceptions import AXLMethodDoesNotExist


def _check_port_assignment(members):
    if isinstance(members["member"], list):
        for member in members["member"]:
            if "port" not in member:
                member["port"] = 0
    elif isinstance(members["member"], dict):
        if "port" not in members:
            members["port"] = 0
    return members


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


class RouteGroup(AbstractAXLDeviceAPI):
    _factory_descriptor = "route_group"

    def add(self, name, members, distributionAlgorithm="Circular", **kwargs):
        _check_port_assignment(members)
        return super().add(**flatten_signature_args(self.add, locals()))


class RouteList(AbstractAXLDeviceAPI):
    _factory_descriptor = "route_list"

    def add(self, name, callManagerGroupName, runOnEveryNode="true", routeListEnabled="true", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class RoutePartition(AbstractAXLDeviceAPI):
    _factory_descriptor = "partition"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class RoutePattern(AbstractAXLAPI):
    _factory_descriptor = "route_pattern"

    def add(self, pattern, routePartitionName, destination,
            blockEnable="false", provideOutsideDialtone="true", networkLocation="OffNet",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class SipRoutePattern(AbstractAXLAPI):
    _factory_descriptor = "sip_route_pattern"

    def add(self, pattern, routePartitionName, sipTrunkName,
            usage="Domain Routing",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class TimePeriod(AbstractAXLAPI):
    _factory_descriptor = "time_period"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class TimeSchedule(AbstractAXLAPI):
    _factory_descriptor = "time_schedule"

    def add(self, name, members, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class TodAccess(AbstractAXLAPI):
    _factory_descriptor = "time_schedule"

    def add(self, name, ownerIdName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class TransPattern(AbstractAXLAPI):
    _factory_descriptor = "translation_pattern"

    def add(self, pattern, routePartitionName,
            usage="Translation", provideOutsideDialtone="true", patternUrgency="true",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

    def get(self, dialPlanName=None, routeFilterName=None, returnedTags=None, **kwargs):
        return super().get(**flatten_signature_args(self.get, locals()))

