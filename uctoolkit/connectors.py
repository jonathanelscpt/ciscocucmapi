# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import asyncio

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.asyncio import AsyncTransport
from requests import Session
from requests.auth import HTTPBasicAuth

from .exceptions import (
    ServiceProxyError,
    UCToolkitConnectionException
)
from .model import axl_factory
from .api import (
    ThinAXL as _ThinAXLAPI,
    Phone as _PhoneAPI,
    Line as _LineAPI,
    RoutePartition as _RoutePartitionAPI,
    CallPickupGroup as _CallPickupGroupAPI,
    User as _UserAPI
)

WSDL_URLS = {
    "RisPort70": "https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl",
    "CDRonDemand": "https://{fqdn}:8443/realtimeservice2/services/CDRonDemandService?wsdl",
    "PerfMon": "https://{fqdn}:8443/perfmonservice2/services/PerfmonService?wsdl",
    "ControlCenterServices": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServices?wsdl",
    "ControlCenterServicesExtended": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServicesEx?wsdl",
    "LogCollection": "https://{fqdn}:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl",
    "DimeGetFileService": "https://{fqdn}:8443/logcollectionservice/services/DimeGetFileService?wsdl"
}


def get_connection_kwargs(env_dict, kwargs):
    """Update connection kwargs with environment variable values.
    Env parameters take precedence if they exist.

    :param env_dict: dict mapping connection argument names to environment variable names
    :param kwargs: __init__ input args
    :return: kwargs with updated connection parameter values
    :raises UCToolkitConnectionException: if no connection parameters not provided
    """
    connection_kwargs = {k: os.environ.get(v) for k, v in env_dict.items()}
    try:
        # we need to consolidate the env vars with what was provided during __init__
        # we let env vars take precedence if they exist
        init_kwargs = {k: kwargs[v] for k, v in env_dict.items() if connection_kwargs[k] is None}
        connection_kwargs.update(init_kwargs)
        return connection_kwargs
    except KeyError:
        raise UCToolkitConnectionException(
            "All connection parameters must be provided, either via environment variables"
            " or as explicit keyword arguments: {connection_params}".format(
                connection_params=list(env_dict.keys()))
        )


class UCSOAPConnector:
    """
    Parent class for all Cisco UC SOAP Connectors
    """
    def __init__(self, username=None,
                 password=None,
                 wsdl=None,
                 binding_name=None,
                 address=None,
                 tls_verify=False,
                 timeout=30,
                 is_async=False):
        """
        Instantiate UC SOAP Client Connector

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
        self.is_async = is_async

        self._session = Session()
        self._session.auth = HTTPBasicAuth(username, password)
        self._session.verify = tls_verify

        if not self._session.verify:
            urllib3.disable_warnings(InsecureRequestWarning)

        # todo - extend necessary support for async
        if self.is_async:
            loop = asyncio.get_event_loop()
            transport = AsyncTransport(loop,
                                       cache=SqliteCache(),
                                       session=self._session,
                                       timeout=self._timeout
                                       )
        else:
            transport = Transport(cache=SqliteCache(),
                                  session=self._session,
                                  timeout=self._timeout
                                  )

        self._client = Client(wsdl=wsdl, transport=transport)

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

        self._model_factory = self._client.type_factory('ns0')

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
    def model_factory(self):
        """zeep factory for global wsdl namespace"""
        return self._model_factory


class UCMAXLConnector (UCSOAPConnector):

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

        UCSOAPConnector.__init__(self, **connection_kwargs)

        # device API wrappers
        self.sql = _ThinAXLAPI(self, axl_factory)
        self.phones = _PhoneAPI(self, axl_factory)
        self.lines = _LineAPI(self, axl_factory)

        # user API wrappers
        self.users = _UserAPI(self, axl_factory)

        # dial plan API wrappers
        self.route_partitions = _RoutePartitionAPI(self, axl_factory)
        self.call_pickup_groups = _CallPickupGroupAPI(self, axl_factory)


class UCMControlCenterConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=True):
        _wsdl = WSDL_URLS["ControlCenterServicesExtended"].format(fqdn)
        UCSOAPConnector.__init__(self,
                                 username=username,
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
        UCSOAPConnector.__init__(self,
                                 username=username,
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
        _selection_types = [
            "Name",
            "IPV4Address",
            "DirNumber",
            "Description",
            "SIPStatus"
        ]
        _device_classes = [
            'Any',
            'Phone',
            'Gateway',
            'H323',
            'Cti',
            'VoiceMail',
            'MediaResources',
            'HuntList',
            'SIPTrunk',
            'unknown'
        ]
        _device_statuses = [
            'Any',
            'Registered',
            'UnRegistered',
            'Rejected',
            'Unknown'
        ]

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


class UCMPerMonConnector(UCSOAPConnector):

    def __init__(self, username, password, fqdn, tls_verify=False):
        _wsdl = WSDL_URLS["PerfMon"].format(fqdn)
        _binding_name = "{http://schemas.cisco.com/ast/soap}PerfmonBinding"
        _address = "https://{fqdn}:8443/perfmonservice2/services/PerfmonService".format(fqdn=fqdn)
        UCSOAPConnector.__init__(self,
                                 username=username,
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
        UCSOAPConnector.__init__(self,
                                 username=username,
                                 password=password,
                                 wsdl=_wsdl,
                                 tls_verify=tls_verify)

