#!/usr/bin/env python

# source - http://www.ucdevops.com/cisco-cucm-ucxn-sql-python3-ddi-migration-updating-extensions-devices-descriptions-and-text-labels/

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"

import requests
import json
import re

# Json Headers
headers = {
    'Accept': 'application/json',
    'Content-type': 'application/json'
}

# Unity Connection API Credentials
u = 'user'
p = 'password'
# Define Unity Connection host
base_url = 'https://UcxnHost'
# Define Unity Connection User Query URI
get_user_url = '/vmrest/users?query=(alias is {0})'

# Regex Match's
# DDI Regex Match
ddi_regex = r'^\+61390974(\d{3})$'
# Short Code Regex Match
sd_regex = r'^(830)(\d{1})(\d{3})$'
# DDI Replacement Value
ddi_replace = '+61385387'
# Short Code Replacement Value
sd_replace = '7'

# Define the Requests Session Object
def requests_session():
    s = requests.session()
    s.auth = (u, p)
    s.headers = headers
    return s
    
# Create Requests Session Object
s = requests_session()

def open_input_users():
    # Returns a list of userid aliases
    return open('users.txt', 'r').read().split('\n')
    
def get_user_data_by_alias(user):
    # This function Obtains an initial user object by querying an "alias" e.g "Mitch.Dawson"
    # The initial user object is interogated to obtain the API URL for a full user data object.
    # Build URL
    url = base_url + get_user_url.format(user)
    # Make Api Request
    r = s.get(url)
    # Convert Json response to Python Dict
    j = r.json()
    # Extract the "URI" attribute from the User Object, this is a path to query the full user data object.
    user_data = j['User']['URI']
    # Build a url with the new path
    url = base_url + user_data
    # Make Api Request
    r = s.get(url)
    # Convert Json response to Python Dict and return
    return r.json()
    
def get_alternate_extension_object(alternate_extensions_uri):
    # Function returns a list of Alternate Extension Objects
    url = base_url + alternate_extensions_uri
    r = s.get(url)
    return r.json()
    
def change_alternate_extension(ae_uri, new_number):
    # Function posts the new number to the unique
    # alternate extension url "DtmfAccessId" field
    # Build the new url
    url = base_url + ae_uri
    # Create json data object from dictionary values
    update = json.dumps({'DtmfAccessId': new_number})
    # Make a "put" request to the API, providing the json data
    r = s.put(url, data=update)
    # Check for the return status code. "204" is successful
    if r.status_code == 204:
        print('Successfully Changed to new Number "{}"'.format(new_number))
    else:
        print('Error Changing to new Number "{}"'.format(new_number))
        
def build():
    # Open the list of users
    users = open_input_users()
    for user in users:
        if not str(user).startswith('#'):
            # Get User Object by Alias
            user_data = get_user_data_by_alias(user)
            # Extract the Alternate Extension Uri
            alternate_extensions_uri = user_data['AlternateExtensionsURI']
            # Gets a list of dictionaries containing all Alternate Extension Objects
            alternate_extension_object = get_alternate_extension_object(
                alternate_extensions_uri)['AlternateExtension']
            # Iterate Through return alternate extension objects list
            for ae in alternate_extension_object:
                # Get the alternate extension number
                dtmf_access_id = str(ae['DtmfAccessId'])
                # Test for E164 DDI Regex Match
                match = re.match(ddi_regex, dtmf_access_id)
                if match:
                    # Extract the individual URL for this alternate extension object
                    uri = ae['URI']
                    # Build the new number
                    number = ddi_replace + str(match.group(1))
                    # Call the Change Alternate Extension function
                    change_alternate_extension(uri, number)
                else:
                    # Test for Short Dial Regex Match
                    match = re.match(sd_regex, dtmf_access_id)
                    if match:
                        # Extract the individual URL for this alternate extension object
                        uri = ae['URI']
                        # Build the new number
                        number = str(match.group(1)) \
                            + sd_replace + str(match.group(3))
                        # Call the Change Alternate Extension function
                        change_alternate_extension(uri, number)
                    else:
                        pass
                        
build()
