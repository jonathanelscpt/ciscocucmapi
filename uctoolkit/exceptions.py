# -*- coding: utf-8 -*-
"""UCToolkit Exceptions"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *


class UCToolkitException(Exception):
    """Generic package Exception Container"""

    def __init__(self, message=''):
        super(Exception, self).__init__(message)
        self.message = message

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.message)


class ServiceProxyError(UCToolkitException):
    """Unable to create ServiceProxy object with given parameters"""


class UCToolkitConnectionException(UCToolkitException):
    """Exceptions for invalid connection params"""


class AXLError(UCToolkitException):
    """Bubble error received from AXL API"""


class AXLAttributeError(AXLError):
    """Invalid attribute for AXL API endpoint"""


class AXLMethodDoesNotExist(AXLError):
    """Method override for scenarios where certain methods do not exist of an api endpoint"""


class IllegalSQLStatement(AXLError):
    """Illegal SQL Statement response from CUCM"""


class IllegalSearchCriteria(AXLError):
    """Supplied Search Criteria are invalid for AXL API Call"""
