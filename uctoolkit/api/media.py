# -*- coding: utf-8 -*-
"""CUCM Media Configuration APIs."""

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


class ConferenceBridge(DeviceAXLAPI):
    _factory_descriptor = "conference_bridge"

    def add(self, name, devicePoolName,
            product="Cisco IOS Conference Bridge",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MediaResourceGroup(SimpleAXLAPI):
    _factory_descriptor = "mrg"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MediaResourceList(SimpleAXLAPI):
    _factory_descriptor = "mrgl"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Mtp(DeviceAXLAPI):
    _factory_descriptor = "mtp"

    def add(self, name, devicePoolName,
            mtpType="Cisco IOS Enhanced Software Media Termination Point",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Transcoder(DeviceAXLAPI):
    _factory_descriptor = "transcoder"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, devicePoolName,
            product="Cisco IOS Enhanced Media Termination Point",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
