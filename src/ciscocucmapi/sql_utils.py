"""Useful SQL query utils for specific UC System Administration tasks"""

from .helpers import extract_pkid_from_uuid


def get_device_pkid(axl_connector, device_name):
    """Get a device pkid from the device name"""
    sql_statement = f"select pkid from device where name={device_name}"
    return axl_connector.sql.query(sql_statement)


def get_enduser_pkid(axl_connector, userid):
    """Get an enduser pkid from the enduser userid"""
    sql_statement = f"select pkid from enduser where userid={userid}"
    return axl_connector.sql.query(sql_statement)


def associate_device_to_enduser(axl_connector, enduser_pkid_or_uuid, device_pkid_or_uuid, tkuserassociation=1):
    """Insert row into enduserdevicemap table to add user/device association"""
    enduser_pkid = extract_pkid_from_uuid(enduser_pkid_or_uuid)
    device_pkid = extract_pkid_from_uuid(device_pkid_or_uuid)
    sql_statement = f"insert into enduserdevicemap (fkenduser, fkdevice, defaultprofile, tkuserassociation)" \
                    f"values ('{enduser_pkid}','{device_pkid}','f','{tkuserassociation}')"
    return axl_connector.sql.update(sql_statement)


def associate_enduser_to_user_group(axl_connector, enduser_pkid_or_uuid, dirgroup_pkid_or_uuid):
    """Insert row into enduserdirgroupmap table to add enduser/user group association"""
    enduser_pkid = extract_pkid_from_uuid(enduser_pkid_or_uuid)
    dirgroup_pkid = extract_pkid_from_uuid(dirgroup_pkid_or_uuid)
    sql_statement = f"insert into enduserdirgroupmap (fkenduser, fkdirgroup) " \
                    f"values ('{enduser_pkid}', '{dirgroup_pkid}')"
    return axl_connector.sql.update(sql_statement)


def get_dn_pkid(axl_connector, dnorpattern, tkpatternusage=2):
    """Get dn pkid from the dnorpattern from numplan table.

    Note:
        Does not ensure uniqueness as does not include join on route partition table
    :param axl_connector: (UCMAXLConnector) axl connector
    :param (str) dnorpattern: pattern or DN
    :param (int) tkpatternusage: defaults to 2 for DNs
    :return: (str) pkid
    """
    sql_statement = f"select pkid from numplan " \
                    f"where dnorpattern={dnorpattern} "\
                    f"and tkpatternusage={tkpatternusage}"
    return axl_connector.sql.query(sql_statement)


def get_service_parameter_details(axl_connector, parameter_name):
    """Get individual service parameters tuple"""
    sql_statement = f"select * from processconfig "  \
                    f"where paramname = '{parameter_name}'"
    return axl_connector.sql.query(sql_statement)


def update_service_parameter(axl_connector, parameter_name, parameter_value):
    """Update service parameter with specified value"""
    sql_statement = f"update processconfig " \
                    f"set paramvalue = '{parameter_value}' " \
                    f"where paramname = '{parameter_name}'"
    return axl_connector.sql.update(sql_statement)


def ldap_sync(axl_connector, name=None, uuid=None):
    """SQL-based LDAP sync fallback method for AXL versions not supporting doLdapSync"""
    try:
        return axl_connector.sql.update(
            sql_statement=f"update directorypluginconfig set syncnow = '1' where name = '{name}'"
        )
    except TypeError:
        name = extract_pkid_from_uuid(
            axl_connector.ldap_directory.get(uuid=uuid, returnedTags={"name": ""})
        )
        return ldap_sync(axl_connector, name=name)
