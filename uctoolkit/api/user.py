# -*- coding: utf-8 -*-
"""CUCM AXL User APIs."""

from collections import defaultdict

from zeep.helpers import serialize_object

from .base import SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


class AppUser(SimpleAXLAPI):
    _factory_descriptor = "application_user"

    def add(self, userid,
            associatedDevices=None,
            associatedGroups=None,
            ctiControlledDeviceProfiles=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class FeatureGroupTemplate(SimpleAXLAPI):
    _factory_descriptor = "feature_group_template"

    def add(self, name,
            serviceProfile=None,
            userProfile=None,
            homeCluster=True,
            imAndUcPresenceEnable=True,
            meetingInformation=True,
            allowCTIControl=True,
            BLFPresenceGp="Standard Presence group",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SelfProvisioning(SimpleAXLAPI):
    _factory_descriptor = "self_provisioning"
    supported_methods = ["update"]

    def update(self,
               requireAuthentication=False,
               allowAuthentication=False,
               authenticationCode=None,
               ctiRoutePoint=None,
               applicationUser=None,
               **kwargs):
        update_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().update(**update_kwargs)


class ServiceProfile(SimpleAXLAPI):
    _factory_descriptor = "service_profile"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipRealm(SimpleAXLAPI):
    _factory_descriptor = "sip_realm"

    def add(self, realm, userid, digestCredentials,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class UcService(SimpleAXLAPI):
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
        # whitespace won't work with defaultdict, so if statements for the rest
        if not productType:
            if serviceType == "IM and Presence":
                productType = "Unified CM (IM and Presence)"
            elif serviceType == "Video Conference Scheduling Portal":
                productType = "	Telepresence Management System"
            else:
                productType = product_types[serviceType]
        protocols = defaultdict(
            lambda: None,
            CTI="TCP",
            Voicemail="HTTPS"
        )
        if "protocol" not in kwargs:
            kwargs["protocol"] = protocols[serviceType]
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class User(SimpleAXLAPI):
    _factory_descriptor = "user"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "change_dnd_status"]

    def add(self, userid, lastName,
            presenceGroupName="Standard Presence group",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def change_dnd_status(self,
                          userID=None,
                          uuid=None,
                          dndStatus=False):
        """Change Do Not Disturb status for user

        :param userID: (str) userid
        :param uuid: user uuid
        :param dndStatus: (bool) user's do not disturb status
        :return: (str) user pkid
        """
        if uuid:
            axl_resp = self.connector.service.doChangeDNDStatus(uuid=uuid, dndStatus=dndStatus)
        else:
            axl_resp = self.connector.service.doChangeDNDStatus(userID=userID, dndStatus=dndStatus)
        return serialize_object(axl_resp)["return"]


class UserGroup(SimpleAXLAPI):
    """Access Control Groups API"""
    _factory_descriptor = "user_group"

    def add(self, name, members=None, userRoles=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


# class UserPhoneAssociation(AbstractAXLAPI):
#     _factory_descriptor = "quick_user_phone_add"
#
#     def add(self, userId, lastName, extension,
#             firstName=None,
#             routePartitionName=None,
#             name=None, productType=None,
#             **kwargs):
#         return super().add(**flatten_signature_args(self.add, locals()))
#
#     def get(self, returnedTags=None, **kwargs):
#         raise AXLMethodDoesNotExist()
#
#     def update(self, **kwargs):
#         raise AXLMethodDoesNotExist()
#
#     def list(self, searchCriteria=None, returnedTags=None, skip=None, first=None):
#         raise AXLMethodDoesNotExist()
#
#     def remove(self, **kwargs):
#         raise AXLMethodDoesNotExist()


class UserProfileProvision(SimpleAXLAPI):
    _factory_descriptor = "user_profile"

    def add(self, name,
            profile=None, deskPhones=None, mobileDevices=None, defaultUserProfile=None,
            universalLineTemplate=None, allowProvision=False,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
