"""AXL definitions"""


WSDL_URLS = {
    "RisPort70": "https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl",
    "CDRonDemand": "https://{fqdn}:8443/realtimeservice2/services/CDRonDemandService?wsdl",
    "PerfMon": "https://{fqdn}:8443/perfmonservice2/services/PerfmonService?wsdl",
    "ControlCenterServices": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServices?wsdl",
    "ControlCenterServicesExtended": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServicesEx?wsdl",
    "LogCollection": "https://{fqdn}:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl",
    "DimeGetFileService": "https://{fqdn}:8443/logcollectionservice/services/DimeGetFileService?wsdl"
}

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
