# -*- coding: utf-8 -*-
"""AXL Phone Data Model"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
from .axldata import AXLDataModel


class PhoneBasicPropertiesMixin(AXLDataModel):
    """A data model mixin for key AXLData Phone class for ease of use.

    Not intended to be an exhaustive list.  Additional attributes can
    be accessed using the base class __getattr__ method
    """

    # @property
    # def uuid(self):
    #     """The AXL object uuid.  Available for all AXL objects"""
    #     return self._axl_data.get('uuid')

    # @property
    # def name(self):
    #     """Phone Device Name"""
    #     return self._axl_data.get('name')
    #
    # @property
    # def description(self):
    #     """Phone description"""
    #     return self._axl_data.get('description')
    #
    #
    # @property
    # def ownerUserName(self):
    #     """Phone Owner UserID"""
    #     return self._axl_data.get('ownerUserName')
    #
    # @property
    # def product(self):
    #     """Phone product"""
    #     return self._axl_data.get('product')
    #
    # @property
    # def p_class(self):
    #     """Phone class.
    #     Attribute renamed due to shadow use"""
    #     return self._axl_data.get('class')
    #
    # @property
    # def protocol(self):
    #     """Phone protocol."""
    #     return self._axl_data.get('protocol')
    #
    # @property
    # def callingSearchSpaceName(self):
    #     """Phone CSS name."""
    #     return self._axl_data.get('callingSearchSpaceName')
    #
    # @property
    # def devicePoolName(self):
    #     """Phone Device Pool name."""
    #     return self._axl_data.get('devicePoolName')
    #
    # @property
    # def lines(self):
    #     """Phone lines dictionary.
    #     Includes:
    #     - index
    #     - label
    #     - display
    #     - dirn: pattern, routePartitionName
    #     - displayAscii
    #     - callInfoDisplay
    #     - e164Mask
    #     - etc..."""
    #     return self._axl_data.get('lines')
    #
    # @property
    # def phoneTemplateName(self):
    #     """Phone Phone Button Template name"""
    #     return self._axl_data.get('phoneTemplateName')
    #
    # @property
    # def softkeyTemplateName(self):
    #     """Phone list of IP Phone Services"""
    #     return self._axl_data.get('softkeyTemplateName')
    #
    # @property
    # def speeddials(self):
    #     """Phone list of speed dials"""
    #     return self._axl_data.get('speeddials')
    #
    # @property
    # def busyLampFields(self):
    #     """Phone list of BLFs"""
    #     return self._axl_data.get('busyLampFields')
    #
    # @property
    # def services(self):
    #     """Phone list of IP Phone Services"""
    #     return self._axl_data.get('services')
    #
    # @property
    # def enableExtensionMobility(self):
    #     """Phone enableExtensionMobility boolean"""
    #     return self._axl_data.get('enableExtensionMobility')
