# -*- coding: utf-8 -*-
"""AXL User Data Model"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
from .axldata import AXLDataModel


class ThinAXLeBasicPropertiesMixin(AXLDataModel):
    """A data model mixin for Thin AXL"""

    def __str__(self):
        raise NotImplementedError("")

    def __repr__(self):
        raise NotImplementedError("")

    @property
    def sql_response(self):
        """Return sql response table"""
        return self._axl_data
