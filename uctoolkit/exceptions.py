# -*- coding: utf-8 -*-
"""UCToolkit Exceptions"""


class UCToolkitException(Exception):
    """Generic package Exception Container"""

    def __init__(self, message=''):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return f'{self.__class__.__name__}({self.message})'


class AXLAttributeError(UCToolkitException):
    """Invalid attribute for AXL API endpoint"""


class AXLFault(UCToolkitException):
    """Bubble error received from AXL API in zeep Fault"""


class IllegalSQLStatement(UCToolkitException):
    """Illegal SQL Statement response from CUCM"""


class ParseError(UCToolkitException):
    """Unable to parse AXL object"""
