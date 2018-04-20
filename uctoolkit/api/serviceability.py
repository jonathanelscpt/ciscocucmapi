# -*- coding: utf-8 -*-
"""CUCM Serviceability APIs provided via AXL"""

from zeep.helpers import serialize_object

from .base import SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


class BillingServer(SimpleAXLAPI):
    _factory_descriptor = "billing_server"

    def add(self, hostName, userId, password,
            directory="/",
            resendOnFailure=True,
            billingServerProtocol="SFTP",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SNMPCommunityString(SimpleAXLAPI):
    _factory_descriptor = "snmp_community_string"
    supported_methods = ["model", "create", "add", "get", "update", "remove"]

    def add(self, communityName, ArrayOfHosts,
            accessPrivilege=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, communityName):
        # this violates LSP due to invalid method signature.  a case for class re-design
        """Get method for SNMP Community String"""
        axl_resp = self.connector.service.getSNMPCommunityString(communityName=communityName)
        return self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"]["SNMPUser"]
        )


class SNMPUser(SimpleAXLAPI):
    _factory_descriptor = "snmp_user"
    supported_methods = ["model", "create", "add", "get", "update", "remove"]

    def add(self, userName, ArrayOfHosts,
            accessPrivilege=None,
            authRequired=True,
            authPassword=None,
            authProtocol="SHA",
            privacyRequired=True,
            privacyPassword=None,
            privacyProtocol="AES128",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def get(self, userName):
        # this violates LSP due to invalid method signature.  a case for class re-design
        """Get method for SNMP Users"""
        axl_resp = self.connector.service.getSNMPUser(userName=userName)
        self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"]["SNMPUser"]
        )

