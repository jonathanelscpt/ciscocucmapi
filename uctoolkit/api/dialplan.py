# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_kwargs
from ..exceptions import AXLMethodDoesNotExist


def _check_route_group_port_assignment(members):
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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallPickupGroup(AbstractAXLAPI):
    _factory_descriptor = "call_pickup_group"

    def add(self, name, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallPark(AbstractAXLAPI):
    _factory_descriptor = "call_park"

    def add(self, pattern, callManagerName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CalledPartyTransformationPattern(AbstractAXLAPI):
    _factory_descriptor = "called_party_xform_pattern"

    def add(self, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallingPartyTransformationPattern(AbstractAXLAPI):
    _factory_descriptor = "calling_party_xform_pattern"

    def add(self, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CmcInfo(AbstractAXLAPI):
    _factory_descriptor = "cmc"

    def add(self, code, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Css(AbstractAXLAPI):
    _factory_descriptor = "css"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DirectedCallPark(AbstractAXLDeviceAPI):
    _factory_descriptor = "directed_call_park"

    def add(self, pattern, retrievalPrefix, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class FacInfo(AbstractAXLAPI):
    _factory_descriptor = "fac"

    def add(self, name, code, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class HuntList(AbstractAXLDeviceAPI):
    _factory_descriptor = "hunt_list"

    def add(self, name,callManagerGroupName,
            routeListEnabled="true",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class HuntPilot(AbstractAXLAPI):
    _factory_descriptor = "hunt_pilot"

    def add(self, pattern, huntListName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LineGroup(AbstractAXLAPI):
    _factory_descriptor = "line_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LocalRouteGroup(AbstractAXLAPI):
    _factory_descriptor = "local_route_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RouteGroup(AbstractAXLAPI):
    _factory_descriptor = "route_group"

    def add(self, name, members,
            distributionAlgorithm="Circular",
            **kwargs):
        _check_route_group_port_assignment(members)
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RouteList(AbstractAXLDeviceAPI):
    _factory_descriptor = "route_list"

    def add(self, name, callManagerGroupName,
            runOnEveryNode="true",
            routeListEnabled="true",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RoutePartition(AbstractAXLDeviceAPI):
    _factory_descriptor = "partition"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class RoutePattern(AbstractAXLAPI):
    _factory_descriptor = "route_pattern"

    def add(self, pattern, routePartitionName, destination,
            blockEnable="false",
            provideOutsideDialtone="true",
            networkLocation="OffNet",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipRoutePattern(AbstractAXLAPI):
    _factory_descriptor = "sip_route_pattern"

    def add(self, pattern, routePartitionName, sipTrunkName,
            usage="Domain Routing",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TimePeriod(AbstractAXLAPI):
    _factory_descriptor = "time_period"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TimeSchedule(AbstractAXLAPI):
    _factory_descriptor = "time_schedule"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TransPattern(AbstractAXLAPI):
    _factory_descriptor = "translation_pattern"

    def add(self, pattern, routePartitionName,
            usage="Translation",
            provideOutsideDialtone="true",
            patternUrgency="true",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, dialPlanName=None, routeFilterName=None, returnedTags=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().get(**add_kwargs)

