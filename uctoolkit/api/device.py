# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI, check_identifiers
from .._internal_utils import flatten_signature_args


class Line(AbstractAXLDeviceAPI):
    _factory_descriptor = "line"

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        # self._factory_name = "line"

    def add(self, name, routePartitionName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class Phone(AbstractAXLDeviceAPI):
    _factory_descriptor = "phone"

    def add(self, name, product, devicePoolName, protocol="SIP", **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Phone"
        return super().add(**flatten_signature_args(self.add, locals()))

    def wipe(self, **kwargs):
        """Allows Cisco's newer Android-based devices, like the Cisco DX650,
        to be remotely reset to factory defaults, removing user specific settings and data.

        :param kwargs: phone name or uuid
        :return: None
        """
        check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._serialize_axl_object("wipe", **kwargs)

    def options(self, uuid, returned_choices=None):
        # self._client.getPhoneOptions(uuid, returnedChoices=returned_choices)
        # todo - needs further AXL API review
        raise NotImplementedError


class CtiRoutePoint(AbstractAXLDeviceAPI):
    _factory_descriptor = "cti_route_point"

    def add(self, name, devicePoolName, product="CTI Route Point", protocol="SCCP", **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "CTI Route Point"
        return super().add(**flatten_signature_args(self.add, locals()))


class DeviceProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "udp"

    def add(self, name, product, phoneTemplateName, protocol="SIP", **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Device Profile"
        return super().add(**flatten_signature_args(self.add, locals()))


class PhoneButtonTemplate(AbstractAXLAPI):
    _factory_descriptor = "phone_button_template"

    def add(self, name, basePhoneTemplateName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))
