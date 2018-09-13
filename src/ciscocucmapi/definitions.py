# -*- coding: utf-8 -*-
"""AXL definitions"""

import inspect
import os
import pathlib

import ciscocucmapi.api


__all__ = [
    "PACKAGE_ROOT_PATH",
    "WSDL_URLS", "WSDL_PATH",
    "AXL_API_ENDPOINTS", "AXL_BINDING_NAME", "AXL_ADDRESS",
    "RISPORT_BINDING_NAME", "RISPORT_ADDRESS",
    "PERFMON_BINDING_NAME", "PERFMON_ADDRESS",
]

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PACKAGE_ROOT_PATH = pathlib.Path(_ROOT_DIR)
WSDL_PATH = PACKAGE_ROOT_PATH.parents[1] / "schema"


WSDL_URLS = {
    "RisPort70": "https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl",
    "CDRonDemand": "https://{fqdn}:8443/realtimeservice2/services/CDRonDemandService?wsdl",
    "PerfMon": "https://{fqdn}:8443/perfmonservice2/services/PerfmonService?wsdl",
    "ControlCenterServices": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServices?wsdl",
    "ControlCenterServicesExtended": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServicesEx?wsdl",
    "LogCollection": "https://{fqdn}:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl",
    "DimeGetFileService": "https://{fqdn}:8443/logcollectionservice/services/DimeGetFileService?wsdl"
}

AXL_API_ENDPOINTS = {m[0]: m[1] for m in inspect.getmembers(ciscocucmapi.api, inspect.isclass)}
AXL_BINDING_NAME = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
AXL_ADDRESS = "https://{fqdn}:8443/axl/"

RISPORT_BINDING_NAME = "{http://schemas.cisco.com/ast/soap}RisBinding"
RISPORT_ADDRESS = "https://{fqdn}:8443/realtimeservice2/services/RISService70"
RISPORT = {
    "type": (
        "Name",
        "IPV4Address",
        "DirNumber",
        "Description",
        "SIPStatus"
    ),
    "class": (
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
    ),
    "status": (
        'Any',
        'Registered',
        'UnRegistered',
        'Rejected',
        'Unknown'
    ),
    "max_devices": {
        "v9": 1000,
        "default": 1000
    },
    "all_models": 255
}

PERFMON_BINDING_NAME = "{http://schemas.cisco.com/ast/soap}PerfmonBinding"
PERFMON_ADDRESS = "https://{fqdn}:8443/perfmonservice2/services/PerfmonService"
