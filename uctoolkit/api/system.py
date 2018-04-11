# -*- coding: utf-8 -*-
"""CUCM System Configuration APIs."""

from uctoolkit.api.abstract import AbstractAXLAPI, AbstractAXLDeviceAPI


class CallManagerGroup(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'callmanager_group'
    _RETURN_OBJECT_NAME = 'callManagerGroup'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "members"
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


class DevicePool(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'device_pool'
    _RETURN_OBJECT_NAME = 'devicePool'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "dateTimeSettingName",
        "callManagerGroupName",
        "regionName",
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


