# Cisco UC Toolkit

The uctoolkit package is inspired by the most excellent [ciscosparkapi](https://github.com/CiscoDevNet/ciscosparkapi)
Python API wrapper for Cisco Spark.  The library wraps a 
[python-zeep](https://github.com/mvantellingen/python-zeep) client to create and manage 
AXL connections and provide CRUD operations for common API endpoints.


## Features

 - Simplified Pythonic wrapping of Cisco UC SOAP APIs
 - `python-zeep`-based client under the hood - much faster than `suds`
 - Complete abstraction from AXL SOAP API - no xml!
 - Native Python tooling includes:
   - Native returned AXL data objects modelled with a `dict`-like interface and characteristics
   - xml order is honoured due to `OrderedDict` implementation
   - AXL crud operations supported using both Python objects and native AXL calling requirements
 - Transparent sourcing of AXL credentials from local environment variables
 - Easy, template-able reading and writing to JSON objects, making Cisco UC DevOps implementations a reality
 
  
## Installation

Installing and upgrading `uctoolkit` is done with `pip`:

**Installing via PIP**

    $ pip install uctoolkit

**Upgrading via PIP**

    $ pip install uctoolkit --upgrade
    

## Quick Start

```python
from uctoolkit import UCMAXLConnector
import json


axl = UCMAXLConnector()  # env vars for connection params

# adding phones
bot_device_attributes = {
    "name": "SEPDEADDEADDEAD",
    "product": "Cisco 8821",
    "devicePoolName": "US_NYC_DP",
}
axl.phone.add(**bot_device_attributes)

# api endpoints can be created prior to invoking axl method-calling for pre-processing
new_bot_device = axl.phone.create()
# very useful API template development!
with open("/path/to/templates/phone.json", "w") as _:
    json.dump(axl.phone.model(), _, indent=4)

# getting existing phones with null-string dicts or lists of `returnedTags`
dead_device = axl.phone.get(name="SEPDEADDEADDEAD", 
                            returnedTags={"name": "", "devicePoolName": "", "callingSearchSpaceName": ""}
                            )
beefy_device = axl.phone.get(name="SEPBEEFBEEFBEEF", 
                            returnedTags=["name", "devicePoolName", "callingSearchSpaceName"]
                             )

# listing phones by name
nyc_bot_attrs = {
    "name": "SEP%",
    "devicePoolName": "US_NYC%",
    "callingSearchSpaceName": "US_%"
}
nyc_bot_devices = axl.phone.list(searchCriteria=nyc_bot_attrs,
                                 returnedTags=["name", "description", "lines"]
                                 )
# implicit "return all" available for `searchCriteria` and `returnedTags` - use sparingly for large data sets!
all_devices = axl.phone.list()

# property-like getters and setters
botuser15 = next(filter(lambda person: person.name == 'BOTUSER015', nyc_bot_devices))
botuser15.callingSearchSpaceName = "US_NYC_NATIONAL_CSS"

# updating a phone
botuser15.callingSearchSpaceName = "US_NYC_INTERNATIONAL_CSS"
botuser15.newName = "BOTJONELS"
botuser15.locationName = "Hub_None"
axl.phone.update(name=botuser15.name,
                 newName=botuser15.newName,
                 callingSearchSpaceName=botuser15.callingSearchSpaceName,
                 locationName=botuser15.locationName
                 )

# deleting a phone
axl.phone.remove(uuid=botuser15.uuid) 

# Thin AXL sql querying and execution also available
numplan = axl.sql.query("SELECT * FROM numplan")
directory_numbers = [row['dnorpattern'] for row in numplan]
numplan.csv(destination_path="/path/to/datadump/numplan.csv")  # pathlib also supported
```


### Connector Environment Variables
 
 The following env vars are supported for easy of use:
 
 - `AXL_USERNAME`
 - `AXL_PASSWORD`
 - `AXL_WSDL_URL`
 - `AXL_FQDN`


### AXL WSDL

The package includes the AXL wsdl for ease of use.  The schema will be updated regularly to match the latest CUCM
releases.  By default, unless an AXL version is specified, the `current` WSDL will be used.

Due to the strictness of `python-zeep`'s WSDL and .xsd parsing, numerous AXL defects have been encountered during
development and testing.  As a result, the packaged WSDL and .xsd files *may* include patches to mitigate defects
where applicable.  Known AXL defects which have resulted in patches are catalogued in `AXL_DEFECTS.md`.  

If you require a more up-to-date WSDL, or are uncomfortable with using a patched schema, all `UCSOAPConnector`
accept a direct path to a local WSDL file as input.


### API Endpoint Support

Not all API Endpoints are supported, as API and data models are required to mitigate inconsistencies in the 
AXL API.  If you'd to extend API support, please create a pull request, or raise a GitHub issue and I'll add
an enhancement.

I am not currently back-testing all version support, and do not intend to test against pre-9 UCM versions.  The package
has been developed primarily against UCM 11.5.  If any API definitions interfere with the backwards compatibility of
AXL for prior versions, please raise a GitHub issue and I will address this.

 
### Supported Languages and AXL Versions

 - Currently only Python 3.6 is supported.   Python 2.7 not planned for support in the short-term.
 - All AXL versions *should* be supported, however only 11.5 has been currently tested.  All
   AXL data models include static metadata on mandatory params for `add` calls.  It  is 
   not expected that these should change across AXL schema versions.  Please raise a defect 
   if you encounter any issues.
 - Other API methods should contain reliable schema-driven metadata and attributes.
 
 
## Donate
 
If this library has helped you, or if you would like to support future development, 
donations are most welcome:

| Cryptocurrency  | Address |
| :---:  | :---  |
| **BTC** | 3EFVaakujecqhEmNkah5Q5gkpNbyy251os |
| **ETH** | 0xb44b637e99b32b9f12ba9430ff823cabb3ca7db5 |
| **BCH** | 38YJXxgchDgSjzd8b91LkmcbQSy1q6ruYx |
| **LTC** | MTJKDiS8Jv9qG9iYGWHyhTrAL6oynFwQw1 |
 
 
## Support
 
I'm open to discussing ad-hoc commercial support or custom DevOps implementations.
Please contact me at [jonathanelscpt@gmail.com](mailto:jonathanelscpt@gmail.com) for more information. 
Note that asking questions or reporting bugs via this e-mail address may not receive responses.
Please rather create GitHub issues for this.
 