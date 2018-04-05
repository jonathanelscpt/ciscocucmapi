# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from . import AbstractAXLDeviceAPI


class Phone(AbstractAXLDeviceAPI):
    """Cisco CUCM Phones API.

    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'phone'
    _RETURN_OBJECT_NAME = 'phone'
    _IDENTIFIERS = (
        "name",
        "uuid"
    )
    _LIST_API_SEARCH_CRITERIA = (
        "name",
        "description",
        "protocol",
        "callingSearchSpaceName",
        "devicePoolName",
        "securityProfileName"
    )
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "protocolSide",
        "devicePoolName",
        "commonPhoneConfigName",
        "useTrustedRelayPoint",
        "locationName"
    )

    def __init__(self, client, object_factory):
        """Initialize a new Phone object with the provided AXL client.

        :param client: zeep SOAP AXL client for API calls to CUCM's SOAP interface
        :param object_factory: factory function for instantiating data models objects
        :raises TypeError: If parameter types are invalid.
        """
        super(Phone, self).__init__(client, object_factory)

    @classmethod
    def object_type(cls):
        return cls._OBJECT_TYPE

    @classmethod
    def return_object_name(cls):
        return cls._RETURN_OBJECT_NAME

    @classmethod
    def add_api_mandatory_attributes(cls):
        return cls._ADD_API_MANDATORY_ATTRIBUTES

    @classmethod
    def list_api_search_criteria(cls):
        return cls._LIST_API_SEARCH_CRITERIA

    @classmethod
    def identifiers(cls):
        return cls._IDENTIFIERS

    def wipe(self, **kwargs):
        """Allows Cisco's newer Android-based devices, like the Cisco DX650,
        to be remotely reset to factory defaults, removing user specific settings and data.

        :param kwargs: phone name or uuid, but not both
        :return: None
        :raises TypeError: if name or uuid not supplied
        """
        self._check_identifiers(**kwargs)
        self._serialize_axl_object(self, "wipe", **kwargs)

    def options(self, uuid, returned_choices=None):
        self._client.getPhoneOptions(uuid, returnedChoices=returned_choices)

