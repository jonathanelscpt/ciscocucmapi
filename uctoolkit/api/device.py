# -*- coding: utf-8 -*-
"""CUCM AXL Device APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI, check_identifiers
from .._internal_utils import flatten_signature_kwargs
from ..exceptions import AXLMethodDoesNotExist


class CommonDeviceConfig(AbstractAXLDeviceAPI):
    _factory_descriptor = "common_device_config"

    def add(self, name,
            softkeyTemplateName=None,
            userLocale=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def restart(self, **kwargs):
        raise AXLMethodDoesNotExist

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class CommonPhoneConfig(AbstractAXLDeviceAPI):
    _factory_descriptor = "common_phone_profile"

    def add(self, name,
            unlockPwd=None,
            featureControlPolicy=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def restart(self, **kwargs):
        raise AXLMethodDoesNotExist

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class CtiRoutePoint(AbstractAXLDeviceAPI):
    _factory_descriptor = "cti_route_point"

    def add(self, name, devicePoolName,
            product="CTI Route Point",
            protocol="SCCP",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "CTI Route Point"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "udp"

    def add(self, name, product, phoneTemplateName,
            protocol="SIP",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Device Profile"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class FeatureControlPolicy(AbstractAXLAPI):
    _factory_descriptor = "feature_control_policy"

    def add(self, name,
            features=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class IpPhoneServices(AbstractAXLAPI):
    _factory_descriptor = "ip_phone_service"

    def add(self, serviceName, asciiServiceName, serviceUrl,
            secureServiceUrl=None,
            serviceCategory="XML Service",
            serviceType="Standard IP Phone Service",
            enabled=True,
            enterpriseSubscription=False,
            parameters=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Line(AbstractAXLDeviceAPI):
    _factory_descriptor = "line"

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)

    def add(self, name, routePartitionName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Phone(AbstractAXLDeviceAPI):
    _factory_descriptor = "phone"

    def add(self, name, product, devicePoolName,
            locationName="Hub_None",
            protocol="SIP",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Phone"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def wipe(self, **kwargs):
        """Allows Cisco's newer Android-based devices, like the Cisco DX650,
        to be remotely reset to factory defaults, removing user specific settings and data.

        :param kwargs: phone name or uuid
        :return: None
        """
        # check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._serialize_axl_object("wipe", **kwargs)

    def options(self, uuid, returned_choices=None):
        # self._client.getPhoneOptions(uuid, returnedChoices=returned_choices)
        # todo - needs further AXL API review
        raise NotImplementedError


class PhoneButtonTemplate(AbstractAXLAPI):
    _factory_descriptor = "phone_button_template"

    def add(self, name, basePhoneTemplateName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhoneSecurityProfile(AbstractAXLAPI):
    _factory_descriptor = "phone_security_profile"

    def add(self, name,
            phoneType="Universal Device Template",
            protocol="Protocol Not Specified",
            deviceSecurityMode=None,
            authenticationMode="By Null String",
            keySize=1024,
            transportType="TCP+UDP",
            sipPhonePort=5060,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RecordingProfile(AbstractAXLAPI):
    _factory_descriptor = "recording_profile"

    def add(self, name, recorderDestination,
            recordingCssName=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "sip_profile"

    def add(self, name,
            sdpTransparency="Pass all unknown SDP attributes",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SoftKeyTemplate(AbstractAXLDeviceAPI):
    _factory_descriptor = "softkey_template"

    def add(self, name, description,
            baseSoftkeyTemplateName="Standard User",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def reset(self, **kwargs):
        raise AXLMethodDoesNotExist


class SoftKeySet(AbstractAXLAPI):
    _factory_descriptor = "softkey_set"

    def add(self, **kwargs):
        raise AXLMethodDoesNotExist

    def remove(self, **kwargs):
        raise AXLMethodDoesNotExist


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
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class UniversalLineTemplate(AbstractAXLAPI):
    _factory_descriptor = "ult"

    def add(self, name,
            routePartition=None,
            lineDescription=None,
            callingSearchSpace=None,
            voiceMailProfile=None,
            alertingName=None,
            rejectAnonymousCall="false",  # overrides inconsistency between normal line add and ULT
            blfPresenceGroup="Standard Presence group",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
