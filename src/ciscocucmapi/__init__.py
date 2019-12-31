"""ciscocucmapi Library


ciscocucmapi is a Python-based library providing basic connectors for common Cisco UC SOAP APIs
to facilitate DevOps Cisco UC application provisioning.

:copyright: (c) 2018 by Jonathan Els.
:license: MIT, see LICENSE for more details.
"""

# Set default logging handler to avoid "No handler found" warnings.
import logging

from ciscocucmapi.connectors import UCMAXLConnector

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


__version__ = '0.0.2'


# Initialize Package Logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
