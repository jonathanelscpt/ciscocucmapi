#!/usr/bin/env python

# source - http://www.ucdevops.com/automated-interogation-of-cisco-8861-handsets-parameters-via-web-interface-with-python3/

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"

import requests
import re
from ipaddress import IPv4Network
import time
from lxml import etree

# Define Networks
nets = ['10.10.10.0/24']
# Create a list of IP's using the IPV4Network Class
ips = [str(ip) for net in nets for ip in IPv4Network(net).hosts()]

# Define Phone Base Configuration Statistics Url
baseurl = '/CGI/Java/Serviceability?adapter=device.statistics.configuration'
# Model Alternate TFTP OFF Combination
combination = [
    'Key:Applications', 'Key:KeyPad5', 'Key:KeyPad1',
    'Key:KeyPad1', 'Key:KeyPad8', 'Key:Soft4', 'Key:Soft2',
    'Key:Soft1', 'Key:Soft1'
]

# Credentials
u = 'username'
p = 'password'

# Handset API Http Headers
headers = {'content-type': 'application/xml'}

# Define Regex Search string
regex = 'Alternate TFTP</B></TD><td width=20></TD><TD><B>Yes'

def getHtml(address):
    # Function makes an HTTP request
    # to the required url and returns the HTML
    url = 'http://' + address + baseurl
    r = requests.get(url, timeout=1)
    return r.text
    
def checkHtml(html):
    # Check if Alternate TFTP Value is True
    # by running a regex test on the returned HTML
    return re.search(regex, html)
    
def buildXml():
    # Function creates the xml messages
    # required to turn Alternate TFTP off, returns a list
    messages = []
    for c in combination:
        tag_1 = etree.Element('CiscoIPPhoneExecute')
        tag_2 = etree.SubElement(tag_1, 'ExecuteItem')
        tag_2.set('Priority', '0')
        tag_2.set('URL', c)
        msg = etree.tostring(tag_1, pretty_print=False)
        data = {'XML': msg}
        messages.append(data)
    return messages
    
def sendXml(messages, address):
    # Function unpacks the messages from the supplied list
    # and posts to the phone API
    for message in messages:
        url = 'http://' + address + '/CGI/Execute'
        r = requests.post(
            url, data=message, headers=headers, auth=(u, p)
        )
        print(r.text)
        # Introduce a delay between messages, required for some devices.
        time.sleep(1)
        
def run():
    for ip in ips:
        print(ip)
        # Try and Except loop
        # required to catch exception where there is no response from ip
        try:
            html = getHtml(ip)
        except Exception as e:
            # If there was no response go to next ip
            continue
        else:
            # Check for presence of Alternate TFTP = YES
            if checkHtml(html):
                # Create the list of xml messages
                phoneXml = buildXml()
                # Call the sendXml function to post the messages
                sendXml(phoneXml, ip)
                
run()
