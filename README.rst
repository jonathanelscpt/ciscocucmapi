========
Overview
========

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/jonathanelscpt/ciscocucmapi/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jonathanelscpt/ciscocucmapi/compare/v0.0.0...master



.. end-badges

Python Wrappers for Cisco CUCM SOAP APIs

* Free software: MIT license

Installation
============

::

    pip install ciscocucmapi

You can also install the in-development version with::

    pip install https://github.com/jonathanelscpt/ciscocucmapi/archive/master.zip


Documentation
=============


https://ciscocucmapi.readthedocs.io/


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
