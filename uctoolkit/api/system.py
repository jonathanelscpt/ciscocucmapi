# -*- coding: utf-8 -*-
"""CUCM System Configuration APIs."""

from datetime import datetime, timedelta

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args


class CallManagerGroup(AbstractAXLDeviceAPI):
    _factory_descriptor = "callmanager_group"

    def add(self, name, members, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class DevicePool(AbstractAXLDeviceAPI):
    _factory_descriptor = "device_pool"

    def add(self, name, callManagerGroupName, dateTimeSettingName, regionName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class DateTimeGroup(AbstractAXLDeviceAPI):
    _factory_descriptor = "date_time_group"

    def add(self, name, timeZone, separator="-", dateformat="M-D-Y", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class LdapDirectory(AbstractAXLAPI):
    _factory_descriptor = "ldap_directory"

    def add(self,
            name, ldapDn, ldapPassword, userSearchBase, servers,
            intervalValue=7,
            scheduleUnit="DAY",
            nextExecTime=(datetime.now() + timedelta(days=8)).strftime("%y-%m-%d 00:00"),  # enforced by zeep, not AXL!
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

    def sync_now(self, **kwargs):
        # kwargs["synchronize"] = "true"
        # return self.update(**kwargs)
        # todo - workaround - why is the AXL call not working?
        sql_statement = "update directorypluginconfig set syncnow = '1' where name = '{name}'"
        if "name" in kwargs:
            return self.connector.sql.update(
                sql_statement=sql_statement.format(name=kwargs["name"])
            )
        elif "uuid" in kwargs:
            ldap_dir = self.get(uuid=kwargs["uuid"], returned_tags={"name": ""})
            return self.connector.sql.update(
                sql_statement=sql_statement.format(name=ldap_dir.name)
            )


class LdapFilter(AbstractAXLAPI):
    _factory_descriptor = "ldap_filter"

    def add(self, name, filter, **kwargs):  # shadow not used
        return super().add(**flatten_signature_args(self.add, locals()))


# issue - not working!
class LdapSyncCustomField(AbstractAXLAPI):
    _factory_descriptor = "ldap_custom_field"

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "ldapConfigurationName",
        "customUserField",
        "ldapUserField",
    )

    def add(self, ldapConfigurationName, customUserField, ldapUserField, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


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
                    "videoBandwidth": 384,
                    "immersiveBandwidth": 384,
                    "weight": 50
                }
            }
        return super().add(**flatten_signature_args(self.add, locals()))


class PhoneNtp(AbstractAXLAPI):
    _factory_descriptor = "phone_ntp_reference"

    def add(self, ipAddress, mode="Directed Broadcast", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))
