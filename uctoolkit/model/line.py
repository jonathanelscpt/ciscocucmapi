# -*- coding: utf-8 -*-
"""CUCM AXL Directory Number Data Model"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

from .axldata import AXLDataModel


class LineBasicPropertiesMixin(AXLDataModel):
    """A data model mixin for key AXLData Line class for ease of use.

    Not intended to be an exhaustive list.  Additional attributes can
    be accessed using the base class __getattr__ method
    """

    @property
    def pattern(self):
        """DN Pattern"""
        return self._axl_data.get('pattern')

    @property
    def description(self):
        """DN description"""
        return self._axl_data.get('description')

    @property
    def routePartitionName(self):
        """DN Route Partition Name"""
        return self._axl_data.get('routePartitionName')

    @property
    def alertingName(self):
        """DN Alerting Name"""
        return self._axl_data.get('alertingName')

    @property
    def asciiAlertingName(self):
        """DN ASCII Alerting Name"""
        return self._axl_data.get('asciiAlertingName')

    @property
    def voiceMailProfileName(self):
        """DN Voicemail Profile Name"""
        return self._axl_data.get('voiceMailProfileName')

    @property
    def callPickupGroupName(self):
        """DN Call Pickup Group Name"""
        return self._axl_data.get('callPickupGroupName')

    @property
    def callForwardAll(self):
        """DN Call Forward All dictionary"""
        return self._axl_data.get('callForwardAll')

    @property
    def callForwardBusy(self):
        """DN Call Forward Busy dictionary"""
        return self._axl_data.get('callForwardBusy')

    @property
    def callForwardBusyInt(self):
        """DN Call Forward Busy Internal dictionary"""
        return self._axl_data.get('callForwardBusyInt')

    @property
    def callForwardNoAnswer(self):
        """DN Call Forward No Answer dictionary"""
        return self._axl_data.get('callForwardNoAnswer')

    @property
    def callForwardNoAnswerInt(self):
        """DN Call Forward No Answer Internal dictionary"""
        return self._axl_data.get('callForwardNoAnswerInt')

    @property
    def callForwardNotRegistered(self):
        """DN Call Forward Unregistered dictionary"""
        return self._axl_data.get('callForwardNotRegistered')

    @property
    def callForwardNotRegisteredInt(self):
        """DN Call Forward No Answer Internal dictionary"""
        return self._axl_data.get('callForwardNotRegisteredInt')
