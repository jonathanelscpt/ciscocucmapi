


__author__ = "Mitch Dawson"
__email__ = "info@ucdevops.com"


import requests
from xml.etree import ElementTree
import time


# CUCM URL's
url11 = 'https://V11CUCM:8443/axl/'
url86 = 'https://V86CUCM:8443/axl/'

# V11 CUCM Headers
headers11query = {'Content-Type': 'text/xml',
                  'SOAPAction': 'CUCM:DB ver=11.0 executeSQLQuery'}
headers11update = {'Content-Type': 'text/xml',
                   'SOAPAction': 'CUCM:DB ver=11.0 executeSQLUpdate'}
                   
# V8.6 CUCM Headers
headers86update = {'Content-Type': 'text/xml',
                   'SOAPAction': 'CUCM:DB ver=8.5 executeSQLUpdate'}
                   
q1 = """select dnorpattern from numplan where fkroutepartition = (select pkid from routepartition where name = "PAR_HOLDING") 
and tkpatternusage = '2' and dnorpattern like '%+442078%'"""


def findextensions():
    """
    Find numbers on cucm 11 cluster in PAR_HOLDING
    :return:
    """
    msg = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/11.0">
           <soapenv:Header/>
           <soapenv:Body>
              <ns:executeSQLQuery sequence="?">
                <sql>{0}
                </sql>
              </ns:executeSQLQuery>
           </soapenv:Body>
        </soapenv:Envelope>""".format(q1)
    # Create the Requests Connection
    post = requests.post(url11, data=msg, headers=headers11query, verify=False, auth=('username', 'password'))
 
    # Parse the response string
    response = ElementTree.fromstring(post.content)
    # Find returned rows
    result = response.iterfind(".//row/*")
    for r in result:
        time.sleep(1.5)
        if r.tag == 'dnorpattern':
            newdn = r.text
            # Take e164 number and take last 4 digits
            olddn = r.text[-4:]
            # Pass e164 number to cluster11 function
            cluster11(newdn)
            # Pass 4 digit number to cluster86 function
            cluster86(olddn)
        
        
def cluster11(dn):
    """
    Move patterns to PAR_RESOURCES
    :param dn:
    :return:
    """
    # Message to Post
    msg = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/11.0">
           <soapenv:Header/>
           <soapenv:Body>
              <ns:executeSQLUpdate sequence="?">
                <sql>update numplan set fkroutepartition = 'd6f7e81b-4364-4403-876a-10cae8d59df8'
                where dnorpattern = "{0}"
                </sql>
              </ns:executeSQLUpdate>
           </soapenv:Body>
        </soapenv:Envelope>""".format(dn)
    # Create the Requests Connection
    post = requests.post(url11, data=msg, headers=headers11update, verify=False, auth=('username', 'password'))
    # Parse the response string
    response = ElementTree.fromstring(post.content)
    # Find returned rows
    result = response.iterfind(".//return/*")
    for i in result:
        if i.tag == 'rowsUpdated':
            if i.text == '1':
                print('#### Successfully moved ' + str(dn) + ' to PAR_RESOURCES ####')
            else:
                print('#### The response indicates no rows were updated for dn ' + str(dn) + ' ####')


def cluster86(dn):
    """
    Move numbers to staging partition on 8.6 cluster
    :param dn:
    :return:
    """
    # Message to Post
    msg = """
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/8.5">
               <soapenv:Header/>
               <soapenv:Body>
                  <ns:executeSQLUpdate sequence="?">
                    <sql>update numplan set fkroutepartition = '61de9659-bc10-fca0-aa5e-81dc4b7e2fe4'
                    where dnorpattern = "{0}"
                    </sql>
                  </ns:executeSQLUpdate>
               </soapenv:Body>
            </soapenv:Envelope>""".format(dn)
    # Create the Requests Connection
    post = requests.post(url86, data=msg, headers=headers86update, verify=False, auth=('username', 'password'))
    # Parse the response string
    response = ElementTree.fromstring(post.content)
    # Find returned rows
    result = response.iterfind(".//return/*")
    for i in result:
        if i.tag == 'rowsUpdated':
            if i.text == '1':
                print('#### Successfully moved ' + str(dn) + ' to staging partition ####')
            else:
                print('#### The response indicates no rows were updated for dn ' + str(dn) + ' ####')


findextensions()
