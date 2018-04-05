# -*- coding: utf-8 -*-
"""CUCM AXL Thin AXL API."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from . import AbstractThinAXLAPI


class ThinAXL(AbstractThinAXLAPI):
    """Cisco CUCM Phones API.
    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'thin_axl'
    _RETURN_OBJECT_NAME = 'row'

    def __init__(self, client, object_factory):
        """
        Initialize a new ThinAXLAPI object with the provided AXL client.

        :param client: zeep SOAP AXL client for API calls to CUCM's SOAP interface
        :param object_factory: factory function for instantiating SQL data models objects
        :raises TypeError: If parameter types are invalid.
        """
        super(ThinAXL, self).__init__(client, object_factory)

    def object_type(self):
        return self._OBJECT_TYPE

    def return_object_name(self):
        return self._RETURN_OBJECT_NAME
