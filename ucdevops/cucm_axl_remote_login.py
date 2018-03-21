#!/usr/bin/env python

# source - http://www.ucdevops.com/cisco-cucm-axl-python-extension-mobility-remote-login/
__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"

from suds.client import Client  
   
# Define AXL Authentication Credentials for Cluster  
username = "username"  
password = "password"  
   
# Define AXL URL for Cluster  
url = "https://CUCM:8443/axl/"  
   
# Define WSDL Location 
wsdl = "file:///C:/pathto/AXLAPI.wsdl"  
   
# Build SUDS Client Connection  
client = Client(location=url, url=wsdl, retxml=False, username=username, password=password)
# Open and read csv File, split on new line
data = open("login.csv", "r").read().split("\n")
   
# loop through and break out individual components  
for line in data[1:]:
    mac,profile,uid = line.split(",") 
    print(mac,profile,uid)
  
    # Call client service "doDeviceLogin" method and pass in the parameters  
    x = client.service.doDeviceLogin(deviceName=dn, loginDuration='0', profileName=pn, userId=uid)  
    print(x)
  
