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

.. |codecov| image:: https://codecov.io/github/jonathanelscpt/ciscocucmapi/coverage.svg?branch=master
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/ciscocucmapi/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/ciscocucmapi/compare/v0.0.1...master



.. end-badges

Python Wrappers for Cisco CUCM SOAP APIs

* Free software: MIT license


Features
========

The ciscocucmapi package is inspired by the most excellent `webexteamssdk <https://github.com/CiscoDevNet/webexteamssdk>`__
Python API wrapper for Cisco Spark.  The library wraps a `python-zeep <https://github.com/mvantellingen/python-zeep>`__
client to manage CUCM SOAP connections (specifically for AXL) and CRUD operations for common API endpoints.


Overview
========

* Simplified Pythonic wrappings of Cisco UC SOAP APIs
* :code:`python-zeep`-based client under the hood - much faster than :code:`suds`.  WSDL caching is enabled by default.
* Complete abstraction of AXL SOAP API - no xml!
* Native Python tooling includes:
    * Native returned AXL data objects modelled with a :code:`dict`-like interface and characteristics
    * xml order is honoured due to :code:`OrderedDict` implementation
    * AXL crud operations supported using both Python objects and native AXL calling requirements
* Transparent sourcing of AXL credentials from local environment variables
* Easy, template-able reading and writing to JSON objects, making Cisco UC DevOps implementations a reality


Installation
============

::

    pip install ciscocucmapi

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/ciscocucmapi/archive/master.zip


Documentation
=============

https://ciscocucmapi.readthedocs.io/


Quick Start
===========

.. code-block:: python

    from ciscocucmapi import UCMAXLConnector
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




Connector Environment Variables
===============================

 The following env vars are supported for ease of use:

 - :code:`AXL_USERNAME`
 - :code:`AXL_PASSWORD`
 - :code:`AXL_WSDL_URL`
 - :code:`AXL_FQDN`


AXL WSDL
========

The package includes the AXL wsdl for ease of use.  The schema will be updated regularly to match the latest CUCM
releases.  By default, unless an AXL version is specified, the :code:`current` WSDL will be used.

Due to the strictness of :code:`python-zeep`'s WSDL and .xsd parsing, numerous AXL defects have been encountered during
development and testing.  As a result, the packaged WSDL and .xsd files *may* include patches to mitigate defects
where applicable.  Known AXL defects which have resulted in patches are catalogued in
AXL_DEFECTS.rst.

If you require a more up-to-date WSDL, or are uncomfortable with using a patched schema, all :code:`UCSOAPConnector`
accept a direct path to a local WSDL file as input.


API Endpoint Support
====================

Not all API Endpoints are supported, as API and data models are required to mitigate inconsistencies in the
AXL API.  If you'd like to extend API support, please create a pull request, or raise a GitHub issue and I'll add
an enhancement.

I am not currently back-testing all version support, and do not intend to test against pre-9 UCM versions.  The package
has been developed primarily against UCM 11.5.  If any API definitions interfere with the backwards compatibility of
AXL for prior versions, please raise a GitHub issue and I will address this.


Supported Languages and AXL Versions
====================================

- Currently only Python 3.6+ is supported.   There are no plans to support Python 2.7.
- All AXL versions *should* be supported, however only 11.5 has been currently tested.  All AXL data models include
  static metadata on mandatory params for :code:`add` calls.  It  is not expected that these should change across AXL
  schema versions.  Please raise a defect if you encounter any issues.
- Other API methods should contain reliable schema-driven metadata and attributes.


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


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
