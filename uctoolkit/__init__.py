# -*- coding: utf-8 -*-
"""
UCToolkit Library
~~~~~~~~~~~~~~~~~

UCToolkit is a Python-based library providing basic connectors for common Cisco UC SOAP APIs
to facilitate DevOps Cisco UC application provisioning.

:copyright: (c) 2018 by Jonathan Els.
:license: MIT, see LICENSE for more details.
"""

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__

from uctoolkit.connectors import (
    UCMAXLConnector
)

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Initialize Package Logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = (
    UCMAXLConnector,
    # UCMControlCenterConnector,
    # UCMRisPortConnector,
    # UCMPerMonConnector,
    # UCMLogCollectionConnector
)
