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


class UserBasicPropertiesMixin(AXLDataModel):
    """A data model mixin for key AXLData User class for ease of use.

    Not intended to be an exhaustive list.  Additional attributes can
    be accessed using the base class __getattr__ method"""

    # @property
    # def uuid(self):
    #     """The AXL object uuid.  Available for all AXL objects"""
    #     return self._axl_data.get('uuid')

    @property
    def userid(self):
        """User userid"""
        return self._axl_data.get('userid')

    @property
    def firstName(self):
        """User first name"""
        return self._axl_data.get('firstName')

    @property
    def lastName(self):
        """User last name"""
        return self._axl_data.get('lastName')

    @property
    def mailid(self):
        """User email address"""
        return self._axl_data.get('mailid')

    @property
    def password(self):
        """User password"""
        return self._axl_data.get('password')

    @property
    def pin(self):
        """User userid"""
        return self._axl_data.get('pin')

    @property
    def telephoneNumber(self):
        """User telephone number"""
        return self._axl_data.get('telephoneNumber')

    @property
    def primaryExtension(self):
        """User primary extension dict with dn and partition"""
        return self._axl_data.get('primaryExtension')

    @property
    def directoryUri(self):
        """User directory URI"""
        return self._axl_data.get('directoryUri')

    @property
    def associatedDevices(self):
        """User list of associated devices"""
        return self._axl_data.get('associatedDevices')

    @property
    def imAndPresenceEnable(self):
        """User IM and Presence enabled boolean"""
        return self._axl_data.get('imAndPresenceEnable')

    @property
    def homeCluster(self):
        """User Home Cluster boolean"""
        return self._axl_data.get('homeCluster')
