# -*- coding: utf-8 -*-
"""CUCM Media Configuration APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args


class ConferenceBridge(AbstractAXLDeviceAPI):
    _factory_descriptor = "conference_bridge"

    def add(self, name, devicePoolName, product="Cisco IOS Conference Bridge", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class MediaResourceGroup(AbstractAXLAPI):
    _factory_descriptor = "mrg"

    def add(self, name, members, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class MediaResourceList(AbstractAXLDeviceAPI):
    _factory_descriptor = "mrgl"

    def add(self, name, members, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class Mtp(AbstractAXLDeviceAPI):
    _factory_descriptor = "mtp"

    def add(self, name, devicePoolName, mtpType="Cisco IOS Enhanced Software Media Termination Point", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))
