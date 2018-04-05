# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .exceptions import (
    ServiceProxyCreationError,
    UCToolkitConnectionException
)
from .model import axl_factory

from .api.device import Phone as _PhoneAPI
from .api.sql import ThinAXL as _ThinAXLAPI
# from .api.lines import LinesAPI as _LinesAPI
# from .api.users import UsersAPI as _UsersAPI

from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth

import os
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import logging.config
import logging


urllib3.disable_warnings(InsecureRequestWarning)

WSDL_URLS = {
    "RisPort70": "https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl",
    "CDRonDemand": "https://{fqdn}:8443/realtimeservice2/services/CDRonDemandService?wsdl",
    "PerfMon": "https://{fqdn}:8443/perfmonservice2/services/PerfmonService?wsdl",
    "ControlCenterServices": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServices?wsdl",
    "ControlCenterServicesExtended": "https://{fqdn}:8443/controlcenterservice2/services/ControlCenterServicesEx?wsdl",
    "LogCollection": "https://{fqdn}:8443/logcollectionservice2/services/LogCollectionPortTypeService?wsdl",
    "DimeGetFileService": "https://{fqdn}:8443/logcollectionservice/services/DimeGetFileService?wsdl"
}


def enable_logging():
    # default suggested zeep loggers
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'zeep.transports': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': ['console'],
            },
        }
    })


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
                 timeout=30):
        """
        Instantiate UC SOAP Client Connector

        :param username: SOAP client connector username
        :param password: SOAP client connector password
        :param wsdl: SOAP WSDL location
        :param binding_name: QName of the binding
        :param address: address of the endpoint
        :param tls_verify: /path/to/certificate.pem or False.  Certificate must be a CA_BUNDLE. Supports .pem and .crt
        :param timeout: timeout in seconds.  Overrides zeep 300 default to timeout after 30sec
        """
        self._username = username
        self._wsdl = wsdl
        self._timeout = timeout

        self._session = Session()
        self._session.auth = HTTPBasicAuth(username, password)
        self._session.verify = tls_verify
        transport = Transport(cache=SqliteCache(), session=self._session, timeout=self._timeout)
        self._client = Client(wsdl=wsdl, transport=transport)

        if binding_name and address:
            # create ServiceProxy from custom binding and address
            self._client = self._client.create_service(binding_name, address)
        elif binding_name or address:
            raise ServiceProxyCreationError(
                message="Incomplete parameters for ServiceProxy Object creation.  "
                        "Requires 'binding_name' and 'address'"
            )
        else:
            # use first service and first port within that service - zeep default behaviour
            self.service = self._client.service

    @property
    def timeout(self):
        return self._timeout

    @property
    def wsdl(self):
        return self._wsdl


class UCMAXLConnector (UCSOAPConnector):

    ENV = {
        "username": "AXL_USERNAME",
        "password": "AXL_PASSWORD",
        "fqdn": "AXL_WSDL_URL",
        "wsdl": "AXL_FQDN",
        # "timeout": "AXL_TIMEOUT"
    }

    def __init__(self, **kwargs):

        connection_kwargs = get_connection_kwargs(self.ENV, kwargs)
        connection_kwargs["binding_name"] = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        connection_kwargs["address"] = "https://{0}:8443/axl/".format(connection_kwargs["fqdn"])
        del connection_kwargs["fqdn"]  # not used in super() call
        UCSOAPConnector.__init__(self, **connection_kwargs)

        # AXL API Wrappers
        self.sql = _ThinAXLAPI(self._client, axl_factory)
        self.phones = _PhoneAPI(self._client, axl_factory)
        # self.users = _UsersAPI(self._client, axl_factory)
        # self.lines = _LinesAPI(self._client, axl_factory)

    """Thin AXL (SQL Queries / Updates)"""

    def execute_sql_query(self, query):
        result = {'num_rows': 0,
                  'query': query}

        try:
            sql_result = self.service.executeSQLQuery(sql=query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        num_rows = 0
        result_rows = []

        if sql_result is not None:
            if sql_result['return'] is not None:
                for row in sql_result['return']['row']:
                    result_rows.append({})
                    for column in row:
                        result_rows[num_rows][column.tag] = column.text
                    num_rows += 1

        result['num_rows'] = num_rows
        if num_rows > 0:
            result['rows'] = result_rows

        return result

    def execute_sql_update(self, query):
        result = {'rows_updated': 0,
                  'query': query}

        try:
            sql_result = self.service.executeSQLUpdate(sql=query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        if sql_result is not None:
            if sql_result['return'] is not None:
                result['rows_updated'] = sql_result['return']['rowsUpdated']

        return result

    """UCM Group"""

    def get_ucm_group(self, name):
        try:
            result = self.service.getCallManagerGroup(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_ucm_group_members(self, name, members):

        member_data = []
        member_count = 0

        for member in members:
            member_count += 1
            member_data.append({'priority': member_count, 'callManagerName': member})

        try:
            result = self.service.updateCallManagerGroup(name=name, members={'member': member_data})
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_ucm_group(self, name, members):

        member_data = []
        member_count = 0

        for member in members:
            member_count += 1
            member_data.append({'priority': member_count, 'callManagerName': member})

        try:
            result = self.service.addCallManagerGroup(callManagerGroup=
                                                      {'name': name, 'members':{'member': member_data}})
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_ucm_group(self, name):
        try:
            result = self.service.removeCallManagerGroup(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Users"""

    def get_user(self, userid):
        try:
            result = self.service.getUser(userid=userid)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def list_users(self, **kwargs):

        allowed_tags = ['firstName', 'lastName', 'userid', 'department']
        search_criteria = {}
        users = {}

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if key in allowed_tags:
                    search_criteria[key] = value

        if len(search_criteria) == 0:
            search_criteria['userid'] = '%'

        returned_tags = {'firstName': '', 'lastName': '', 'userid': ''}

        try:
            result = self.service.listUser(searchCriteria=search_criteria, returnedTags=returned_tags)

            if result['return'] is not None:

                for user in result['return']['user']:

                    users[user['userid']] = {}

                    users[user['userid']]['uuid'] = user['uuid']
                    users[user['userid']]['firstName'] = user['firstName']
                    users[user['userid']]['lastName'] = user['lastName']
                    users[user['userid']]['userid'] = user['userid']

        except Exception as fault:
            users = None
            self.last_exception = fault

        return users

    def update_user(self, user_data):
        try:
            result = self.service.updateUser(**user_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def sql_get_device_pkid(self, device):

        sql_query = "select pkid from device where name = '{0}'".format(device)

        result = self.run_sql_query(sql_query)

        if result['num_rows'] > 0:
            pkid = result['rows'][0]['pkid']
        else:
            pkid = None

        return pkid

    def sql_get_user_group_pkid(self, group_name):

        sql_query = "select pkid from dirgroup where name = '{0}'".format(group_name)

        result = self.run_sql_query(sql_query)

        if result['num_rows'] > 0:
            pkid = result['rows'][0]['pkid']
        else:
            pkid = None

        return pkid

    def sql_get_enduser_pkid(self, userid):

        sql_query = "select pkid from enduser where userid = '{0}'".format(userid)

        result = self.run_sql_query(sql_query)

        if result['num_rows'] > 0:
            pkid = result['rows'][0]['pkid']
        else:
            pkid = None

        return pkid

    def sql_associate_user_to_group(self, userid, group_name):

        user_group_pkid = self.sql_get_user_group_pkid(group_name)
        enduser_pkid = self.sql_get_enduser_pkid(userid)

        if user_group_pkid is not None and enduser_pkid is not None:
            query = "insert into enduserdirgroupmap (fkenduser, fkdirgroup) values ('{0}', '{1}')".format(enduser_pkid,
                                                                                                      user_group_pkid)

            sql_result = self.run_sql_update(query)

            if sql_result['rows_updated'] > 0:
                result = True
            else:
                result = False

            return result

    def sql_remove_user_from_group(self, userid, group_name):
        pass
        # TODO: Need to add this code

    """Lines"""

    def get_line(self, dn, partition):
        try:
            result = self.service.getLine(pattern=dn, routePartitionName=partition)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_line(self, line_data):
        try:
            result = self.service.addLine(line=line_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_line(self, line_data):
        try:
            result = self.service.updateLine(**line_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """LDAP Filter"""

    def get_ldap_filter(self, name):
        try:
            result = self.service.getLdapFilter(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_ldap_filter(self, name, filter_name):

        filter_data = {
            'name': name,
            'filter': filter_name
        }

        try:
            result = self.service.addLdapFilter(filter_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_ldap_filter(self, name):
        try:
            result = self.service.removeLdapFilter(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """LDAP Directory"""

    def get_ldap_directory(self, name):
        try:
            result = self.service.getLdapDirectory(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_ldap_directory(self, ldap_dir_data):

        try:
            result = self.service.addLdapDirectory(ldapDirectory=ldap_dir_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_ldap_directory(self, name):
        try:
            result = self.service.removeLdapDirectory(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def start_ldap_sync(self, ldap_name=None):
        query = "update directorypluginconfig set syncnow = '1'"
        if ldap_name is not None:
            query += "  where name = '{0}'".format(ldap_name)

        sql_result = self.run_sql_update(query)

        if sql_result['rows_updated'] > 0:
            result = True
        else:
            result = False

        return result

    """ LDAP System"""

    def get_ldap_system(self):
        try:
            result = self.service.getLdapSystem()
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_ldap_system(self, sync_enabled, ldap_server, user_id_attribute):

        try:
            result = self.service.updateLdapSystem(syncEnabled=sync_enabled,
                                                   ldapServer=ldap_server,
                                                   userIdAttribute=user_id_attribute)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """LDAP Authentication"""

    def get_ldap_authentication(self):
        try:
            result = self.service.getLdapAuthentication()
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_ldap_authentication(self, enabled, dn, password, search_base, servers, port, ssl):

        server_data = []

        for server in servers:
            server_data.append({'hostName': server,
                                'ldapPortNumber': port,
                                'sslEnabled': ssl})


        try:
            result = self.service.updateLdapAuthentication(authenticateEndUsers=enabled,
                                                           distinguishedName=dn,
                                                           ldapPassword=password,
                                                           userSearchBase=search_base,
                                                           servers={'server': server_data})
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Phone"""

    def get_phone(self, name):
        try:
            result = self.service.getPhone(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_phone(self, phone_data, line_data=None):

        if line_data is not None:
            phone_data['lines'] = {'line': line_data}

        try:
            result = self.service.addPhone(phone=phone_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_phone(self, name):
        try:
            result = self.service.removePhone(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_phone(self, phone_data, line_data=None):

        if line_data is not None:
            phone_data['lines'] = {'line': line_data}

        try:
            result = self.service.updatePhone(**phone_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Partitions"""

    def add_partition(self, name, description):

        partition_data = {'name': name,
                          'description': description}

        try:
            result = self.service.addRoutePartition(routePartition=partition_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    # Accepts a list of partitions, either as a list of strings with Partition names, or a list of dictionaries
    # containing the name and description for each partition.

    def add_partitions(self, partition_list):

        result = []

        for partition in partition_list:

            if not isinstance(partition, dict):
                partition = {"name": partition, "description": ""}

            try:
                result.append(self.service.addRoutePartition(routePartition=partition))
            except Exception as fault:
                result.append({'fault': fault})
                self.last_exception = fault

        return result

    def get_partition(self, name):

        try:
            result = self.service.getRoutePartition(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_partition(self, name):

        try:
            result = self.service.removeRoutePartition(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Calling Search Space"""

    def add_css(self, name, description, partition_list):

        css_data = {'name': name,
                    'description': description,
                    'members':
                        {'member': []}
                    }

        css_index = 1
        for partition in partition_list:
            partition_data = {'routePartitionName': partition,
                              'index': css_index}
            css_data['members']['member'].append(partition_data)
            css_index += 1

        try:
            result = self.service.addCss(css=css_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def get_css(self, name):

        try:
            result = self.service.getCss(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_css(self, name):

        try:
            result = self.service.removeCss(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_css(self, css_name, description, partition_list):

        members = {'member': []}

        css_index = 1

        for partition in partition_list:
            partition_data = {'routePartitionName': partition,
                              'index': css_index}
            members['member'].append(partition_data)
            css_index += 1

        try:
            result = self.service.updateCss(name=css_name, description=description, members=members)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Route Group"""

    def add_route_group(self, name, distribution_algorithm, device_list):

        rg_data = {
            'name': name,
            'distributionAlgorithm': distribution_algorithm,
            'members': {
                    'member': []
                }
            }

        rg_index = 1
        for device in device_list:
            rg_data['members']['member'].append({
                'deviceSelectionOrder': rg_index,
                'deviceName': device,
                'port': 0
            })
            rg_index += 1

        try:
            result = self.service.addRouteGroup(routeGroup=rg_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def get_route_group(self, name):

        try:
            result = self.service.getRouteGroup(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_route_group(self, name):

        try:
            result = self.service.removeRouteGroup(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_route_group(self, name):
        # TODO: Need to implement
        pass

    """Route List"""

    def add_route_list(self, name, description, cm_group, enabled, roan, members, ddi=None):

        rl_data = {
            'name': name,
            'description': description,
            'callManagerGroupName': cm_group,
            'routeListEnabled': enabled,
            'runOnEveryNode': roan,
            'members': {
                    'member': []
                }
            }

        rg_index = 1
        for member in members:
            rl_data['members']['member'].append({
                'selectionOrder': rg_index,
                'routeGroupName': member,
                'digitDiscardInstructionName': ddi
            })
            rg_index += 1

        try:
            result = self.service.addRouteList(routeList=rl_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def get_route_list(self, name):

        try:
            result = self.service.getRouteList(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_route_list(self, name):

        try:
            result = self.service.removeRouteList(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_route_group(self, name):
        # TODO: Need to implement
        pass

    """Route Pattern"""

    def add_route_pattern(self, pattern, partition, route_list, network_location, outside_dialtone):

        rp_data = {
            'pattern': pattern,
            'routePartitionName': partition,
            'destination': {
                    'routeListName': route_list
                },
            'blockEnable': False,
            'networkLocation': network_location,
            'provideOutsideDialtone': outside_dialtone
            }

        try:
            result = self.service.addRoutePattern(routePattern=rp_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def get_route_pattern(self, pattern, partition):

        try:
            result = self.service.getRoutePattern(pattern=pattern, routePartitionName=partition)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_route_pattern(self, pattern, partition):

        try:
            result = self.service.removeRoutePattern(pattern=pattern, routePartitionName=partition)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_route_pattern(self, name):
        # TODO: Need to implement
        pass

    """SIP Route Pattern"""

    def add_sip_route_pattern(self, pattern, partition, route_list):

        rp_data = {
            'pattern': pattern,
            'routePartitionName': partition,
            'sipTrunkName': route_list,
            'usage': 'Domain Routing',
            }

        try:
            result = self.service.addSipRoutePattern(sipRoutePattern=rp_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def get_sip_route_pattern(self, pattern, partition):

        try:
            result = self.service.getRoutePattern(pattern=pattern, routePartitionName=partition)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_sip_route_pattern(self, pattern, partition):

        try:
            result = self.service.removeRoutePattern(pattern=pattern, routePartitionName=partition)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_sip_route_pattern(self, name):
        # TODO: Need to implement
        pass

    """Conference Bridge"""

    def add_cfb(self, cfb_data):

        try:
            result = self.service.addConferenceBridge(conferenceBridge=cfb_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_cfb_cms(self, name, description, cfb_prefix, sip_trunk,
                    security_icon_control, override_dest, addresses,
                    username, password, port):
        cms_data = {
            'name': name,
            'description': description,
            'product': 'Cisco Meeting Server',
            'conferenceBridgePrefix': cfb_prefix,
            'sipTrunkName': sip_trunk,
            'allowCFBControlOfCallSecurityIcon': security_icon_control,
            'overrideSIPTrunkAddress': override_dest,
            'addresses': {
                'address': addresses
            },
            'userName': username,
            'password': password,
            'httpPort': port
        }

        result = self.add_cfb(cms_data)

        return result

    def get_cfb(self, name):

        try:
            result = self.service.getConferenceBridge(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_cfb(self, name):
        pass

        # try:
        #     result = self.service.removeCss(name=name)
        # except Exception as fault:
        #     result = None
        #     self.last_exception = fault
        #
        # return result

    def update_cfb(self, css_name, description, partition_list):
        pass

        # members = {'member': []}
        #
        # css_index = 1
        #
        # for partition in partition_list:
        #     partition_data = {'routePartitionName': partition,
        #                       'index': css_index}
        #     members['member'].append(partition_data)
        #     css_index += 1
        #
        # try:
        #     result = self.service.updateCss(name=css_name, description=description, members=members)
        # except Exception as fault:
        #     result = None
        #     self.last_exception = fault
        #
        # return result

    """Media Resource Group"""

    def get_mrg(self, name):

        try:
            result = self.service.getMediaResourceGroup(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Media Resource Group List"""

    def get_mrgl(self, name):

        try:
            result = self.service.getMediaResourceList(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Device Pool"""

    def get_device_pool(self, name):

        try:
            result = self.service.getDevicePool(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Device Security Profile"""

    def get_phone_security_profile(self, name):

        try:
            result = self.service.getPhoneSecurityProfile(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_phone_security_profile(self, phone_type, protocol, name, description, device_security_mode,
                                   authentication_mode, key_size, key_order, ec_key_size, tftp_encrypted_config,
                                   nonce_validity_time, transport_type, sip_phone_port, enable_digest_auth):

        security_profile = {'phoneType': phone_type,
                            'protocol': protocol,
                            'name': name,
                            'description': description,
                            'deviceSecurityMode': device_security_mode,
                            'authenticationMode': authentication_mode,
                            'keySize': key_size,
                            'keyOrder': key_order,
                            'ecKeySize': ec_key_size,
                            'tftpEncryptedConfig': tftp_encrypted_config,
                            'nonceValidityTime': nonce_validity_time,
                            'transportType': transport_type,
                            'sipPhonePort': sip_phone_port,
                            'enableDigestAuthentication': enable_digest_auth,
                            }

        try:
            result = self.service.addPhoneSecurityProfile(phoneSecurityProfile=security_profile)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """SIP Trunk Security Profile"""

    def get_sip_trunk_security_profile(self, name):

        try:
            result = self.service.getSipTrunkSecurityProfile(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_sip_trunk_security_profile(self, name, description, security_mode, incoming_transport, outgoing_transport,
                                       digest_auth, nonce_policy_time, x509_subject_name, incoming_port,
                                       app_level_auth, accept_presence_subscription, accept_ood_refer,
                                       accept_unsolicited_notify, allow_replaces, transmit_security_status,
                                       sip_v150_outbound_offer_filter, allow_charging_header):

        security_profile = {
            'name': name,
            'description': description,
            'securityMode': security_mode,
            'incomingTransport': incoming_transport,
            'outgoingTransport': outgoing_transport,
            'digestAuthentication': digest_auth,
            'noncePolicyTime': nonce_policy_time,
            'x509SubjectName': x509_subject_name,
            'incomingPort': incoming_port,
            'applLevelAuthentication': app_level_auth,
            'acceptPresenceSubscription': accept_presence_subscription,
            'acceptOutOfDialogRefer': accept_ood_refer,
            'acceptUnsolicitedNotification': accept_unsolicited_notify,
            'allowReplaceHeader': allow_replaces,
            'transmitSecurityStatus': transmit_security_status,
            'sipV150OutboundSdpOfferFiltering': sip_v150_outbound_offer_filter,
            'allowChargingHeader': allow_charging_header,
        }

        try:
            result = self.service.addSipTrunkSecurityProfile(sipTrunkSecurityProfile=security_profile)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_sip_trunk_security_profile(self, name):

        try:
            result = self.service.removeSipTrunkSecurityProfile(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """SIP Profile"""

    def get_sip_profile(self, name):

        try:
            result = self.service.getSipProfile(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_sip_profile(self, profile_data):

        try:
            result = self.service.addSipProfile(sipProfile=profile_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_sip_profile(self, profile_data):

        try:
            result = self.service.updateSipProfile(**profile_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """SIP Trunk """

    def get_sip_trunk(self, name):

        try:
            result = self.service.getSipTrunk(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def remove_sip_trunk(self, name):

        try:
            result = self.service.removeSipTrunk(name=name)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def add_sip_trunk(self, trunk_data):

        try:
            result = self.service.addSipTrunk(sipTrunk=trunk_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def update_sip_trunk(self, trunk_data):

        try:
            result = self.service.updateSipTrunk(**trunk_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    """Reset / Restart Devices"""

    def do_reset_restart_device(self, device, is_hard_reset, is_mgcp):
        reset_data = {
            'deviceName': device,
            'isHardReset': is_hard_reset,
            'isMGCP': is_mgcp
        }

        try:
            result = self.service.doDeviceReset(**reset_data)
        except Exception as fault:
            result = None
            self.last_exception = fault

        return result

    def reset_device(self, device):
        result = self.do_reset_restart_device(device, True, False)

        return result

    def restart_device(self, device):
        result = self.do_reset_restart_device(device, False, False)

        return result

    def reset_mgcp(self, device):
        result = self.do_reset_restart_device(device, True, True)

        return result

    def restart_mgcp(self, device):
        result = self.do_reset_restart_device(device, False, True)

        return result

    """Service Parameters"""

    def sql_update_service_parameter(self, name, value):

        query = "update processconfig set paramvalue = '{0}' where paramname = '{1}'".format(value, name)

        sql_result = self.run_sql_update(query)

        if sql_result['rows_updated'] > 0:
            result = True
        else:
            result = False

        return result

    def sql_get_service_parameter(self, name):

        query = "select * from processconfig where paramname = '{0}'".format(name)

        sql_result = self.run_sql_query(query)

        if sql_result['num_rows'] > 0:
            result = sql_result['rows']
        else:
            result = None

        return result

    """Device Association"""

    def sql_associate_device_to_user(self, device, userid, association_type='1'):

        device_pkid = self.sql_get_device_pkid(device)
        enduser_pkid = self.sql_get_enduser_pkid(userid)

        if device_pkid is not None and enduser_pkid is not None:

            query = "insert into enduserdevicemap (fkenduser, fkdevice, defaultprofile, tkuserassociation) " \
                    "values ('{0}','{1}','f','{2}')".format(enduser_pkid, device_pkid, association_type)

            sql_result = self.run_sql_update(query)

            if sql_result['rows_updated'] > 0:
                result = True
            else:
                result = False

            return result

    def check_connectivity(self):
        pass


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

# class PAWSHardwareInformationConnector(UCSOAPConnector):
#
#     def __init__(self, username, password, fqdn, wsdl, tls_verify=False):
#         _binding_name = "{http://services.api.platform.vos.cisco.com}HardwareInformationServiceSoap11Binding"
#         _address = "https://{ip_address}:8443/platform-services/services/HardwareInformationService.HardwareInformationServiceHttpsSoap11Endpoint/".format(ip_address=fqdn)  # noqa
#         UCSOAPConnector.__init__(self,
#                                  username=username,
#                                  password=password,
#                                  wsdl=wsdl,
#                                  binding_name=_binding_name,
#                                  address=_address,
#                                  tls_verify=tls_verify)
#
#     def get_hardware_information(self):
#         return self.service.getHardwareInformation()
#
#
# class PAWSPlatformConnector(UCSOAPConnector):
#
#     def __init__(self, username, password, fqdn, wsdl, tls_verify=False):
#         _binding_name = "{http://services.api.platform.vos.cisco.com}ClusterNodesServiceHttpBinding"
#         _address = "https://{ip_address}:8443/platform-services/services/ClusterNodesService.ClusterNodesServiceHttpsEndpoint/".format(ip_address=fqdn)# noqa
#         UCSOAPConnector.__init__(self,
#                                  username=username,
#                                  password=password,
#                                  wsdl=wsdl,
#                                  binding_name=_binding_name,
#                                  address=_address,
#                                  tls_verify=tls_verify)
#
#
# class PAWSConnector:
#
#     # last_exception = None
#
#     def __init__(self, username, password, ip_address, service='ClusterNodesService', tls_verify=True):
#
#         self.last_exception = None
#         _dir = os.path.dirname(__file__)
#
#         if service == 'HardwareInformation':
#             wsdl = os.path.join(_dir, 'paws/hardware_information_service.wsdl')
#             binding = "{http://services.api.platform.vos.cisco.com}HardwareInformationServiceSoap11Binding"
#             endpoint = "https://{ip_address}:8443/platform-services/services/HardwareInformationService.HardwareInformationServiceHttpsSoap11Endpoint/".format(ip_address=ip_address)
#         else:
#             wsdl = 'https://{ip_address}:8443/platform-services/services/ClusterNodesService?wsdl'.format(ip_address=ip_address)
#             binding = "{http://services.api.platform.vos.cisco.com}ClusterNodesServiceHttpBinding"
#             endpoint = "https://{ip_address}:8443/platform-services/services/ClusterNodesService.ClusterNodesServiceHttpsEndpoint/".format(ip_address=ip_address)
#
#         self.session = Session()
#         self.session.auth = HTTPBasicAuth(username, password)
#         self.session.verify = tls_verify
#
#         self.cache = SqliteCache(path='/tmp/sqlite_logcollection.db', timeout=60)
#
#         self.client = Client(wsdl=wsdl, transport=Transport(cache=self.cache, session=self.session))
#
#         self.service = self.client.create_service(binding, endpoint)
#
#     def get_hardware_information(self):
#         hw_info = self.service.getHardwareInformation()
#
#         return hw_info
