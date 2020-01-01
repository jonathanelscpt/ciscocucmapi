===========
AXL Support
===========

.. inclusion-marker-do-not-remove

WSDL
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
