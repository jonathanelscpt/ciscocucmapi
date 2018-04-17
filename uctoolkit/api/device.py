# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI, check_identifiers
from .._internal_utils import flatten_signature_args
from ..exceptions import AXLMethodDoesNotExist


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


class Line(AbstractAXLDeviceAPI):
    _factory_descriptor = "line"

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)

    def add(self, name, routePartitionName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class Phone(AbstractAXLDeviceAPI):
    _factory_descriptor = "phone"

    def add(self, name, product, devicePoolName,
            locationName="Hub_None",
            protocol="SIP",
            **kwargs):
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


class PhoneButtonTemplate(AbstractAXLAPI):
    _factory_descriptor = "phone_button_template"

    def add(self, name, basePhoneTemplateName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class RemoteDestination(AbstractAXLAPI):
    _factory_descriptor = "remote_destination"

    def add(self, destination, ownerUserId,
            name=None,
            enableUnifiedMobility="true",
            enableMobileConnect="true",
            isMobilePhone="true",
            remoteDestinationProfileName=None,
            dualModeDeviceName=None,
            lineAssociations=None,
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class RemoteDestinationProfile(AbstractAXLAPI):
    _factory_descriptor = "rdp"

    def add(self, name, devicePoolName, userId,
            rerouteCallingSearchSpaceName=None,
            callingSearchSpaceName=None,
            lines=None,
            product="Remote Destination Profile",
            protocol="Remote Destination",
            protocolSide="User",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Remote Destination Profile"
        return super().add(**flatten_signature_args(self.add, locals()))


class SipTrunk(AbstractAXLDeviceAPI):
    _factory_descriptor = "sip_trunk"

    def add(self, name, devicePoolName, destinations,
            product="SIP Trunk",
            locationName="Hub_None",
            protocol="SIP",
            securityProfileName="Non Secure SIP Trunk Profile",
            sipProfileName="Standard SIP Profile",
            presenceGroupName="Standard Presence Group",
            protocolSide="Network",
            **kwargs):
        if "class" not in kwargs:
            kwargs["class"] = "Trunk"
        return super().add(**flatten_signature_args(self.add, locals()))


class SipProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "sip_profile"

    def add(self, name,
            sdpTransparency="Pass all unknown SDP attributes",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class SipTrunkSecurityProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "sip_trunk_security_profile"

    def add(self, name,
            acceptPresenceSubscription="false",
            acceptOutOfDialogRefer="false",
            acceptUnsolicitedNotification="false",
            allowReplaceHeader="false",
            transmitSecurityStatus="false",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class UniversalDeviceTemplate(AbstractAXLAPI):
    _factory_descriptor = "udt"

    def add(self, name, devicePool,
            directoryNumber=None,
            lineLabel=None,
            displayCallerId=None,
            callingSearchSpace=None,
            sipProfile="Standard SIP Profile",
            commonPhoneProfile="Standard Common Phone Profile",
            phoneButtonTemplate="Universal Device Template Button Layout",
            deviceSecurityProfile="Universal Device Template - Model-independent Security Profile",
            blfPresenceGroup="Standard Presence group",
            location="Hub_None",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class UniversalLineTemplate(AbstractAXLAPI):
    _factory_descriptor = "ult"

    def add(self, name,
            lineDescription=None,
            callingSearchSpace=None,
            routePartition=None,
            voiceMailProfile=None,
            alertingName=None,
            rejectAnonymousCall="false",
            blfPresenceGroup="Standard Presence group",
            **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

