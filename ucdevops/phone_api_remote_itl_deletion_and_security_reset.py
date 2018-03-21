#!/usr/bin/env python

# source - http://www.ucdevops.com/working-with-the-cisco-handset-api-in-python3-remote-itl-delete-reset-security-settings/

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"

from xmltodict import unparse
from collections import OrderedDict
import requests
import time
from ipaddress import IPv4Network
import re
from multiprocessing import Pool

# Phone Message XML Headers
headers = {"content-type": "application/xml"}

# CUCM Phone Owner / Application User Credentials
u = "username"
p = "password"
# Sip Handset configuration url, used for extracting ITL signature
conf_url = "/CGI/Java/Serviceability?adapter=device.statistics.configuration"

# Define the correct ITL Signature value to match against
# used for phones that present the ITL in their html
itl_sig = "<B>EE 5C 62 E0 5E 2B C6 82 2A 45 64 1E EB BA BF F2 47 6E 1D 93 </B>"

# Define the subnets for the phones that you wish to target
networks = ["10.10.0.0/16"]

# Define supported Sip models
sip_models = ("CP-8861", "CP-8841")
# Define supported SCCP models
sccp_models = ("CP-7965G")

# Model, key press ITL Delete Combination and Delay(model specific)
models = {
    "CP-8861": {
        "keys": [
            "Key:Applications", "Key:KeyPad5", "Key:KeyPad4",
            "Key:KeyPad5", "Key:Soft3", "Key:Soft1"
        ],
        "delay": 1},
    "CP-7965G": {
        "keys": [
            "Init:Settings", "Key:Settings", "Key:KeyPad4", "Key:KeyPad5",
            "Key:KeyPad2", "Key:KeyPadStar", "Key:KeyPadStar",
            "Key:KeyPadPound", "Key:Soft2", "Key:Soft4", "Key:Soft2"
        ],
        "delay": 2},
    "CP-8841": {
        "keys": [
            "Key:Applications", "Key:KeyPad5", "Key:KeyPad4",
            "Key:KeyPad5", "Key:Soft3", "Key:Soft1"
        ],
        "delay": 1}
}

def get_phone_base_html(address):
    # Return phone base html
    return requests.get("http://" + address).text
    
def get_conf_html(address):
    # Return phone configuration  html
    return requests.get(
        "http://" + address + conf_url
    ).text
    
def get_itl_sig(address):
    # Return regex match result of our itl signature
    # For phones that support it
    return re.search(
        itl_sig, get_conf_html(address)
    )
    
def get_phone_model(html, regex_list):
    # Classify the phone model by
    # running a regex test on the returned HTML
    for regex in regex_list:
        search = re.search(regex, html)
        if search:
            return search.group()
        else:
            pass
    print("Could Not Classify...")
    
# Define our function to process the deletion
# of the itl files per phone model
def process_phone(address, phone_model):
    # Carries out the required steps for each model of phone
    if phone_model in sccp_models:
        send_key_press(
            address,
            build_xml(phone_model),
            models[phone_model]["delay"]
        )
    # Sip Phones - Itl signature can be checked
    elif phone_model in sip_models:
        # Check for itl signature
        if not get_itl_sig(address):
            send_key_press(
                address,
                build_xml(phone_model),
                models[phone_model]["delay"]
            )
        else:
            print("Address '{}' has the correct ITL".format(str(address)))
     else:
         print("Phone model not found")
         
# Define our function to iterate through our key press list
# and send the key press to the target device
def send_key_press(address, key_press_list, delay):
    for key_press in key_press_list:
        r = requests.post(
            url="http://" + address + "/CGI/Execute",
            data=key_press, headers=headers, auth=(u, p)
        )
        print(r.text)
        time.sleep(delay)
        
# Define our function to build our xml key press messages
def build_xml(phone_model):
    messages = []
    for kp in models[phone_model]["keys"]:
        d = OrderedDict(
            [("CiscoIPPhoneExecute", OrderedDict(
                [("ExecuteItem", OrderedDict([("@Priority", "0"), ("@URL", kp)])
                  )])
              )])
        messages.append({"XML": unparse(d)})
    return messages
    
# Define our main function
def main(address):
    # Create list of phone model Keys
    model_keys = models.keys()
    # Iterate Through IP Address List
    print("IP = '{}'".format(address))
    try:
        phone_model = get_phone_model(
            get_phone_base_html(address),
            model_keys
        )
    except Exception as e:
        print("Exception : '{}'".format(str(e)))
    else:
        print("Phone model {}".format(phone_model))
        process_phone(address, phone_model)
        
if __name__ == '__main__':
    # Build a list of ip addresses for the given subnets
    ip_addresses = [
        str(ip)for net in networks for ip in IPv4Network(net).hosts()
    ]
    # Create a Process Pool so that we can allocate multiple processes and divide up the work
    pool = Pool(processes=4)
    pool.map(main, ip_addresses)
