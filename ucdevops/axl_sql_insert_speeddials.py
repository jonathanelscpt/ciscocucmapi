#!/usr/bin/env python

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"


from suds.client import Client
from suds.cache import NoCache


# Define Authentication Credentials for the cluster
u = 'username'
p = 'password'
# Define AXL URL for the cluster
url = 'https://CUCM:8443/axl/'
# Define WSDL Locations
wsdl1 = 'file:///C:/PathTo/AXLAPI.wsdl'

# Create the Suds client Object
client = Client(
    location=url, url=wsdl1,
    username=u, password=p,
    cache=NoCache()
)

# Define the SQL Query
query = """
INSERT INTO speeddial
(fkdevice, speeddialindex, speeddialnumber, label, labelascii)
VALUES (
(SELECT pkid from device where name = "{0}"),
"{1}", "{2}", "{3}", "{4}"
)
"""

# Open input file then read it then split on new line
file = open('speeddial.txt', 'r').read().split('\n')

# Loop Through the file skipping the header line
for line in file[1:]:
    # Break out the Components from the text file
    dev, pos, num, lab, asc = line.split(',')
    # Format the SQL query with the values we require
    query = query.format(dev, pos, num, lab, asc)
    # Make the API call
    resp = client.service.executeSQLUpdate(query)
    print(resp)
