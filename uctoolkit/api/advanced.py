# -*- coding: utf-8 -*-
"""CUCM AXL Advanced APIs."""

from operator import methodcaller

from zeep.helpers import serialize_object
from zeep.exceptions import Fault

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs
from ..exceptions import AXLError


class RemoteCluster(SimpleAXLAPI):
    _factory_descriptor = "remote_cluster"

    def add(self, clusterId, fullyQualifiedName,
            emcc=None,
            pstnAccess=None,
            rsvpAgent=None,
            tftp=None,
            lbm=None,
            uds=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def do_update(self, clusterId, server):
        try:
            kwargs = {
                "clusterId": clusterId,
                "server": server
            }
            options_method = methodcaller("".join(["doUpdate", self.__class__.__name__]), **kwargs)
            axl_resp = options_method(self.connector.service)
            return self.object_factory(
                "".join([self.__class__.__name__]),
                serialize_object(axl_resp)["return"]
            )
        except Fault as fault:
            raise AXLError(fault.message)


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

