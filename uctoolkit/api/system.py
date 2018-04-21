# -*- coding: utf-8 -*-
"""CUCM System Configuration APIs."""

from datetime import datetime, timedelta

from zeep.helpers import serialize_object
from zeep.exceptions import Fault

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs, get_signature_locals
from ..exceptions import AXLError


class AudioCodecPreferenceList(SimpleAXLAPI):
    _factory_descriptor = "audio_codec_preference_list"

    def add(self, name, description, codecsInList, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallManagerGroup(DeviceAXLAPI):
    _factory_descriptor = "callmanager_group"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceMobilityGroup(SimpleAXLAPI):
    _factory_descriptor = "device_mobility_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceMobility(SimpleAXLAPI):
    _factory_descriptor = "device_mobility_info"

    def add(self, name, subNet, subNetMaskSz, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DevicePool(DeviceAXLAPI):
    _factory_descriptor = "device_pool"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, callManagerGroupName, dateTimeSettingName, regionName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DateTimeGroup(DeviceAXLAPI):
    _factory_descriptor = "date_time_group"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, timeZone,
            separator="-",
            dateformat="M-D-Y",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LdapDirectory(SimpleAXLAPI):
    _factory_descriptor = "ldap_directory"

    def add(self,
            name, ldapDn, ldapPassword, userSearchBase, servers,
            intervalValue=7,
            scheduleUnit="DAY",
            nextExecTime=None,
            **kwargs):
        if not nextExecTime:
            nextExecTime = (datetime.now() + timedelta(days=intervalValue+1)).strftime("%y-%m-%d 00:00")
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def sync(self, name=None, uuid=None, sync=True):
        try:
            kwargs = get_signature_locals(self.get_sync_status, locals())
            axl_resp = self.connector.service.doLdapSync(**kwargs)
            return serialize_object(axl_resp)["return"]
        except Fault as fault:
            raise AXLError(fault.message)

    def get_sync_status(self, name=None, uuid=None):
        try:
            kwargs = get_signature_locals(self.get_sync_status, locals())
            axl_resp = self.connector.service.getLdapSyncStatus(**kwargs)
            return serialize_object(axl_resp)["return"]
        except Fault as fault:
            raise AXLError(fault.message)


class LdapFilter(SimpleAXLAPI):
    _factory_descriptor = "ldap_filter"

    def add(self, name, filter, **kwargs):  # shadow not used
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


# issue - not working!
class LdapSyncCustomField(SimpleAXLAPI):
    _factory_descriptor = "ldap_custom_field"

    def add(self, ldapConfigurationName, customUserField, ldapUserField, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LbmGroup(SimpleAXLAPI):
    _factory_descriptor = "lbm_group"

    def add(self, name, ProcessnodeActive,
            ProcessnodeStandby=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LbmHubGroup(SimpleAXLAPI):
    _factory_descriptor = "lbm_hub_group"

    def add(self, name, member1,
            member2=None,
            member3=None,
            members=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Location(SimpleAXLAPI):
    _factory_descriptor = "location"

    def add(self, name,
            betweenLocations=None,
            **kwargs):
        # this approach is probably not compatible with pre-9's flattened locations.
        # if warranted in future, would require extension for a version check.
        if not betweenLocations:
            betweenLocations = {
                "betweenLocation": {
                    "locationName": "Hub_None",
                    "audioBandwidth": 0,  # translates to 'UNLIMITED'
                    "videoBandwidth": 384,  # investigate default?
                    "immersiveBandwidth": 384,
                    "weight": 50
                }
            }
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PresenceRedundancyGroup(SimpleAXLAPI):
    _factory_descriptor = "presence_redundancy_group"

    def add(self, name, server1,
            server2=None,
            haEnabled=False,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhoneNtp(SimpleAXLAPI):
    _factory_descriptor = "phone_ntp_reference"

    def add(self, ipAddress, mode="Directed Broadcast", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhysicalLocation(SimpleAXLAPI):
    _factory_descriptor = "physical_location"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PresenceGroup(SimpleAXLAPI):
    _factory_descriptor = "presence_group"

    def add(self, name, presenceGroups=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Region(DeviceAXLAPI):
    _factory_descriptor = "region"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "restart"]

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Srst(DeviceAXLAPI):
    _factory_descriptor = "srst"

    def add(self, name, ipAddress, SipNetwork=None, **kwargs):
        # there are corner cases, but this is a good for optimized usability
        if not SipNetwork:
            SipNetwork=ipAddress
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
