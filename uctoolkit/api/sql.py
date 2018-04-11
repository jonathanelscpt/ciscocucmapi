# -*- coding: utf-8 -*-
"""CUCM AXL Thin AXL API."""

from .abstract import AbstractThinAXLAPI


class ThinAXL(AbstractThinAXLAPI):
    """Cisco CUCM ThinAXL API.
    Wraps the CUCM AXL API and exposes the API as native Python
    methods that return native Python objects.
    """
    _OBJECT_TYPE = 'sql'

    @property
    def object_type(self):
        return self._OBJECT_TYPE
