# -*- coding: utf-8 -*-
"""CUCM System Configuration APIs."""

from datetime import datetime, timedelta

from zeep.helpers import serialize_object
from zeep.exceptions import Fault

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_kwargs, get_signature_locals
from ..exceptions import AXLError


class CallManagerGroup(AbstractAXLDeviceAPI):
    _factory_descriptor = "callmanager_group"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DevicePool(AbstractAXLDeviceAPI):
    _factory_descriptor = "device_pool"

    def add(self, name, callManagerGroupName, dateTimeSettingName, regionName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DateTimeGroup(AbstractAXLAPI):
    _factory_descriptor = "date_time_group"

    def add(self, name, timeZone, separator="-", dateformat="M-D-Y", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LdapDirectory(AbstractAXLAPI):
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

    def sync(self, name=None, uuid=None, sync="true"):
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


class LdapFilter(AbstractAXLAPI):
    _factory_descriptor = "ldap_filter"

    def add(self, name, filter, **kwargs):  # shadow not used
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


# issue - not working!
class LdapSyncCustomField(AbstractAXLAPI):
    _factory_descriptor = "ldap_custom_field"

    def add(self, ldapConfigurationName, customUserField, ldapUserField, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Location(AbstractAXLAPI):
    _factory_descriptor = "location"

    def add(self, name, betweenLocations=None, **kwargs):
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


class PhoneNtp(AbstractAXLAPI):
    _factory_descriptor = "phone_ntp_reference"

    def add(self, ipAddress, mode="Directed Broadcast", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Region(AbstractAXLAPI):
    _factory_descriptor = "region"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Srst(AbstractAXLAPI):
    _factory_descriptor = "srst"

    def add(self, name, ipAddress, SipNetwork=None, **kwargs):
        if not SipNetwork:
            SipNetwork=ipAddress
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
