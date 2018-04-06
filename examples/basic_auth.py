# -*- coding: utf-8 -*-

from uctoolkit import UCMAXLConnector

# explicit auth creden
USERNAME = 'administrator'
PASSWORD = 'ciscopsdt'
FQDN = "10.10.20.1"
WSDL = 'file://C://Users//jonathan.els//develop//pvt-repos//UCToolkit//schema//current//AXLAPI.wsdl'


def main():
    axl = UCMAXLConnector(username=USERNAME, password=PASSWORD, fqdn=FQDN, wsdl=WSDL)
    bot_device_name = "BOTUSER015"
    botuser15 = axl.phones.get(name=bot_device_name)
    print(botuser15.callingSearchSpaceName)


if __name__ == '__main__':
    main()
