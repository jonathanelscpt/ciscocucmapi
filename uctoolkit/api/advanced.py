# -*- coding: utf-8 -*-
"""CUCM AXL Advanced APIs."""

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


class VoiceMailPilot(SimpleAXLAPI):
    _factory_descriptor = "voicemail_pilot"

    def add(self, dirn, isDefault=False, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VoiceMailProfile(DeviceAXLAPI):
    _factory_descriptor = "voicemail_profile"

    def add(self, name, voiceMailPilot, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VpnGateway(SimpleAXLAPI):
    _factory_descriptor = "vpn_gateway"

    def add(self, name, url, certificates,
            vpnGateways=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VpnGroup(SimpleAXLAPI):
    _factory_descriptor = "vpn_group"

    def add(self, name,
            vpnGateways=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VpnProfile(SimpleAXLAPI):
    _factory_descriptor = "vpn_profile"

    def add(self, name,
            autoNetworkDetection=False,
            mtu=1920,
            failToConnect=30,
            enableHostIdCheck=True,
            clientAuthentication="User and Password",
            pwdPersistant=False,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

