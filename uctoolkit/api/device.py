# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .abstract import AbstractAXLDeviceAPI


class Line(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'line'
    _RETURN_OBJECT_NAME = 'line'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "routePartitionName",
        "usage"
    )

    def __init__(self, client, object_factory):
        super(Line, self).__init__(client, object_factory)

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class Phone(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'phone'
    _RETURN_OBJECT_NAME = 'phone'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "devicePoolName",
        "commonPhoneConfigName",
        "locationName"
    )

    def __init__(self, connector, object_factory):
        super(Phone, self).__init__(connector, object_factory)

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def wipe(self, **kwargs):
        """Allows Cisco's newer Android-based devices, like the Cisco DX650,
        to be remotely reset to factory defaults, removing user specific settings and data.

        :param kwargs: phone name or uuid
        :return: None
        """
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._serialize_axl_object("wipe", **kwargs)

    def options(self, uuid, returned_choices=None):
        # self._client.getPhoneOptions(uuid, returnedChoices=returned_choices)
        # todo - needs further AXL API review
        raise NotImplementedError
