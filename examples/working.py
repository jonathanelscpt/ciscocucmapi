# -*- coding: utf-8 -*-

import pprint
import json
from collections import OrderedDict
from lxml import etree
from zeep.exceptions import Fault

import ciscocucmapi
from ciscocucmapi import sql_utils
from ciscocucmapi.helpers import filter_attributes


def main():
    wsdl = 'file://C://Users//jonathan.els//develop//pvt-repos//UCToolkit//schema//current//AXLAPI.wsdl'
    #
    username = 'administrator'
    password = 'ciscopsdt'
    fqdn = "10.10.20.1"
    # username = 'ccmadmin'
    # password = 'cisco!test'
    # fqdn = "10.144.230.249"

    axl = ciscocucmapi.UCMAXLConnector(username=username, password=password, fqdn=fqdn, history=True)
    # axl = ciscocucmapi.UCMAXLConnector(history=True)

    # axl = ciscocucmapi.UCMAXLConnector(fqdn="10.10.20.1")

    pp = pprint.PrettyPrinter(indent=4)

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

    # try:
    #     cucm_phone = axl.phone.get(name="SEP111111111111")
    #     cucm_phone.name = "SEPFEEDFEEDFE10"
    #     cucm_phone.update(phone_defaults)
    #     cucm_phone.lines['line'] = phone_lines
    #     # print(cucm_phone.lines.line[1].dirn.pattern)
    #     axl.phone.add(**cucm_phone.filter(axl.phone.model()))
    # except Fault:
    #     print(axl.history.last_sent_xml)
    #     print(axl.history.last_received_xml)

    # sql_statement = "SELECT d.name " \
    #                 "FROM device d " \
    #                 "INNER JOIN commonphoneconfig cpc ON d.fkcommonphoneconfig=cpc.pkid " \
    #                 "INNER JOIN vpnprofile vp ON cpc.fkvpnprofile = vp.pkid " \
    #                 "WHERE vp.name = 'vpn-profile-name'"


    # try:
    #     print(axl.ldap_system.get())
    # finally:
    #     print(axl.history.last_sent_xml)
    #     print(axl.history.last_received_xml)
    # try:
    #     print(axl.ldap_authentication.get())
    # finally:
    #     print(axl.history.last_sent_xml)
    #     print(axl.history.last_received_xml)
    # print(axl.sql.query(sql_statement=sql_statement))
    # print(axl.dhcp_server.add(processNodeName="hq-cucm-pub"))
    # print(axl.mwi_number.add(pattern=12345, routePartitionName=None))
    # print(axl.enterprise_phone_config.get())
    # print(axl.history.last_received_xml)
    # axl.elin_group.add(name="axl_elin_group", elinNumbers={"elinNumber": [{"pattern": 6666, "partition": None}]})
    # print(axl.user.change_dnd_status(userID="user01", dndStatus=True))
    # print(axl.called_party_tracing.add(directorynumber=12345487234))
    # print(axl.directory_lookup_rules.add(name="test", numberOfDigits=2, digitsToBeRemoved=1, priority=1))
    # print(axl.http_profile.add(name="http", userName="joanthan", password="1234213", webServiceRootUri="https://herpaderp.com/"))
    # print(axl.handoff_configuration.add(pattern=1234324, routePartitionName=None))
    # rg_members = {
    #     "member": [
    #         {
    #             "deviceSelectionOrder": 1,
    #             "deviceName": "test_trunk",
    #             # "ports": 0
    #         },
    #         {
    #             "deviceSelectionOrder": 2,
    #             "deviceName": "SIPTrunktoCUP",
    #             # "ports": 0
    #         },
    #     ]
    # }
    # target = {
    #     "name": "my name",
    #     "description": "Herro!",
    #     "genWizardId": "a987sdf89dsf9sd8f09dsf-324-342",
    #     "lines": {
    #         "line": [
    #             {
    #                 "directoryNumber": "3453454",
    #                 "routePartitionName": "Phones_Pt"
    #             },
    #             {
    #                 "directoryNumber": "4563242",
    #                 "routePartitionName": "Phones_Pt"
    #             },
    #         ]
    #     }
    # }
    # model = {
    #     "name": "",
    #     "description": "",
    #     "lines": {
    #         "line": [
    #             {
    #                 "directoryNumber": "",
    #                 "routePartitionName": ""
    #             }
    #         ]
    #     }
    # }
    # print(axl.snmp_mib2_system_group.get(sysContact="test"))
    # axl.application_dial_rules.add(name="w23ww", numberBeginWith=34543, numberOfDigits=67, digitsToBeRemoved=23, prefixPattern=234234, priority=5)
    # print(axl.history.last_sent_xml)
    # print(axl.application_server.add(name="appcucserver", ipAddress="123.123.123.123", appServerType="Cisco Unity Connection"))
    # pp.pprint(axl.application_server.info(uuid="{DF5A6D36-A817-4539-AA68-E6100A77EBA2}"))
    # try:
    # #     rt = {
    # #     "clusterId": "",
    # #     "lastContactTime": "",
    # #     "clusterUriString": "",
    # #     "role": "",
    # #     "lastDataRecieved": "",
    # #     "syncronizationStatus": "",
    # #     }
    # #     print(axl.ils_config.get(returnedTags=None))
    # #     print(axl.ldap_system.get())
    # #     print(axl.ldap_authentication.get())
    # #     print([ls.uuid for ls in axl.ldap_search.list()])
    # #     print(axl.ldap_search.get(uuid='{82DA1670-3348-4788-908E-2FB4B0541AB0}'))
    # #     print(axl.ldap_search.update(uuid='{82DA1670-3348-4788-908E-2FB4B0541AB0}', userSearchBase2="dc=honkey, dc=tonk"))
    # #     print(axl.callmanager.list(returnedTags={"ports": {"sipPorts": {"sipPhonePort": ""}}}))
    #
    #     alarmConfigs = {
    #         "AlarmConfig": [
    #             # {
    #             #     "AlarmLevelEvent": "Informational",
    #             #     "monitor": "Local Syslog",
    #             #     "Enable": True,
    #             #     "RemoteServerName1": "",
    #             #     "RemoteServerName2": "",
    #             #     "RemoteServerName3": "",
    #             #     "RemoteServerName4": "",
    #             #     "RemoteServerName5": "",
    #             # },
    #             # {
    #             #     "AlarmLevelEvent": "Error",
    #             #     "monitor": "SDI Trace",
    #             #     "Enable": True,
    #             #     "RemoteServerName1": "",
    #             #     "RemoteServerName2": "",
    #             #     "RemoteServerName3": "",
    #             #     "RemoteServerName4": "",
    #             #     "RemoteServerName5": "",
    #             # },
    #             # {
    #             #     "AlarmLevelEvent": "Critical",
    #             #     "monitor": "SDL Trace",
    #             #     "Enable": True,
    #             #     "RemoteServerName1": "",
    #             #     "RemoteServerName2": "",
    #             #     "RemoteServerName3": "",
    #             #     "RemoteServerName4": "",
    #             #     "RemoteServerName5": "",
    #             # },
    #             {
    #                 "AlarmLevelEvent": "Critical",
    #                 "monitor": "Sys Log",
    #                 "Enable": True,
    #                 "RemoteServerName1": "123.123.123.100",
    #                 "RemoteServerName2": "123.123.123.101",
    #                 "RemoteServerName3": "123.123.123.102",
    #                 "RemoteServerName4": "123.123.123.103",
    #                 "RemoteServerName5": "123.123.123.104",
    #             },
    #         ]
    #     }
    #     # pp.pprint(axl.syslog_configuration.get(serverName="hq-cucm-pub").axl_data)
    #     # pp.pprint(axl.syslog_configuration.update(serverName="hq-cucm-pub", alarmConfigs=alarmConfigs))
    #     # pp.pprint(axl.process_node.list(returnedTags=["name", "nodeUsage", "processNodeRole"]))
    #     # pp.pprint(axl.process_node.get(uuid="BD1F5630-F85E-D345-8D24-41CAB521E37E"))
    #
    # except Fault as fault:
    #     print(fault.message)
    # finally:
    #     try:
    #         print(axl.history.last_sent_xml)
    #         print(axl.history.last_received_xml)
    #     except IndexError:
    #         pass

    # print(axl.snmp_user.get(userName="asdf"))
    # print(axl.snmp_community_string.get(communityName="asdf"))
    # pp.pprint(axl.route_plan_report.list())
    # pp.pprint(axl.enterprise_parameter.reset_all())
    # pp.pprint(axl.annunciator.get(name="ANN_2"))
    # pp.pprint(axl.announcement.get(name="AXL Announcement"))
    # pp.pprint(axl.announcement.model(include_types=True, target_cls=dict))
    # pp.pprint(axl.aar_group.update_matrix(aarGroupToName="qwerty", aarGroupFromName="qwerty", prefixDigit=999))
    # pp.pprint(axl.aar_group.update_matrix(uuid="F8F9B77B-94A3-4B73-8139-FC35F6554743", prefixDigit=2222))
    # axl.announcement.add(name="AXL Announcement")
    # print(filter_attributes(target, model))
    # pp.pprint(axl.phone.model(target_cls=dict, include_types=True))
    # axl.physical_location.add(name="PL_AXL", description='PL')
    # axl.device_mobility_info.add(name="DMI_AXL",
    #                              subNet="10.10.20.0",
    #                              subNetMaskSz=24,
    #                              members={"member": [{"devicePoolName": "Default"}]})
    # print(axl.feature_control_policy.get(name="asdf"))
    # axl.feature_control_policy.add(name="axl_fcp",
    #                                features={
    #                                    "feature": [
    #                                        {
    #                                            'featureName': "Meet Me",
    #                                            "overrideDefault": True,
    #                                            "enableSetting": True
    #                                        },
    #                                        {
    #                                            'featureName': "Mobility",
    #                                            "overrideDefault": True,
    #                                            "enableSetting": True
    #                                        }
    #                                    ]
    #                                })
    # axl.ip_phone_service.add(serviceName="new service",
    #                          asciiServiceName="new service",
    #                          serviceUrl="http://newservice.com:8080/service",
    #                          secureServiceUrl="https://newservice.com:8443/service")
    # print(axl.handoff_mobility.get(handoffNumber="343432"))
    # axl.handoff_mobility.list(name="name")
    # axl.mobility_profile.add(name="AXL", mobileClientCallingOption="Dial via Office Forward",
    #                          dvofServiceAccessNumber=12345, dvorCallerId=123466)
    # axl.recording_profile.add(name="RP_AXL", recorderDestination=12345123)
    # axl.region.options(name="test")
    # try:
        # print(axl.lbm_hub_group.list())
        # axl.phone_security_profile.get(name=)
        # axl.billing_server.add(hostName="billing.cisco.com", userId="billing", password="billitjie")
        # axl.snmp_user.get(userName="test")
        # axl.feature_group_template.add(name="FGT_AXL")
        # axl.meetme.add(pattern=4543534, routePartitionName="Phones_Pt")
        # axl.default_device_profile.get(name='asdf')
        # axl.route_partition.add(name="axl_pt")
        # print(axl.route_partition.get(name="axl_pt"))
        # print(axl.route_partition.list())
        # axl.route_partition.apply(name="axl_pt")
        # axl.route_partition.restart(name="axl_pt")
        # try:
        #     axl.route_partition.reset(name="axl_pt")
        # except AttributeError as e:
        #     print(e)
        # axl.route_list.add(name="axl_rl2", callManagerGroupName="Default")
        # axl.route_pattern.add(pattern="80066", routePartitionName="Phones_Pt", destination={"routeListName": "axl_rl"})
        # axl.sip_dial_rules.add(name="sdr2")
        # axl.sip_realm.add(realm="jonathan.lab", userid="jonathan.els", digestCredentials="herpies")
        # axl.voh_server.add(name="voh_axl", sipTrunkName="SIPTrunktoCUP")
        # axl.wlan_profile.add(name="axl_wlan", ssid="jonathan")
        # print(axl.wlan_profile.get(name="axl_get"))
        # print(axl.wlan_profile_group.get(name="asdfsdf"))
        # axl.wifi_hotspot.add(name="asdf_wifi", ssidPrefix="asdf")
        # axl.network_access_profile.add(name="nap_axl2")
        # print(axl.advertised_patterns.add(pattern=1234))
        # axl.blocked_learned_patterns.add(pattern=1112)
        # uuid = axl.remote_cluster.get(clusterId="remote1.devnet.lab")  #fullyQualifiedName="remote1.devnet.lab"
        # axl.remote_cluster.do_update(clusterId="remote1.devnet.lab", server="remote1.devnet.lab")
        # sipp = axl.sip_profile.get(name="Standard SIP Profile")
        # axl.sip_profile.options(uuid="FCBC7581-4D8D-48F3-917E-00B09FB39213", returnedChoices={"userInfo": {"first": 2, "skip":1}, "dtmfDbLevel": {"first": 2}})
        # print(axl.audio_codec_preference_list.get(name="asdf"))
        # axl.conference_now.list()
    # except Fault as fault:
    #     print(fault.message)
    # finally:
    #     try:
    #         # axl.route_partition.remove(name="axl_pt")
    #         print(axl.history.last_sent)
    #         print(axl.history.last_received)
    #     except Exception:
    #         pass
    # axl.softkey_template.add(name="new skt", description="ridiculous!")
    # print(axl.softkey_set.get(name="new skt"))
    # print(axl.common_device_config.apply(name="CDC_AXL"))
    # axl.common_phone_profile.add(name="CPC", unlockPwd="asdf!asdf")
    # print(axl.common_phone_profile.get(name="CPC"))
    # axl.route_group.add(name="api-add-rg", members=rg_members)
    # axl.route_list.add(name="axl_rl", callManagerGroupName="Default")
    # axl.route_pattern.add(pattern="8003", routePartitionName="Phones_Pt", destination={"routeListName": "axl_rl"})
    # axl.sip_route_pattern.add(pattern="cisco.com", routePartitionName="Xlate_Pt", sipTrunkName="axl_rl")
    # axl.srst.add(name="NYC_SRST", ipAddress="192.168.200.100")
    # print(axl.transcoder.get(name="NYC_XCODE"))
    # axl.transcoder.add(name="AXL_Xcode", devicePoolName="Default")
    # axl.translation_pattern.add(pattern=8082, routePartitionName="Xlate_Pt")
    # axl.voicemail_pilot.add(dirn=8888)
    # axl.voicemail_profile.add(name="axl_vmp", voiceMailPilot={"dirn": 8888})
    # axl.uc_service.add(name="CTI", serviceType="CTI", productType="CTI", hostnameorip="cucm.cisco.com")
    # axl.uc_service.add(name="AXL_CTI", serviceType="CTI", hostnameorip="cisco.com")
    # axl.uc_service.add(name="AXL_LDAP", serviceType="Directory", hostnameorip="ldap.jj.com")
    # axl.uc_service.add(name="AXL_MS", serviceType="MailStore", hostnameorip="ms.jj.com")
    # axl.uc_service.add(name="AXL_TMS", serviceType="Video Conference Scheduling Portal", hostnameorip="tms.jj.com", ucServiceXml={"TmsPortalUrl": "tms.jj.com"})
    # axl.uc_service.add(name="AXL_VM", serviceType="Voicemail", hostnameorip="vm.jj.com")
    # axl.uc_service.add(name="AXL_WBX", serviceType="Conferencing", hostnameorip="jj.webex.com")
    # axl.uc_service.add(name="AXL_IMP", serviceType="IM and Presence", hostnameorip="imp.sandbox.com")
    # axl.service_profile.add(name="UC")
    # print(axl.sip_trunk.get(name="test_trunk"))
    # axl.sip_trunk.add(name="axl_trunk_2", devicePoolName="Default", destinations={"destination": [{"addressIpv4": "1.233.233.2", "port": 5060, "sortOrder": 1}]})
    # axl.sip_trunk_security_profile.add(name="STSP_AXL", acceptOutOfDialogRefer="true", acceptUnsolicitedNotification="true", acceptPresenceSubscription="true")
    # axl.sip_profile.add(name="SP2")
    # pp.pprint(axl.user_group.get(name="UG").axl_data)
    # axl.time_period.add(name="TPRD")
    # axl.time_schedule.add(name="SC", members={"member": [{"timePeriodName": "TPRD"}]})
    # axl.user_profile.add(name="UP2",
    #                      deskPhones="asdf",
    #                      mobileDevices="asdf",
    #                      profile="asdf",
    #                      universalLineTemplate="Sample Line Template with TAG usage examples",
    #                      allowProvision="false")
    # print(axl.user_profile.get(name="Standard (Factory Default) User Profile"))
    # axl.quick_user_phone_add.add(userId="jj", lastName="Els", extension="4007", routePartitionName="Phones_Pt")
    # axl.udt.add(name="axl_udt", devicePool="Default")
    # axl.ult.add(name="axl_ult",lineDescription="test",routePartition="Phones_Pt")

    # axl.remote_destination.add(name="Jonathan RD", destination="6666", ownerUserId="jonathan.els",
    #                            remoteDestinationProfileName="RDPJONATHAN")
    # axl.line.reset(name="123432", uuid="uuid")
    # sql_utils.ldap_sync(axl, name=None)

    # try:
    #     axl.rdp.add(name="RDPAXL", devicePoolName="Default", userId="jonathan.els")
    #     # print(axl.rdp.get(name="rdpjonathan"))
    # except:
    #     print(axl.history.last_sent)
    #     print(axl.history.last_received)
    # print(axl.translation_pattern.get(pattern=8080, routePartitionName="Xlate_Pt"))
    # axl.location.add(name="AXL_LIB_LOC")
    # axl.mtp.add(name="axl_mtp", devicePoolName="Default")
    # axl.phone_button_template.add(name="_new 6961", basePhoneTemplateName="Standard 6961 SIP")
    # axl.phone_ntp_reference.add(ipAddress="192.168.111.222", description="newly added after refactoring")

    # dp = axl.date_time_group.list()
    # ldap = {
    #     "name": "sandboxldap",
    #     "ldapDn": "administrator",
    #     "ldapPassword": "ciscopsdt",
    #     "userSearchBase": "OU=UCCX Users,DC=abc,DC=inc",
    #     "intervalValue": "3",
    #     "servers": {
    #         "server": {
    #             "hostName": "10.10.20.100",
    #             "ldapPortNumber": "389"
    #         }
    #     }
    # }

    # ldap_uuid = axl.ldap_directory.add(**ldap)
    # ldir = axl.ldap_directory.get(uuid=ldap_uuid, returned_tags={"uuid": ""})

    # custom = {
    #     "ldapConfigurationName": "sandboxldap",
    #     "customUserField": "initials",
    #     "ldapUserField": "initials",
    #     }

    # print(axl.route_partition.add(name="factory_flattening_test_Pt"))

    # print(axl.ldap_directory.sync_now(name="sandboxldap"))
    # with open("../out/ldap.json", "w") as _:
    #     json.dump(axl.ldap_directory.model(target_cls=dict, include_types=True), _, indent=4)
    # print()

    # members = {
    #     "member": {
    #         "lineSelectionOrder": 1,
    #         "directoryNumber": {
    #             "pattern": "2005",
    #             "routePartitionName": "Phones_Pt"
    #         }
    #     }
    # }
    # axl.line_group.add(name="my_new_lg", members=members)

    # axl_lg = axl.line_group.get(name="axl_lg")
    # with open("../out/line_group.json", "w") as _:
    #     json.dump(axl_lg.axl_data, _, indent=4)
    # print()
    # line_sql = axl.sql.query("select * from numplan where dnorpattern='4000'")
    # line_sql.to_csv("../out/sql.csv")

    # axl.conference_bridge.add(name="AXL_CFB", devicePoolName="Default")
    # rt = {
    #     "name": "",
    #     "confidentialAccess": {
    #         "confidentialAccessMode": "",
    #         "confidentialAccessLevel": ""
    #
    #     }
    # }
    # list_phone_res = axl.client.get_type("ns0:LPhone")
    # all_phones = axl.phones.list()
    # pp.pprint([phone for phone in all_phones])

    #
    # phone = axl.phones.get(name="SEP203A07FC523A")
    # axl.phones.update(name="SEP203A07FC523A", description="changed desc2")
    # ph = axl.phones.get(name="SEP203A07FC523A")
    # axl.aar_group.add(name="aar_test")
    # aar = axl.aar_group.get(name="aar_test")
    # uuid_resp = axl.aar_group.update(name="aar_test", newName="aar_test_updated")
    # aar_get = axl.aar_group.get(uuid=uuid_resp)
    # axl.aar_group.remove(uuid=uuid_resp)
    # axl.aar_group.get(uuid=uuid_resp)
    # pp.pprint(phone.axl_data)
    # phones = axl.phones.list(
    #     search_criteria={"name": "%"},
    #     returned_tags={"name": ""}
    # )
    # pp.pprint(sorted(list(phone.name for phone in phones)))

    # pp.pprint(get_model_dict(list_phone_res))

    # # print(type(get_line_obj.elements_nested[0][1][0]))
    # # print(type(get_line_obj.elements_nested[0][1][0][0]))
    # # print(type(get_line_obj.elements_nested[0][1][0][1]))
    # print(isinstance(get_req, UnresolvedType))
    # print(get_req.resolve())
    # print(extract_get_choices(get_req.elements_nested[0][1][0]))

    # t =('uuid',
    #     'name',
    #     ('pattern', 'routePartitionName')
    #     )
    # d = {
    #     # "uuid": "",
    #     # "name": "",
    #     "routePartitionName": "",
    #     # "pattern": ""
    # }
    # print(check_valid_attribute_req_dict(t, d))
    # test_dict = {
    #     'name': 'SEPAAAABBBBCCCC',
    #     'callingSearchSpaceName': {
    #         '_value_1': 'US_NYC_NATIONAL_CSS',
    #         'uuid': '{987345984385093485gd09df8g}'
    #     }
    # }
    #
    # print(sanitize_data_model_dict(test_dict))

    # print([element[0] for element in list_obj.elements[0][1].type.elements])
    # zeep_obj = axl.client.get_type("ns0:XPhone")
    # min_add_kwargs = {el.name: (el.min_occurs, el.is_optional, el.nillable, el.default)
    #                   for el in list(filter_mandatory_attributes(zeep_obj))}
    # pp.pprint(min_add_kwargs)
    # for attr, v in min_add_kwargs.items():
    #     min_add_kwargs[attr] = bot_phone[attr]
    # pp.pprint(min_add_kwargs)

    # # del min_add_kwargs['primaryPhoneName']
    # # del min_add_kwargs['phoneTemplateName']
    # # del min_add_kwargs['phoneTemplateName']
    # #
    # min_add_kwargs['name'] = 'BOTADDTEST'
    # axl.phones.add(**min_add_kwargs)

    # zeep_obj = axl.client.get_type("ns0:XPhone")
    # min_add_kwargs = {el.name: None for el in list(filter_mandatory_attributes(zeep_obj))}
    # min_add_kwargs['class'] =
    # min_add_kwargs['commonPhoneConfigName'] =
    # min_add_kwargs['devicePoolName'] =
    # min_add_kwargs['locationName'] = "Hub_None"
    # min_add_kwargs['name'] = 'BOTPHONETEST'
    # min_add_kwargs['phoneTemplateName'] =
    # min_add_kwargs['protocol'] = "SIP"

    # print(serialize_object(botphone.elements[0][1].type.elements[0][1].name))
    # pp.pprint(dict(mandatory_attrs))
    # print("hello")

    # print(
    #     [dict((element.tag, element.text) for element in row) for row in add_phone_req.elements]
    # )
    # print((serialize_object(add_phone_req)))
    # botphone.newName = "BOTNEWBOTUSER"
    # del botphone["certificateStatus"]
    # del botphone["currentProfileName"]
    # del botphone["uuid"]
    # # del botphone["lines"]
    # del botphone["model"]
    # del botphone["protocol"]
    # del botphone["loginTime"]
    # del botphone["protocolSide"]
    # del botphone["loginUserId"]
    # del botphone["currentConfig"]
    # del botphone["roamingDevicePoolName"]
    # del botphone["numberOfButtons"]
    # del botphone["class"]
    # del botphone["loginDuration"]
    # del botphone["isDualMode"]
    # del botphone["product"]
    # del botphone["ctiid"]
    # del botphone["confidentialAccess"]
    # axl.phones.update(**dict(botphone))

    # names = {"name": "BOTUSER%"}
    # uuid = '{93ABE697-403C-F042-60D3-D7694DC05792}'
    # returnedTags = {"name": "", "protocol": ""}
    # cluster_phones = axl.phones.list(search_criteria=names, returned_tags={"name": ""})
    # botphone
    # # print([phone.name for phone in cluster_phones])
    # numplan_out = axl.sql.query("SELECT * FROM numplan where dnorpattern LIKE '1%'")
    # dn_list = sorted([row['dnorpattern'] for row in numplan_out])
    # print(dn_list)
    # # check_phone = axl.phones.get(uuid=uuid, returnedTags=returnedTags)
    # # print(check_phone)
    # # axl.phones.remove(name="BOTUSER015")

    # bot_names = {
    #     "name": "%"
    # }
    # returned_tags = {
    #     "name": "",
    #     "description": "",
    #     "callingSearchSpaceName": ""
    # }

    # created_bot_phone = axl.lines.create(pattern="1001", description="New Line", routePartitionName="DN_PT")
    # # print(created_bot_phone.__bases__)
    # axl.lines.add(created_bot_phone)

    # phones = axl.phones.list(search_criteria=bot_names, returned_tags=returned_tags)
    # # accessing and updating phone attributes
    # botuser15 = next(filter(lambda person: person.name == 'BOTUSER015', phones))
    # botuser15.callingSearchSpaceName = "US_NYC_NATIONAL_CSS"
    # print(botuser15.callingSearchSpaceName)
    # print(botuser15.protocolSide)

    # new_rp_name="new_test6"
    # axl.route_partitions.add(name=new_rp_name)
    # new_rp = axl.route_partitions.get(name=new_rp_name)
    # # kwargs = dir_uri_rp.axl_data
    # del kwargs['dialPlanWizardGenId']
    # del kwargs['uuid']
    # del kwargs['partitionUsage']
    # # del kwargs['timeScheduleIdName']
    # # del kwargs['partitionUsage']
    # print(kwargs)
    # axl.route_partitions.apply(name=new_rp.name)
    # axl.route_partitions.restart(name=new_rp.name)
    # axl.route_partitions.remove(name=new_rp.name)

    # local dd env

    # lines = axl.lines.list(search_criteria={"pattern": "%"}, returned_tags={"8000": "", "routePartitionName": ""})
    # line = axl.lines.get(pattern="8000", routePartitionName="Phones_PT")
    # line = axl.lines.get(uuid="{E67D8377-F53F-1FB6-B4F9-75AFF5F4078E}")
    # print(line.routePartitionName)
    # print([(line.pattern, line.routePartitionName) for line in lines])


if __name__ == '__main__':
    main()
