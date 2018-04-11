# -*- coding: utf-8 -*-
"""Useful SQL query utils for UC System Administration  tasks where full AXL object
instantiation and method calling is too verbose or slow"""

from .helpers import extract_pkid_from_uuid


def get_device_pkid(axl_connector, device_name):
    sql_statement = "select pkid " \
            "from device " \
            "where name={device_name}".format(
             device_name=device_name
            )
    return axl_connector.sql.query(sql_statement)


def get_enduser_pkid(axl_connector, userid):
    sql_statement = "select pkid " \
            "from enduser " \
            "where userid={userid}".format(
             userid=userid
            )
    return axl_connector.sql.query(sql_statement)


def associate_device_to_enduser(axl_connector, enduser_pkid_or_uuid, device_pkid_or_uuid, tkuserassociation=1):
    enduser_pkid = extract_pkid_from_uuid(enduser_pkid_or_uuid)
    device_pkid = extract_pkid_from_uuid(device_pkid_or_uuid)
    sql_statement = "insert into enduserdevicemap (fkenduser, fkdevice, defaultprofile, tkuserassociation)" \
                    "values ('{enduser_pkid}','{device_pkid}','f','{tkuserassociation}')".format(
                     enduser_pkid=enduser_pkid,
                     device_pkid=device_pkid,
                     tkuserassociation=tkuserassociation
                    )
    return axl_connector.sql.update(sql_statement)


def associate_enduser_to_user_group(axl_connector, enduser_pkid_or_uuid, dirgroup_pkid_or_uuid):
    enduser_pkid = extract_pkid_from_uuid(enduser_pkid_or_uuid)
    dirgroup_pkid = extract_pkid_from_uuid(dirgroup_pkid_or_uuid)
    sql_statement = "insert into enduserdirgroupmap (fkenduser, fkdirgroup) " \
                    "values ('{enduser_pkid}', '{dirgroup_pkid}')".format(
                     enduser_pkid=enduser_pkid,
                     dirgroup_pkid=dirgroup_pkid
                    )
    return axl_connector.sql.update(sql_statement)


def get_dnorpattern_pkid(axl_connector, dnorpattern, tkpatternusage=2):
    sql_statement = "select pkid from numplan " \
                    "where dnorpattern={dnorpattern} "\
                    "and tkpatternusage={tkpatternusage}".format(
                     dnorpattern=dnorpattern,
                     tkpatternusage=tkpatternusage
                     )
    return axl_connector.sql.query(sql_statement)


def get_service_parameter_details(axl_connector, parameter_name):
    sql_statement = "select * from processconfig "  \
                    "where paramname = '{parameter_name}'".format(
                     parameter_name=parameter_name
                    )
    return axl_connector.sql.query(sql_statement)


def update_service_parameter(axl_connector, parameter_name, parameter_value):
    sql_statement = "update processconfig " \
                    "set paramvalue = '{parameter_value}' " \
                    "where paramname = '{parameter_name}'".format(
                     parameter_value=parameter_value,
                     parameter_name=parameter_name
                    )
    return axl_connector.sql.update(sql_statement)
