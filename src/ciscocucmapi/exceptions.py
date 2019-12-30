"""ciscocucmapi exceptions"""


class CiscoCUCMAPIException(Exception):
    """Generic package Exception Container"""

    def __init__(self, message=''):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return f'{self.__class__.__name__}({self.message})'


class AXLAttributeError(CiscoCUCMAPIException):
    """Invalid attribute for AXL API endpoint"""


class AXLFault(CiscoCUCMAPIException):
    """Bubble error received from AXL API in zeep Fault"""


class IllegalSQLStatement(CiscoCUCMAPIException):
    """Illegal SQL Statement response from CUCM"""


class ParseError(CiscoCUCMAPIException):
    """Unable to parse AXL object"""
