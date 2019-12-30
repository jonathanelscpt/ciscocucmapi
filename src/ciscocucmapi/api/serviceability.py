"""CUCM Serviceability APIs provided via AXL"""

from zeep.helpers import serialize_object

from .._internal_utils import flatten_signature_kwargs
from .base import SimpleAXLAPI


class BillingServer(SimpleAXLAPI):
    _factory_descriptor = "billing_server"

    def add(self, hostName, userId, password, directory="/", resendOnFailure=True, billingServerProtocol="SFTP",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class ProcessNodeService(SimpleAXLAPI):
    _factory_descriptor = "process_node_service"
    supported_methods = ["get", "update", "list"]


class SNMPCommunityString(SimpleAXLAPI):
    _factory_descriptor = "snmp_community_string"
    supported_methods = ["model", "create", "add", "get", "update", "remove"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._return_name = self.__class__.__name__

    def add(self, communityName, ArrayOfHosts, accessPrivilege=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, communityName):
        # todo - this violates LSP due to invalid method signature.  a case for class re-design
        """Get method for SNMP Community String"""
        axl_resp = self.connector.service.getSNMPCommunityString(communityName=communityName)
        return self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"][self._return_name])


class SNMPMIB2List(SimpleAXLAPI):
    _factory_descriptor = "snmp_mib2_system_group"
    supported_methods = ["get", "update"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._return_name = self.__class__.__name__

    def get(self, sysContact):
        # todo - this violates LSP due to invalid method signature.  a case for class re-design
        """Get method for SNMPMIB2List"""
        axl_resp = self.connector.service.getSNMPMIB2List(sysContact=sysContact)
        return self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"][self._return_name])


class SNMPUser(SimpleAXLAPI):
    _factory_descriptor = "snmp_user"
    supported_methods = ["model", "create", "add", "get", "update", "remove"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._return_name = self.__class__.__name__

    def add(self, userName, ArrayOfHosts, accessPrivilege=None, authRequired=True, authPassword=None,
            authProtocol="SHA", privacyRequired=True, privacyPassword=None, privacyProtocol="AES128", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, userName):
        # todo - this violates LSP due to invalid method signature.  a case for class re-design
        """Get method for SNMP Users"""
        axl_resp = self.connector.service.getSNMPUser(userName=userName)
        return self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"][self._return_name]
        )


class SyslogConfiguration(SimpleAXLAPI):
    _factory_descriptor = "syslog_configuration"
    supported_methods = ["get", "update"]

    def get(self, serverName, serviceGroup="CM Services", service="Cisco CallManager", **kwargs):
        get_kwargs = flatten_signature_kwargs(self.get, locals())
        return super().get(**get_kwargs)

    def update(self, serverName, serviceGroup="CM Services", service="Cisco CallManager", alarmConfigs=None):
        update_kwargs = flatten_signature_kwargs(self.update, locals())
        return super().update(**update_kwargs)
