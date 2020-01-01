==============
Cisco CUCM API
==============

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/ciscocucmapi/badge/?style=flat
    :target: https://readthedocs.org/projects/ciscocucmapi
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/jonathanelscpt/ciscocucmapi.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/jonathanelscpt/ciscocucmapi

.. |codecov| image:: https://codecov.io/gh/jonathanelscpt/ciscocucmapi/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jonathanelscpt/ciscocucmapi

.. |version| image:: https://img.shields.io/pypi/v/ciscocucmapi.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/ciscocucmapi

.. |wheel| image:: https://img.shields.io/pypi/wheel/ciscocucmapi.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/ciscocucmapi

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ciscocucmapi.svg
    :alt: Supported versions
    :target: https://pypi.org/project/ciscocucmapi

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ciscocucmapi.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/ciscocucmapi

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/ciscocucmapi/v0.0.2.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/ciscocucmapi/compare/v0.0.2...master



.. end-badges

Python Wrappers for Cisco CUCM SOAP APIs

* Free software: MIT license


Overview
========

The ciscocucmapi package is inspired by the most excellent `webexteamssdk <https://github.com/CiscoDevNet/webexteamssdk>`__
Python API wrapper for Cisco Spark.  The library wraps a `python-zeep <https://github.com/mvantellingen/python-zeep>`__
client to manage CUCM SOAP connections (specifically for AXL) and CRUD operations for common API endpoints.

* Simplified Pythonic wrappings of Cisco UC SOAP APIs
* :code:`python-zeep`-based client under the hood - much faster than :code:`suds`.  WSDL caching is enabled by default.
* Complete abstraction of AXL SOAP API - no xml!
* Native Python tooling includes:
    * Native returned AXL data objects modelled with a :code:`dict`-like interface and characteristics
    * xml order is honoured due to :code:`OrderedDict` implementation
    * AXL crud operations supported using both Python objects and native AXL calling requirements
* Transparent sourcing of AXL credentials from local environment variables
* Easy, template-able reading and writing to JSON objects, making Cisco UC DevOps implementations a reality

Documentation
=============

https://ciscocucmapi.readthedocs.io/

Installation
============

At the command line::

    pip install ciscocucmapi

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/ciscocucmapi/archive/master.zip


Quick Start
===========

.. code-block:: python

    from ciscocucmapi import UCMAXLConnector
    import json


    axl = UCMAXLConnector(username='axl', password='password', fqdn='192.168.99.99')

    # adding phones
    ipphone_attributes = {
        "name": "SEPDEADDEADDEAD",
        "product": "Cisco 8821",
        "devicePoolName": "US_NYC_DP",
    }
    axl.phone.add(**ipphone_attributes)

    # api endpoints can be created prior to invoking axl method-calling for pre-processing
    new_bot_device = axl.phone.create()
    # very useful API template development!
    with open("/path/to/templates/phone.json", "w") as _:
        json.dump(axl.phone.model(), _, indent=4)

    # getting existing phones with null-string dicts or lists of `returnedTags`
    dead_device = axl.phone.get(name="SEPDEADDEADDEAD",
                                returnedTags={"name": "", "devicePoolName": "",
                                              "callingSearchSpaceName": ""})
    beefy_device = axl.phone.get(name="SEPBEEFBEEFBEEF",
                                 returnedTags=["name", "devicePoolName", "callingSearchSpaceName"])

    # listing phones by name
    nyc_bot_attrs = {
        "name": "BOT%",
        "devicePoolName": "US_NYC%",
        "callingSearchSpaceName": "US_%"
    }
    nyc_bot_devices = axl.phone.list(searchCriteria=nyc_bot_attrs,
                                     returnedTags=["name", "description", "lines"])
    # implicit "return all" available for `searchCriteria` and `returnedTags`
    # use sparingly for large data sets!
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
                     locationName=botuser15.locationName)

    # deleting a phone
    axl.phone.remove(uuid=botuser15.uuid)

    # Thin AXL sql querying and execution also available
    numplan = axl.sql.query("SELECT * FROM numplan")
    directory_numbers = [row['dnorpattern'] for row in numplan]
    numplan.csv(destination_path="/path/to/datadump/numplan.csv")  # pathlib also supported


Donate
======

If this library has helped you, or if you would like to support future development, donations are most welcome:

==============  ==========================================
Cryptocurrency  Address
==============  ==========================================
 **BTC**        38c7QWggrB2HLUJZFmhAC2zh4t8C57c1ec
 **ETH**        0x01eD3b58a07c6d005281Db76e6c1AE2bfF2226AD
==============  ==========================================


Support
=======

I'm open to discussing ad-hoc commercial support or custom DevOps implementations. Please contact me at
jonathanelscpt@gmail.com for more information. Note that asking questions or reporting bugs via this e-mail address
may not receive responses. Please rather create GitHub issues for this.
