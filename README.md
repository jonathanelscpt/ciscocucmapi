# Cisco UC Toolkit

The uctoolkit package is inspired by the most excellent [ciscosparkapi](https://github.com/CiscoDevNet/ciscosparkapi)
Python API wrapper for Cisco Spark.  The library uses a custom 
[python-zeep](https://github.com/mvantellingen/python-zeep) connector for AXL connections.


## Features

 - Simplified Pythonic wrapping of Cisco UC SOAP-based APIs
 - Complete abstraction from AXL SOAP API
 - Native Python tooling includes:
   - API interactions using native Python tools
   - Native returned AXL data objects modelled with `dict`-like characteristics
   - AXL crud operations supported using both Python objects and native AXL calling requirements
 - Transparent sourcing of AXL credentials from local environment variables
 
  
## Installation

Installing and upgrading uctoolkit is done with pip:

**Installing via PIP**

    $ pip install uctoolkit

**Upgrading via PIP**

    $ pip install uctoolkit --upgrade
    

## Quick Start

```python
from uctoolkit import UCMAXLConnector


axl = UCMAXLConnector()  # env vars for connection params

# list phones by name
bot_names = {
    "name": "BOT%"
}
returned_tags = {
    "name": "",
    "description": "",
    "lines": ""
}
bot_devices = axl.phones.list(search_criteria=bot_names, returned_tags=returned_tags)

# accessing and updating phone attributes
botuser15 = next(filter(lambda person: person.name == 'BOTUSER015', bot_devices))
botuser15.callingSearchSpaceName = "US_NYC_NATIONAL_CSS"

# updating a phone using native api
botuser15.callingSearchSpaceName = "US_NYC_INTERNAL_CSS"
botuser15.newName = "BOTJONATHANELS"  # does not update botuser15.name attribute
botuser15.locationName = "US_NYC_LOC"
kwargs = {
    "newName": botuser15.newName,
    "locationName": botuser15.locationName
}
axl.phones.update(name=botuser15.name, **kwargs)
# updating a phone from data model object
axl.phones.update(botuser15)


# deleting a phone
axl.phones.remove(botuser15)  # using existing phone object
axl.phones.remove(name="BOTUSER015")  # native API call


# execute sql query
numplan = axl.sql.query("SELECT * FROM numplan")
dns = [_['dnorpattern'] for _ in numplan]

```


 ## Connector Environment Variables
 
 The following env vars are supported for easy of use:
 
 - AXL_USERNAME
 - AXL_PASSWORD
 - AXL_WSDL_URL
 - AXL_FQDN

 
## Supported Languages and AXL Versions

 - Currently only Python 3.6 tested.
 - Python 2.7 planned, but not a current priority
 - All AXL versions should be supported, however only 11.5 has been currently tested.
 
 
 ## Donate
 
If this library has helped you, or if you would like to support future development, please feel free to donate:

 - BTC: xxxxxxxxxxxxxxx
 - ETH: xxxxxxxxxxxxxxx
 
 # Support
 
 I'm also willing to discuss ad-hoc commercial support or DevOps implementations.
 Please contact me at [jonathanelscpt@gmail.com](mailto:jonathanelscpt@gmail.com) for more information. 
 Note that asking questions or reporting bugs via this e-mail address may not receive responses.
 Please create GitHub issues for this.
 