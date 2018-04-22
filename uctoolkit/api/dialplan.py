# -*- coding: utf-8 -*-
"""CUCM Dial Plan Configuration APIs."""

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


def _check_route_group_port_assignment(members):
    """Assign all ports for route groups members when not specified."""
    if isinstance(members["member"], list):
        for member in members["member"]:
            if "port" not in member:
                member["port"] = 0
    elif isinstance(members["member"], dict):
        if "port" not in members:
            members["port"] = 0
    return members


class AarGroup(SimpleAXLAPI):
    _factory_descriptor = "aar_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class AdvertisedPatterns(SimpleAXLAPI):
    _factory_descriptor = "advertised_patterns"

    def add(self, pattern,
            patternType="Enterprise Number",
            hostedRoutePSTNRule="No PSTN",
            pstnFailStrip=0,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class BlockedLearnedPatterns(SimpleAXLAPI):
    _factory_descriptor = "blocked_learned_patterns"

    def add(self,
            pattern=None,
            prefix=None,
            clusterId=None,
            patternType=None,
            **kwargs):
        if not (pattern or prefix or clusterId):
            raise ValueError("At least one of the match criteria must be specified: {criteria}".format(
                criteria=("pattern", "prefix", "clusterId")
            ))
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallPickupGroup(SimpleAXLAPI):
    _factory_descriptor = "call_pickup_group"

    def add(self, name, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallPark(SimpleAXLAPI):
    _factory_descriptor = "call_park"

    def add(self, pattern, callManagerName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CalledPartyTransformationPattern(SimpleAXLAPI):
    _factory_descriptor = "called_party_xform_pattern"

    def add(self, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallingPartyTransformationPattern(SimpleAXLAPI):
    _factory_descriptor = "calling_party_xform_pattern"

    def add(self, pattern, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CmcInfo(SimpleAXLAPI):
    _factory_descriptor = "cmc"

    def add(self, code, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class ConferenceNow(SimpleAXLAPI):
    _factory_descriptor = "conference_now"

    def add(self, conferenceNowNumber,
            routePartitionName=None,
            maxWaitTimeForHost=15,
            MohAudioSourceId=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Css(SimpleAXLAPI):
    _factory_descriptor = "css"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DirectedCallPark(DeviceAXLAPI):
    _factory_descriptor = "directed_call_park"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "reset"]

    def add(self, pattern, retrievalPrefix, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class EnterpriseFeatureAccessConfiguration(SimpleAXLAPI):
    _factory_descriptor = "mobility_enterprise_feature_access_number"

    def add(self, patter,
            routePartitionName=None,
            isDefaultEafNumber=False,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class FacInfo(SimpleAXLAPI):
    _factory_descriptor = "fac"

    def add(self, name, code, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class HuntList(DeviceAXLAPI):
    _factory_descriptor = "hunt_list"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "reset"]

    def add(self, name,callManagerGroupName,
            routeListEnabled=True,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class HuntPilot(SimpleAXLAPI):
    _factory_descriptor = "hunt_pilot"

    def add(self, pattern, huntListName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LineGroup(SimpleAXLAPI):
    _factory_descriptor = "line_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LocalRouteGroup(SimpleAXLAPI):
    _factory_descriptor = "local_route_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MeetMe(SimpleAXLAPI):
    _factory_descriptor = "meetme"

    def add(self, pattern,
            routePartitionName=None,
            minimumSecurityLevel="Non Secure",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Mobility(SimpleAXLAPI):
    _factory_descriptor = "handoff_mobility"
    supported_methods = ["model", "create", "add", "get", "update"]

    def add(self, handoffNumber,
            handoffPartitionName=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MobilityProfile(SimpleAXLAPI):
    _factory_descriptor = "mobility_profile"

    def add(self, name,
            mobileClientCallingOption="Dial via Office Reverse",
            dvofServiceAccessNumber=None,
            dirn=None,
            dvorCallerId=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RouteGroup(SimpleAXLAPI):
    _factory_descriptor = "route_group"

    def add(self, name, members,
            distributionAlgorithm="Circular",
            **kwargs):
        _check_route_group_port_assignment(members)
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RouteList(DeviceAXLAPI):
    _factory_descriptor = "route_list"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "reset"]

    def add(self, name, callManagerGroupName,
            runOnEveryNode=True,
            routeListEnabled=True,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RoutePartition(DeviceAXLAPI):
    _factory_descriptor = "route_partition"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "restart"]

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RoutePattern(SimpleAXLAPI):
    _factory_descriptor = "route_pattern"

    def add(self, pattern, routePartitionName, destination,
            blockEnable=False,
            provideOutsideDialtone=True,
            networkLocation="OffNet",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipDialRules(SimpleAXLAPI):
    _factory_descriptor = "sip_dial_rules"

    def add(self, name,
            patterns=None,
            plars=None,
            dialPattern="7940_7960_OTHER",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipRoutePattern(SimpleAXLAPI):
    _factory_descriptor = "sip_route_pattern"

    def add(self, pattern, routePartitionName, sipTrunkName,
            usage="Domain Routing",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TimePeriod(SimpleAXLAPI):
    _factory_descriptor = "time_period"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TimeSchedule(SimpleAXLAPI):
    _factory_descriptor = "time_schedule"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class TransPattern(SimpleAXLAPI):
    _factory_descriptor = "translation_pattern"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "options"]

    def add(self, pattern, routePartitionName,
            usage="Translation",
            provideOutsideDialtone=True,
            patternUrgency=True,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, dialPlanName=None, routeFilterName=None, returnedTags=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().get(**add_kwargs)

