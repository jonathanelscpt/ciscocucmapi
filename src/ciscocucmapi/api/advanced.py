"""CUCM AXL Advanced APIs."""

from operator import methodcaller

from zeep.helpers import serialize_object

from .._internal_utils import flatten_signature_kwargs
from ..helpers import get_model_dict
from .base import DeviceAXLAPI
from .base import SimpleAXLAPI


class CalledPartyTracing(SimpleAXLAPI):
    _factory_descriptor = "called_party_tracing"
    supported_methods = ["add", "list", "remove"]

    def add(self, directorynumber, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DirNumberAliasLookupandSync(SimpleAXLAPI):
    _factory_descriptor = "directory_number_alias_sync"

    def add(self, ldapConfigName, ldapManagerDisgName, ldapPassword, ldapUserSearch, servers,
            ldapDirectoryServerUsage="DirSync", enableCachingofRecords=False, sipAliasSuffix=None,
            keepAliveSearch=None, keepAliveTime=5, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class IlsConfig(SimpleAXLAPI):
    _factory_descriptor = "ils_config"
    supported_methods = ["get", "update"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._get_model_name = "NewIlsConfig"

    def get(self, clusterId, returnedTags=None, **kwargs):
        if not returnedTags:
            get_model = self._get_wsdl_obj(self._get_model_name)
            returnedTags = get_model_dict(get_model)
        return super().get(clusterId=clusterId, returnedTags=returnedTags, **kwargs)


class MessageWaiting(SimpleAXLAPI):
    _factory_descriptor = "mwi_number"

    def add(self, pattern, routePartitionName=None, callingSearchSpaceName=None, messageWaitingIndicator=False,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RemoteCluster(SimpleAXLAPI):
    _factory_descriptor = "remote_cluster"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "do_update"]

    def add(self, clusterId, fullyQualifiedName, emcc=None, pstnAccess=None, rsvpAgent=None, tftp=None, lbm=None,
            uds=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def do_update(self, clusterId, server):
        kwargs = {
            "clusterId": clusterId,
            "server": server
        }
        options_method = methodcaller("".join(["doUpdate", self.__class__.__name__]), **kwargs)
        axl_resp = options_method(self.connector.service)
        return self.object_factory(
            "".join([self.__class__.__name__]),
            serialize_object(axl_resp)["return"])


class SecureConfig(SimpleAXLAPI):
    _factory_descriptor = "secure_config"
    supported_methods = ["get", "update"]

    def get(self, name="NativeEmergencyCallHandling", returnedTags=None, **kwargs):
        get_kwargs = flatten_signature_kwargs(self.get, locals())
        return super().get(**get_kwargs)

    def update(self, name="NativeEmergencyCallHandling", value="Enabled", **kwargs):
        update_kwargs = flatten_signature_kwargs(self.get, locals())
        return super().get(**update_kwargs)


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

    def add(self, name, url, certificates, vpnGateways=None, **kwargs):
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

    def add(self, name, autoNetworkDetection=False, mtu=1920, failToConnect=30, enableHostIdCheck=True,
            clientAuthentication="User and Password", pwdPersistant=False, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
