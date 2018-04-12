# -*- coding: utf-8 -*-
"""CUCM System Configuration APIs."""

from datetime import datetime, timedelta

from uctoolkit.api.base import AbstractAXLAPI, AbstractAXLDeviceAPI


class CallManagerGroup(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "members"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class DevicePool(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "dateTimeSettingName",
        "callManagerGroupName",
        "regionName",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class DateTimeGroup(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "timeZone",
        "separator",
        "dateformat",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            separator="-",
            dateformat="M-D-Y",
            **kwargs):
        default_kwargs = {
            "separator": separator,
            "dateformat": dateformat
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)


class LdapDirectory(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "ldapDn",
        "ldapPassword",
        "userSearchBase",
        "servers",
        "nextExecTime"  # enforced by zeep, not AXL!
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            intervalValue=7,
            scheduleUnit="DAY",
            nextExecTime=(datetime.now() + timedelta(days=8)).strftime("%y-%m-%d 00:00"),
            **kwargs):
        default_kwargs = {
            "intervalValue": intervalValue,
            "scheduleUnit": scheduleUnit,
            "nextExecTime": nextExecTime,
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)

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

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "filter",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


# issue - not working!
class LdapSyncCustomField(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "ldapConfigurationName",
        "customUserField",
        "ldapUserField",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class LdapSystem(AbstractAXLAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "filter",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES
