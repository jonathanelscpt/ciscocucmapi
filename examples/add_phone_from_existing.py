# -*- coding: utf-8 -*-

from uctoolkit import UCMAXLConnector
from zeep.exceptions import Fault


def main():
    phone_defaults = {
        "product": "Cisco 8841",
        "protocol": "SIP",
        "securityProfileName": "Cisco 8841 - Standard SIP Non-Secure Profile",
        "loadInformation": None
    }
    phone_lines = [
        {
            "index": 1,
            "dirn": {
                "pattern": 4001,
                "routePartitionName": "Phones_Pt",
            }
        },
        {
            "index": 2,
            "dirn": {
                "pattern": 4002,
                "routePartitionName": "Phones_Pt",
            }
        }
    ]
    axl = UCMAXLConnector()
    try:
        cucm_phone = axl.phone.get(name="SEP111111111111")
        cucm_phone.name = "SEPFEEDFEEDFEED"
        cucm_phone.update(phone_defaults)
        cucm_phone.lines['line'] = phone_lines
        axl.phone.add(**cucm_phone.filter(axl.phone.model()))
    except Fault:
        print(axl.history.last_sent_xml)
        print(axl.history.last_received_xml)


if __name__ == '__main__':
    main()
