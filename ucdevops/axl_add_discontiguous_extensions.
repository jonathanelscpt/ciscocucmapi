#!/usr/bin/env python

__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"


from suds.client import Client
from suds.xsd.doctor import ImportDoctor
from suds.xsd.doctor import Import
from suds.cache import NoCache


tns = 'http://www.cisco.com/AXLAPIService/'
imp = Import('http://schemas.xmlsoap.org/soap/encoding/',
             'http://schemas.xmlsoap.org/soap/encoding/')
imp.filter.add(tns)

# Define Authentication Credentials for Cluster
username = 'username'
password = 'password'
# Define AXL URL for Cluster
url = 'https://CUCM:8443/axl/'
# Define WSDL Location
wsdl = 'file:///C:/PathTo/AXLAPI.wsdl'

# Create Suds Client Object
client = Client(location=url, url=wsdl, faults=False, username=username,
                password=password, plugins=[ImportDoctor(imp)],cache=NoCache()
)

# Define our line object creation function
def lineObject(line):
    """
    Function returns a dictionary object of line attributes and values
    """
    # Create an empty dictionary
    lineObject = {}
    # Create a variable to be used to populate the description,
    # alertingName and asciiAlertingName variables
    description = 'Spare Denver Ext 12.10.17'
    # Format the line value, in this example we prepend '\+' as
    # e164 format is required
    lineObject['pattern'] = '\+' + line
    # Set Urgent Priority
    lineObject['patternUrgency'] = 't'
    # Assign the description variable above
    lineObject['description'] = description
    lineObject['alertingName'] = description
    lineObject['asciiAlertingName'] = description
    # Assign the partition of where the line should reside
    lineObject['routePartitionName'] = 'PAR_RESOURCES'
    # Assign the required Line CSS
    lineObject['shareLineAppearanceCssName'] = 'CSS_US_DEN_839_LINE_IN'
    # Create Call Forward settings object
    cFwdNoVMNoDest = {
        'forwardToVoiceMail': 'f',
        'callingSearchSpaceName': 'CSS_US_DEN_839_LINE_N',
        'destination': ''
    }
    # Create callForward object values
    lineObject['callForwardAll'] = cFwdNoVMNoDest
    lineObject['callForwardBusy'] = cFwdNoVMNoDest
    lineObject['callForwardBusyInt'] = cFwdNoVMNoDest
    lineObject['callForwardNoAnswer'] = cFwdNoVMNoDest
    lineObject['callForwardNoAnswerInt'] = cFwdNoVMNoDest
    lineObject['callForwardNoCoverage'] = cFwdNoVMNoDest
    lineObject['callForwardNoCoverageInt'] = cFwdNoVMNoDest
    lineObject['callForwardOnFailure'] = cFwdNoVMNoDest
    lineObject['callForwardNotRegistered'] = cFwdNoVMNoDest
    lineObject['callForwardNotRegisteredInt'] = cFwdNoVMNoDest
    # Return the lineObject
    return lineObject

# The input list consists of a single column of values in a text file
# Open the input list of numbers, Read it then split on new line
file = open('lines.txt', 'r').read().split('\n')
# Loop through the lines
for line in file:
    # Create a new line object
    lineObj = lineObject(line)
    # Post the new line object to the AXL API
    x = client.service.addLine(lineObj)
    # If the request was successful,
    # the response will return a tuple with status code 200 as the first element
    if x[0] == 200:
        print(
            'Sucessfully added Line {}'.format(lineObj['pattern'])
        )
    else:
        # Anything other than 200 indicates an error
        print(
            'Error adding line {}'.format(lineObj['pattern'])
        )
        print(x[1])
  
