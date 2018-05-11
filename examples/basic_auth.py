# -*- coding: utf-8 -*-

from uctoolkit import UCMAXLConnector

# explicit auth credentials
USERNAME = 'administrator'
PASSWORD = 'ciscopsdt'
FQDN = "10.10.20.1"
WSDL = 'file://C://path//to//AXLAPI.wsdl'


def main():
    axl = UCMAXLConnector(username=USERNAME, password=PASSWORD, fqdn=FQDN, wsdl=WSDL)
    botuser15 = axl.phone.get(name="BOTUSER015")
    print(botuser15.callingSearchSpaceName)


if __name__ == '__main__':
    main()
