# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""

from .base import AbstractAXLDeviceAPI


class Line(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "pattern",
        "routePartitionName"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES


class Phone(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "devicePoolName"
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            protocol="SIP",
            **kwargs):
        """Extend 'add' to provide defaults for attrs that constrant for this API call

        :param protocol: defaults to 'SIP'
        :param kwargs: phone attribute kwargs
        :return: API Data Model object
        """
        # workaround for restricted 'class' attribute
        if "class" not in kwargs:
            kwargs["class"] = "Phone"
        default_kwargs = {
            "protocol": protocol,
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)

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

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "devicePoolName"
    )

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
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)


class DeviceProfile(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "class",
        "protocol",
        "phoneTemplateName",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            protocol="SIP",
            **kwargs):
        """Extend 'add' to provide defaults for attrs that constrant for this API call

        :param protocol: default kwarg for easy method-calling
        :param kwargs:
        :return: API Data Model object
        """
        # workaround for restricted 'class' attribute
        if "class" not in kwargs:
            kwargs["class"] = "Device Profile"
        default_kwargs = {
            "protocol": protocol,
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)

