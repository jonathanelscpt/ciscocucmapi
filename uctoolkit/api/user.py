# -*- coding: utf-8 -*-
"""CUCM AXL User APIs."""

from collections import defaultdict

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args


class ServiceProfile(AbstractAXLAPI):
    _factory_descriptor = "service_profile"

    def add(self, name, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class UcService(AbstractAXLAPI):
    _factory_descriptor = "uc_service"

    def add(self, name, serviceType, hostnameorip, productType=None, **kwargs):
        product_types = defaultdict(
            lambda: None,
            Voicemail="Unity Connection",
            CTI="CTI",
            MailStore="Exchange",
            Conferencing="WebEx (Conferencing)",
            Directory="Directory"
        )
        protocols = defaultdict(
            lambda: None,
            CTI="TCP",
            Voicemail="HTTPS"
        )
        if not productType:
            if serviceType == "IM and Presence":
                productType = "Unified CM (IM and Presence)"
            elif serviceType == "Video Conference Scheduling Portal":
                productType = "	Telepresence Management System"
            else:
                productType = product_types[serviceType]
        if "protocol" not in kwargs:
            kwargs["protocol"] = protocols[serviceType]
        # cannot use locals() as we've created local vars in this method
        kwargs.update({
            "name": name,
            "serviceType": serviceType,
            "hostnameorip": hostnameorip,
            "productType": productType
        })
        return super().add(**kwargs)


class User(AbstractAXLAPI):
    _factory_descriptor = "user"

    def add(self, userid, lastName,
            presenceGroupName="Standard Presence group",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class UserGroup(AbstractAXLAPI):
    """Access Control Groups API"""
    _factory_descriptor = "user_group"

    def add(self, name, members=None, userRoles=None, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

