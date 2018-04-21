# -*- coding: utf-8 -*-
"""python-zeep client wrappers for Cisco UC SOAP APIs"""

import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
# import asyncio

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
# from zeep.asyncio import AsyncTransport
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.plugins import HistoryPlugin

from .exceptions import ServiceProxyError
from .model import axl_factory
from .definitions import WSDL_URLS
from .api import *


def get_connection_kwargs(env_dict, kwargs):
    """Get zeep client kwargs by consolidating environment variables and statically defined attributes.

    Note:
    Static parameters take precedence over env vars, if they exist.

    :param env_dict: dict mapping connection argument names to environment variable names
    :param kwargs: __init__ input args
    :return: kwargs with updated connection parameter values
    :raises UCToolkitConnectionException: if no connection parameters not provided
    """
    connection_kwargs = {k: os.environ.get(v) for k, v in env_dict.items()}
    connection_kwargs.update(kwargs)
    return connection_kwargs


class AXLHistoryPlugin(HistoryPlugin):

    @staticmethod
    def _parse_envelope(envelope):
        return etree.tostring(envelope, encoding="unicode", pretty_print=True)

    @property
    def last_sent(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return self._parse_envelope(last_tx['sent']['envelope'])

    @property
    def last_received(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return self._parse_envelope(last_tx['received']['envelope'])


class UCSOAPConnector(object):
    """Parent class for all Cisco UC SOAP Connectors"""

    def __init__(self, username=None,
                 password=None,
                 wsdl=None,
                 binding_name=None,
                 address=None,
                 tls_verify=False,
                 timeout=30,
                 is_async=False,
                 history=True,
                 history_maxlen=1):
        """Instantiate UC SOAP Client Connector

        :param username: SOAP client connector username
        :param password: SOAP client connector password
        :param wsdl: SOAP WSDL location
        :param binding_name: QName of the binding
        :param address: address of the endpoint
        :param tls_verify: /path/to/certificate.pem or False.  Certificate must be a CA_BUNDLE. Supports .pem and .crt
        :param is_async: create async client
        :param timeout: timeout in seconds.  Overrides zeep 300 default to timeout after 30sec
        """
        self._username = username
        self._wsdl = wsdl
        self._timeout = timeout
        # self.is_async = is_async

        self._session = Session()
        self._session.auth = HTTPBasicAuth(username, password)
        self._session.verify = tls_verify
        self._plugins = []

        if not self._session.verify:
            urllib3.disable_warnings(InsecureRequestWarning)

        if history:
            self._history = AXLHistoryPlugin(maxlen=history_maxlen)
            self._plugins.append(self._history)

        # todo - extend necessary support for async
        # if self.is_async:
        #     loop = asyncio.get_event_loop()
        #     transport = AsyncTransport(loop,
        #                                cache=SqliteCache(),
        #                                session=self._session,
        #                                timeout=self._timeout
        #                                )
        # else:
        transport = Transport(cache=SqliteCache(),
                              session=self._session,
                              timeout=self._timeout
                              )

        # self._client = Client(wsdl=wsdl, transport=transport)
        self._client = Client(wsdl=wsdl, transport=transport, plugins=self._plugins)
        if binding_name and address:
            # self._client = self._client.create_service(binding_name, address)
            self._service = self._client.create_service(binding_name, address)
        elif binding_name or address:
            raise ServiceProxyError(
                message="Incomplete parameters for ServiceProxy Object creation.  "
                        "Requires both 'binding_name' and 'address'"
            )
        else:
            # use first service and first port within that service - zeep default behaviour
            self._service = ServiceProxyError("ServiceProxy not used for this connector")

        self.model_factory = self._client.type_factory('ns0')

    @property
    def timeout(self):
        return self._timeout

    @property
    def wsdl(self):
        return self._wsdl

    @property
    def client(self):
        """Direct access to zeep client for wsdl inspection or advanced in-line client modification,
        factory building, etc."""
        return self._client

    @property
    def service(self):
        """Direct access to zeep service for method-calling of proxied services"""
        return self._service

    @property
    def history(self):
        return self._history


class UCMAXLConnector(UCSOAPConnector):
    _ENV = {
        "username": "AXL_USERNAME",
        "password": "AXL_PASSWORD",
        "fqdn": "AXL_FQDN",
        "wsdl": "AXL_WSDL_URL"
    }

    def __init__(self, **kwargs):
        connection_kwargs = get_connection_kwargs(self._ENV, kwargs)
        connection_kwargs["binding_name"] = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        connection_kwargs["address"] = "https://{fqdn}:8443/axl/".format(
            fqdn=connection_kwargs["fqdn"]
        )
        del connection_kwargs["fqdn"]  # remove fqdn as not used in super() call
        super().__init__(**connection_kwargs)

        # for api in API_ENDPOINTS.values():
        #     setattr(self, api.factory_descriptor, api(self, axl_factory))

        # sql API wrapper
        self.sql = ThinAXLAPI(self, axl_factory)

        # device API wrappers
        self.common_device_config = CommonDeviceConfig(self, axl_factory)
        self.common_phone_profile = CommonPhoneConfig(self, axl_factory)
        self.cti_route_point = CtiRoutePoint(self, axl_factory)
        self.feature_control_policy = FeatureControlPolicy(self, axl_factory)
        self.ip_phone_service = IpPhoneServices(self, axl_factory)
        self.line = Line(self, axl_factory)
        self.network_access_profile = NetworkAccessProfile(self, axl_factory)
        self.phone = Phone(self, axl_factory)
        self.default_device_profile = DefaultDeviceProfile(self, axl_factory)
        self.udp = DeviceProfile(self, axl_factory)
        self.phone_button_template = PhoneButtonTemplate(self, axl_factory)
        self.phone_security_profile = PhoneSecurityProfile(self, axl_factory)
        self.recording_profile = RecordingProfile(self, axl_factory)
        self.sip_trunk = SipTrunk(self, axl_factory)
        self.sip_trunk_security_profile = SipTrunkSecurityProfile(self, axl_factory)
        self.sip_profile = SipProfile(self, axl_factory)
        self.softkey_template = SoftKeyTemplate(self, axl_factory)
        self.softkey_set = SoftKeySet(self, axl_factory)
        self.udt = UniversalDeviceTemplate(self, axl_factory)
        self.ult = UniversalLineTemplate(self, axl_factory)
        self.remote_destination = RemoteDestination(self, axl_factory)
        self.rdp = RemoteDestinationProfile(self, axl_factory)
        self.wifi_hotspot = WifiHotspot(self, axl_factory)
        self.wlan_profile = WLANProfile(self, axl_factory)
        self.wlan_profile_group = WlanProfileGroup(self, axl_factory)

        # user API wrappers
        self.application_user = AppUser(self, axl_factory)
        self.feature_group_template = FeatureGroupTemplate(self, axl_factory)
        self.user = User(self, axl_factory)
        self.uc_service = UcService(self, axl_factory)
        self.service_profile = ServiceProfile(self, axl_factory)
        self.user_group = UserGroup(self, axl_factory)
        self.user_profile = UserProfileProvision(self, axl_factory)
        # self.quick_user_phone_add = _UserPhoneAssociationAPI(self, axl_factory)

        # dial plan API wrappers
        self.advertised_patterns = AdvertisedPatterns(self, axl_factory)
        self.aar_group = AarGroup(self, axl_factory)
        self.blocked_learned_patterns = BlockedLearnedPatterns(self, axl_factory)
        self.call_pickup_group = CallPickupGroup(self, axl_factory)
        self.call_park = CallPark(self, axl_factory)
        self.called_party_xform_pattern = CalledPartyTransformationPattern(self, axl_factory)
        self.calling_party_xform_pattern = CallingPartyTransformationPattern(self, axl_factory)
        self.conference_now = ConferenceNow(self, axl_factory)
        self.cmc = CmcInfo(self, axl_factory)
        self.css = Css(self, axl_factory)
        self.directed_call_park = DirectedCallPark(self, axl_factory)
        self.mobility_enterprise_feature_access_number = EnterpriseFeatureAccessConfiguration(self, axl_factory)
        self.fac = FacInfo(self, axl_factory)
        self.handoff_mobility = Mobility(self, axl_factory)
        self.meetme = MeetMe(self, axl_factory)
        self.mobility_profile = MobilityProfile(self, axl_factory)
        self.hunt_list = HuntList(self, axl_factory)
        self.hunt_pilot = HuntPilot(self, axl_factory)
        self.line_group = LineGroup(self, axl_factory)
        self.local_route_group = LocalRouteGroup(self, axl_factory)
        self.route_group = RouteGroup(self, axl_factory)
        self.route_list = RouteList(self, axl_factory)
        self.route_partition = RoutePartition(self, axl_factory)
        self.route_pattern = RoutePattern(self, axl_factory)
        self.sip_dial_rules = SipDialRules(self, axl_factory)
        self.sip_realm = SipRealm(self, axl_factory)
        self.sip_route_pattern = SipRoutePattern(self, axl_factory)
        self.time_period = TimePeriod(self, axl_factory)
        self.time_schedule = TimeSchedule(self, axl_factory)
        self.translation_pattern = TransPattern(self, axl_factory)

        # system API wrappers
        self.audio_codec_preference_list = AudioCodecPreferenceList(self, axl_factory)
        self.callmanager_group = CallManagerGroup(self, axl_factory)
        self.date_time_group = DateTimeGroup(self, axl_factory)
        self.device_mobility_group = DeviceMobilityGroup(self, axl_factory)
        self.device_mobility_info = DeviceMobility(self, axl_factory)
        self.device_pool = DevicePool(self, axl_factory)
        self.ldap_directory = LdapDirectory(self, axl_factory)
        self.ldap_filter = LdapFilter(self, axl_factory)
        self.ldap_sync_custom_field = LdapSyncCustomField(self, axl_factory)
        self.lbm_group = LbmGroup(self, axl_factory)
        self.lbm_hub_group = LbmHubGroup(self, axl_factory)
        self.location = Location(self, axl_factory)
        self.presence_redundancy_group = PresenceRedundancyGroup(self, axl_factory)
        self.phone_ntp_reference = PhoneNtp(self, axl_factory)
        self.physical_location = PhysicalLocation(self, axl_factory)
        self.presence_group = PresenceGroup(self, axl_factory)
        self.region = Region(self, axl_factory)
        self.srst = Srst(self, axl_factory)

        # media API wrappers
        self.conference_bridge = ConferenceBridge(self, axl_factory)
        self.mrg = MediaResourceGroup(self, axl_factory)
        self.mrgl = MediaResourceList(self, axl_factory)
        self.mtp = Mtp(self, axl_factory)
        self.transcoder = Transcoder(self, axl_factory)
        self.voh_server = VohServer(self, axl_factory)

        # advanced API wrappers
        self.remote_cluster = RemoteCluster(self, axl_factory)
        self.voicemail_pilot = VoiceMailPilot(self, axl_factory)
        self.voicemail_profile = VoiceMailProfile(self, axl_factory)
        self.vpn_gateway = VpnGateway(self, axl_factory)
        self.vpn_group = VpnGroup(self, axl_factory)
        self.vpn_profile = VpnProfile(self, axl_factory)

        # serviceability API wrappers
        self.billing_server = BillingServer(self, axl_factory)
        self.snmp_community_string = SNMPCommunityString(self, axl_factory)
        self.snmp_user = SNMPUser(self, axl_factory)


class UCMControlCenterConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=True):
        _wsdl = WSDL_URLS["ControlCenterServicesExtended"].format(fqdn)
        super().__init__(username=username,
                         password=password,
                         wsdl=_wsdl,
                         tls_verify=tls_verify)

    def get_service_status(self, services=None):
        # check this comment on factory creation:
        # https://github.com/mvantellingen/python-zeep/issues/145#issuecomment-261509531

        # if not services:
        #     return self.service.soapGetServiceStatus()
        # else:
        #     return self.service.soapGetServiceStatus(services)
        raise NotImplementedError()

    def do_service_deployment(self):
        # todo
        # return self.service.soapDoServiceDeployment()
        raise NotImplementedError()

    def get_product_information_list(self):
        # todo
        # return self.service.getProductInformationList()
        raise NotImplementedError()


class UCMRisPortConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=False):
        _wsdl = WSDL_URLS["RisPort70"].format(fqdn)
        _binding_name = "{http://schemas.cisco.com/ast/soap}RisBinding"
        _address = "https://{fqdn}:8443/realtimeservice2/services/RISService70".format(fqdn=fqdn)
        super().__init__(username=username,
                         password=password,
                         wsdl=_wsdl,
                         binding_name=_binding_name,
                         address=_address,
                         tls_verify=tls_verify)

    def select_cm_device(self, state_info=None, **cm_selection_criteria):
        # device_class = "Any",
        # status = "Any",
        # max_devices = 1000,
        # model = 255,
        # selection_type = None,
        # node_name = None
        #
        _max_devices = 1000  # assume CUCM 9.1 and above only
        _all_models = 255  # returns all models

        # return self.service.selectCmDevice(state_info, {"CmSelectionCriteria": cm_selection_criteria})
        raise NotImplementedError()

    def select_cm_device_ext(self):
        # return self.service.SelectCmDeviceExt
        raise NotImplementedError()

    def select_cti_item(self):
        # return self.service.selectCtiItem
        raise NotImplementedError()

    def select_cm_device_sip(self):
        # return self.service.SelectCmDeviceSIP
        raise NotImplementedError()


class UCMPerfMonConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=False):
        _wsdl = WSDL_URLS["PerfMon"].format(fqdn)
        _binding_name = "{http://schemas.cisco.com/ast/soap}PerfmonBinding"
        _address = "https://{fqdn}:8443/perfmonservice2/services/PerfmonService".format(fqdn=fqdn)
        super().__init__(username=username,
                         password=password,
                         wsdl=_wsdl,
                         binding_name=_binding_name,
                         address=_address,
                         tls_verify=tls_verify)

    def open_session(self):
        # todo
        # return self.service.perfmonOpenSession()
        raise NotImplementedError()

    def add_counter(self, session_handle, counters):
        """
        :param session_handle: A session Handle returned from perfmonOpenSession()
        :param counters: An array of counters or a single string for a single counter
        :return: True for Success and False for Failure
        """
        # todo - fix unreferenced counter_data var
        if isinstance(counters, list):
            counter_data = [
                {
                    'Counter': []
                }
            ]

            for counter in counters:
                new_counter = {
                    'Name': counter
                }
                counter_data['Counter'].append(new_counter)

        elif counters is not None:
            counter_data = [
                {
                    'Counter': [
                        {
                            'Name': counters
                        }
                    ]
                }
            ]

        try:
            self.service.perfmonAddCounter(SessionHandle=session_handle, ArrayOfCounter=counter_data)
            result = True
        # todo - fix except - bubble to the top with custom exception?
        except:
            result = False

        # return result
        raise NotImplementedError()

    def remove_counter(self):
        # todo
        # return self.service.perfmonRemoveCounter()
        raise NotImplementedError()

    def collect_session_data(self, session_handle):
        # todo
        # return self.service.perfmonCollectSessionData(SessionHandle=session_handle)
        raise NotImplementedError()

    def close_session(self):
        # todo
        # return self.service.perfmonCloseSession()
        raise NotImplementedError()

    def list_instance(self):
        # todo
        # return self.service.perfmonListInstance()
        raise NotImplementedError()

    def query_counter_description(self):
        # todo
        # return self.service.perfmonQueryCounterDescription()
        raise NotImplementedError()

    def list_counter(self):
        # todo
        # return self.service.perfmonListCounter()
        raise NotImplementedError()

    def collect_counter_data(self):
        # todo
        # return self.service.perfmonCollectCounterData()
        raise NotImplementedError()


class UCMLogCollectionConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=False):
        _wsdl = WSDL_URLS["LogCollection"].format(fqdn)
        super().__init__(username=username,
                         password=password,
                         wsdl=_wsdl,
                         tls_verify=tls_verify)
