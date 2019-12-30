"""CUCM System Configuration APIs."""

from datetime import datetime
from datetime import timedelta

from zeep.helpers import serialize_object

from .._internal_utils import flatten_signature_kwargs
from .._internal_utils import get_signature_locals
from .._internal_utils import nullstring_dict
from ..helpers import get_model_dict
from .base import DeviceAXLAPI
from .base import SimpleAXLAPI


class ApplicationServer(SimpleAXLAPI):
    _factory_descriptor = "application_server"

    def add(self, name, appServerType, ipAddress=None, appUsers=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class AppServerInfo(SimpleAXLAPI):
    _factory_descriptor = "application_server_info"
    supported_methods = ["model", "create", "add", "get", "update", "remove"]

    def add(self, appServerName, appServerContent, content=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class AudioCodecPreferenceList(SimpleAXLAPI):
    _factory_descriptor = "audio_codec_preference_list"

    def add(self, name, description, codecsInList, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class CallManager(DeviceAXLAPI):
    _factory_descriptor = "callmanager"
    supported_methods = ["get", "list", "update", "apply", "restart", "reset"]


class CallManagerGroup(DeviceAXLAPI):
    _factory_descriptor = "callmanager_group"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DateTimeGroup(DeviceAXLAPI):
    _factory_descriptor = "date_time_group"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, timeZone, separator="-", dateformat="M-D-Y", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceMobilityGroup(SimpleAXLAPI):
    _factory_descriptor = "device_mobility_group"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DeviceMobility(SimpleAXLAPI):
    _factory_descriptor = "device_mobility_info"

    def add(self, name, subNet, subNetMaskSz, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DevicePool(DeviceAXLAPI):
    _factory_descriptor = "device_pool"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, callManagerGroupName, dateTimeSettingName, regionName, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class DhcpServer(SimpleAXLAPI):
    _factory_descriptor = "dhcp_server"

    def add(self, processNodeName, primaryTftpServerIpAddress=None, secondaryTftpServerIpAddress=None,
            primaryDnsIpAddress=None, secondaryDnsIpAddress=None, domainName=None, arpCacheTimeout=0,
            ipAddressLeaseTime=0, renewalTime=0, rebindingTime=0, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class EnterprisePhoneConfig(SimpleAXLAPI):
    _factory_descriptor = "enterprise_phone_config"
    supported_methods = ["get", "update"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._get_model_name = "XEnterprisePhoneConfig"

    def get(self):
        axl_resp = self.connector.service.getEnterprisePhoneConfig()
        return serialize_object(axl_resp)["return"][self._return_name]


class DhcpSubnet(SimpleAXLAPI):
    _factory_descriptor = "dhcp_subnet"

    def add(self, dhcpServerName, primaryStartIpAddress, primaryEndIpAddress, subnetIpAddress, subnetMask,
            primaryRouterIpAddress,  # making this mandatory for sanity-sake
            primaryTftpServerIpAddress=None, secondaryTftpServerIpAddress=None, primaryDnsIpAddress=None,
            secondaryDnsIpAddress=None, domainName=None, arpCacheTimeout=0, ipAddressLeaseTime=0, renewalTime=0,
            rebindingTime=0, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LdapAuthentication(SimpleAXLAPI):
    _factory_descriptor = "ldap_authentication"
    supported_methods = ["get", "update"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._get_model_name = "XLdapAuthentication"

    def get(self):
        axl_resp = self.connector.service.getLdapAuthentication()
        return serialize_object(axl_resp)["return"][self._return_name]


class LdapDirectory(SimpleAXLAPI):
    _factory_descriptor = "ldap_directory"
    supported_methods = [
        "model", "create", "add", "get", "update", "list", "remove",
        "sync", "get_sync_status",
    ]

    def add(self, name, ldapDn, ldapPassword, userSearchBase, servers, intervalValue=7, scheduleUnit="DAY",
            nextExecTime=None, **kwargs):
        if not nextExecTime:
            nextExecTime = (datetime.now() + timedelta(days=intervalValue + 1)).strftime("%y-%m-%d 00:00")
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)

    def sync(self, name=None, uuid=None, sync=True):
        kwargs = get_signature_locals(self.get_sync_status, locals())
        axl_resp = self.connector.service.doLdapSync(**kwargs)
        return serialize_object(axl_resp)["return"]

    def get_sync_status(self, name=None, uuid=None):
        kwargs = get_signature_locals(self.get_sync_status, locals())
        axl_resp = self.connector.service.getLdapSyncStatus(**kwargs)
        return serialize_object(axl_resp)["return"]


class LdapFilter(SimpleAXLAPI):
    _factory_descriptor = "ldap_filter"

    def add(self, name, filter, **kwargs):  # shadow not used
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LdapSearch(SimpleAXLAPI):
    _factory_descriptor = "ldap_search"
    supported_methods = ["get", "list", "update"]


# issue - not working!
class LdapSyncCustomField(SimpleAXLAPI):
    _factory_descriptor = "ldap_custom_field"

    def add(self, ldapConfigurationName, customUserField, ldapUserField, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LdapSystem(SimpleAXLAPI):
    _factory_descriptor = "ldap_system"
    supported_methods = ["get", "update"]

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._get_model_name = "XLdapSystem"

    def get(self):
        axl_resp = self.connector.service.getLdapSystem()
        return serialize_object(axl_resp)["return"][self._return_name]

    def update(self, syncEnabled=True, ldapServer="Microsoft Active Directory", userIdAttribute="sAMAccountName"):
        return super().update(syncEnabled=syncEnabled, ldapServer=ldapServer, userIdAttribute=userIdAttribute)


class LbmGroup(SimpleAXLAPI):
    _factory_descriptor = "lbm_group"

    def add(self, name, ProcessnodeActive, ProcessnodeStandby=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class LbmHubGroup(SimpleAXLAPI):
    _factory_descriptor = "lbm_hub_group"

    def add(self, name, member1,
            member2=None,
            member3=None,
            members=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Location(SimpleAXLAPI):
    _factory_descriptor = "location"

    def add(self, name,
            betweenLocations=None,
            **kwargs):
        # this approach is probably not compatible with pre-9's flattened locations.
        # if warranted in future, would require extension for a version check.
        if not betweenLocations:
            betweenLocations = {
                "betweenLocation": {
                    "locationName": "Hub_None",
                    "audioBandwidth": 0,  # translates to 'UNLIMITED'
                    "videoBandwidth": 384,  # investigate default?
                    "immersiveBandwidth": 384,
                    "weight": 50
                }
            }
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PresenceRedundancyGroup(SimpleAXLAPI):
    _factory_descriptor = "presence_redundancy_group"

    def add(self, name, server1, server2=None, haEnabled=False, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhoneNtp(SimpleAXLAPI):
    _factory_descriptor = "phone_ntp_reference"

    def add(self, ipAddress, mode="Directed Broadcast", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PhysicalLocation(SimpleAXLAPI):
    _factory_descriptor = "physical_location"

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class PresenceGroup(SimpleAXLAPI):
    _factory_descriptor = "presence_group"

    def add(self, name, presenceGroups=None, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class ProcessNode(SimpleAXLAPI):
    _factory_descriptor = "process_node"

    def add(self, name,
            processNodeRole="CUCM Voice/Video"):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Region(DeviceAXLAPI):
    _factory_descriptor = "region"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "restart"]

    def add(self, name, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class ServiceParameter(SimpleAXLAPI):
    _factory_descriptor = "service_parameter"
    supported_methods = ["get", "list", "update", "reset_all"]

    def reset_all(self, processNodeName, service):
        axl_resp = self.connector.service.doServiceParametersReset(processNodeName=processNodeName, service=service)
        return serialize_object(axl_resp)["return"]


class EnterpriseParameter(ServiceParameter):
    _factory_descriptor = "enterprise_parameter"

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        self._return_name = "serviceParameter"
        self._get_method_name = "GetServiceParameterReq"
        self._get_model_name = "RServiceParameter"
        self._list_method_name = "ListServiceParameterReq"
        self._list_model_name = "LServiceParameter"

    def get(self, returnedTags=None, **kwargs):
        if "uuid" not in kwargs and "processNodeName" not in kwargs and "service" not in kwargs:
            kwargs["processNodeName"] = "EnterpriseWideData"
            kwargs["service"] = "Enterprise Wide"
        if isinstance(returnedTags, list):
            returnedTags = nullstring_dict(returnedTags)
        get_kwargs = flatten_signature_kwargs(self.get, locals())
        axl_resp = self.connector.service.getServiceParameter(**get_kwargs)
        return serialize_object(axl_resp)["return"][self._return_name]

    def list(self, searchCriteria=None, returnedTags=None, skip=None, first=None):
        # todo - warrants rework in base class
        if not searchCriteria:
            searchCriteria = {
                "processNodeName": "EnterpriseWideData",
                "service": "Enterprise Wide"
            }
        if not returnedTags:
            list_model = self._get_wsdl_obj(self._list_model_name)
            returnedTags = get_model_dict(list_model)
        elif isinstance(returnedTags, list):
            returnedTags = nullstring_dict(returnedTags)
        axl_resp = self.connector.service.listServiceParameter(searchCriteria=searchCriteria,
                                                               returnedTags=returnedTags,
                                                               skip=skip,
                                                               first=first)
        try:
            axl_list = serialize_object(axl_resp)["return"][self._return_name]
            return [self.object_factory(self.__class__.__name__, item) for item in axl_list]
        except TypeError:
            return []

    def reset_all(self):
        # todo - this violates LSP due to invalid method signature.  a case for class re-design
        axl_resp = self.connector.service.doEnterpriseParametersReset()
        return serialize_object(axl_resp)["return"]


class Srst(DeviceAXLAPI):
    _factory_descriptor = "srst"

    def add(self, name, ipAddress, SipNetwork=None, **kwargs):
        # there are corner cases, but this is a good for optimized usability
        if not SipNetwork:
            SipNetwork = ipAddress
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
