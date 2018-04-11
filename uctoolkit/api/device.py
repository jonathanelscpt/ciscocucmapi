# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""

from .abstract import AbstractAXLDeviceAPI


class Line(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'line'
    _RETURN_OBJECT_NAME = 'line'
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "routePartitionName",
        "usage"
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
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"],**kwargs)
        self._serialize_axl_object("wipe", **kwargs)

    def options(self, uuid, returned_choices=None):
        # self._client.getPhoneOptions(uuid, returnedChoices=returned_choices)
        # todo - needs further AXL API review
        raise NotImplementedError


class CtiRoutePoint(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'cti_route_point'
    _RETURN_OBJECT_NAME = 'ctiRoutePoint'
    # locationName marked mandatory in UI, but not API - default to Hub_None
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "devicePoolName",
        # "locationName"
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

    def add(self,
            product="CTI Route Point",
            protocol="SCCP",
            **kwargs):
        """Extend 'add' to provide defaults for attrs that constrant for this API call

        :param product: default kwarg for easy method-calling
        :param protocol: default kwarg for easy method-calling
        :param kwargs:
        :return: API Data Model object
        """
        # workaround for restricted 'class' attribute
        if "class" not in kwargs:
            kwargs["class"] = "CTI Route Point"
        default_kwargs = {
            "product": product,
            "protocol": protocol,
        }
        kwargs.update(default_kwargs)
        return super(CtiRoutePoint, self).add(**kwargs)

