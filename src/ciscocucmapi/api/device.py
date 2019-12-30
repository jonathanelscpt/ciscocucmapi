"""CUCM AXL Device APIs."""

from .._internal_utils import flatten_signature_kwargs
from .base import DeviceAXLAPI
from .base import SimpleAXLAPI


class CommonDeviceConfig(DeviceAXLAPI):
    _factory_descriptor = "common_device_config"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, softkeyTemplateName=None, userLocale=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CommonPhoneConfig(DeviceAXLAPI):
    _factory_descriptor = "common_phone_profile"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, unlockPwd=None, featureControlPolicy=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CtiRoutePoint(DeviceAXLAPI):
    _factory_descriptor = "cti_route_point"

    def add(self, name, devicePoolName, product="CTI Route Point", protocol="SCCP", **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "CTI Route Point"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DefaultDeviceProfile(SimpleAXLAPI):
    _factory_descriptor = "default_device_profile"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "options"]

    def add(self, name, product, phoneButtonTemplate="Universal Device Template Button Layout", softkeyTemplate=None,
            protocol="SIP", protocolSide="User", **kwargs):
        # the name is not obvious in the UI.  It appears to default to a concat of product and protocol.
        # it may be useful to log a warning for this...
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Device Profile"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceProfile(SimpleAXLAPI):
    _factory_descriptor = "udp"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "options"]

    def add(self, name, product, phoneTemplateName,
            protocol="SIP",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Device Profile"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class FeatureControlPolicy(SimpleAXLAPI):
    _factory_descriptor = "feature_control_policy"

    def add(self, name,
            features=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class IpPhoneServices(SimpleAXLAPI):
    _factory_descriptor = "ip_phone_service"

    def add(self, serviceName, asciiServiceName, serviceUrl, secureServiceUrl=None, serviceCategory="XML Service",
            serviceType="Standard IP Phone Service", enabled=True, enterpriseSubscription=False, parameters=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Line(DeviceAXLAPI):
    _factory_descriptor = "line"
    supported_methods = [
        "model", "create", "add", "get", "update", "list", "remove", "options", "apply", "restart", "reset"
    ]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)

    def add(self, pattern, routePartitionName,
            usage="Device",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class NetworkAccessProfile(SimpleAXLAPI):
    _factory_descriptor = "network_access_profile"

    def add(self, name, vpnRequired="Default", proxySettings="None", proxyHostname="", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Phone(DeviceAXLAPI):
    _factory_descriptor = "phone"
    supported_methods = [
        "model", "create", "add", "get", "list", "update", "remove",
        "options", "wipe", "lock",
        "apply", "restart", "reset",
    ]

    @staticmethod
    def _check_confidential_access(confidentialAccess):
        """Workaround for AXL defect not accepting None for 'confidentialAccessMode'"""
        if not confidentialAccess['confidentialAccessMode']:
            confidentialAccess['confidentialAccessMode'] = ''
        return confidentialAccess

    def add(self, name, product, devicePoolName, locationName="Hub_None", protocol="SIP",
            commonPhoneConfigName="Standard Common Phone Profile", **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Phone"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        try:
            add_kwargs['confidentialAccess'] = self._check_confidential_access(add_kwargs['confidentialAccess'])
        except KeyError:
            pass
        return super().add(**add_kwargs)

    def update(self, **kwargs):
        try:
            kwargs['confidentialAccess'] = self._check_confidential_access(kwargs['confidentialAccess'])
        except KeyError:
            pass
        return super().update(**kwargs)

    def wipe(self, **kwargs):
        """Allows Cisco's newer Android-based devices, like the Cisco DX650,
        to be remotely reset to factory defaults, removing user specific settings and data.

        :param kwargs: phone name or uuid
        :return: None
        """
        # check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_axl_object("wipe", **kwargs)

    def lock(self, **kwargs):
        return self._serialize_axl_object("lock", **kwargs)


class PhoneButtonTemplate(DeviceAXLAPI):
    _factory_descriptor = "phone_button_template"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "restart"]

    def add(self, name, basePhoneTemplateName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhoneSecurityProfile(DeviceAXLAPI):
    _factory_descriptor = "phone_security_profile"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "restart"]

    def add(self, name, phoneType="Universal Device Template", protocol="Protocol Not Specified",
            deviceSecurityMode=None, authenticationMode="By Null String", keySize=1024, transportType="TCP+UDP",
            sipPhonePort=5060, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RecordingProfile(SimpleAXLAPI):
    _factory_descriptor = "recording_profile"

    def add(self, name, recorderDestination, recordingCssName=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RemoteDestination(SimpleAXLAPI):
    _factory_descriptor = "remote_destination"

    def add(self, destination, ownerUserId, name=None, enableUnifiedMobility=True, enableMobileConnect=True,
            isMobilePhone=True, remoteDestinationProfileName=None, dualModeDeviceName=None, lineAssociations=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class RemoteDestinationProfile(SimpleAXLAPI):
    _factory_descriptor = "rdp"

    def add(self, name, devicePoolName, userId, rerouteCallingSearchSpaceName=None, callingSearchSpaceName=None,
            lines=None, product="Remote Destination Profile", protocol="Remote Destination", protocolSide="User",
            **kwargs):
        if "class" not in kwargs:  # workaround for restricted 'class' attribute
            kwargs["class"] = "Remote Destination Profile"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SdpTransparencyProfile(SimpleAXLAPI):
    _factory_descriptor = "sdp_transparency_profile"

    def add(self, name, attributeSet, **kwargs):
        if "class" not in kwargs:
            kwargs["class"] = "Trunk"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipTrunk(DeviceAXLAPI):
    _factory_descriptor = "sip_trunk"

    def add(self, name, devicePoolName, destinations, product="SIP Trunk", locationName="Hub_None", protocol="SIP",
            securityProfileName="Non Secure SIP Trunk Profile", sipProfileName="Standard SIP Profile",
            presenceGroupName="Standard Presence Group", protocolSide="Network", **kwargs):
        if "class" not in kwargs:
            kwargs["class"] = "Trunk"
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipProfile(DeviceAXLAPI):
    _factory_descriptor = "sip_profile"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "options", "apply", "restart"]

    def add(self, name, sdpTransparency="Pass all unknown SDP attributes", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SipTrunkSecurityProfile(DeviceAXLAPI):
    _factory_descriptor = "sip_trunk_security_profile"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "reset"]

    def add(self, name, acceptPresenceSubscription=False, acceptOutOfDialogRefer=False,
            acceptUnsolicitedNotification=False, allowReplaceHeader=False, transmitSecurityStatus=False, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SoftKeyTemplate(DeviceAXLAPI):
    _factory_descriptor = "softkey_template"
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove", "apply", "restart"]

    def add(self, name, description,
            baseSoftkeyTemplateName="Standard User",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class SoftKeySet(SimpleAXLAPI):
    _factory_descriptor = "softkey_set"
    supported_methods = ["get", "update"]


class UniversalDeviceTemplate(SimpleAXLAPI):
    _factory_descriptor = "udt"

    def add(self, name, devicePool, directoryNumber=None, lineLabel=None, displayCallerId=None, callingSearchSpace=None,
            sipProfile="Standard SIP Profile", commonPhoneProfile="Standard Common Phone Profile",
            phoneButtonTemplate="Universal Device Template Button Layout",
            deviceSecurityProfile="Universal Device Template - Model-independent Security Profile",
            blfPresenceGroup="Standard Presence group", location="Hub_None", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class UniversalLineTemplate(SimpleAXLAPI):
    _factory_descriptor = "ult"

    def add(self, name, routePartition=None, lineDescription=None, callingSearchSpace=None, voiceMailProfile=None,
            alertingName=None, rejectAnonymousCall=False,  # override inconsistency between normal line add and ULT
            blfPresenceGroup="Standard Presence group", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class WifiHotspot(SimpleAXLAPI):
    _factory_descriptor = "wifi_hotspot"

    def add(self, name, ssidPrefix, frequencyBand="Auto", userModifiable="Allowed", authenticationMethod="None",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class WLANProfile(SimpleAXLAPI):
    _factory_descriptor = "wlan_profile"

    def add(self, name, ssid, frequencyBand="Auto", userModifiable="Allowed", authMethod="EAP-FAST",
            networkAccessProfile=None, userName="", password="", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class WlanProfileGroup(SimpleAXLAPI):
    _factory_descriptor = "wlan_profile_group"

    def add(self, name,
            members=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
