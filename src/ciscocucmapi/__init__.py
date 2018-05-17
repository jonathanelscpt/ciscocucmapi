# -*- coding: utf-8 -*-
"""ciscocucmapi Library


ciscocucmapi is a Python-based library providing basic connectors for common Cisco UC SOAP APIs
to facilitate DevOps Cisco UC application provisioning.

:copyright: (c) 2018 by Jonathan Els.
:license: MIT, see LICENSE for more details.
"""

import logging

from .connectors import (
    UCMAXLConnector
)


# Initialize Package Logging - set default logging handler to avoid "No handler found" warnings.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = [
    'UCMAXLConnector',
    # 'UCMControlCenterConnector',
    # 'UCMRisPortConnector',
    # 'UCMPerfMonConnector',
    # 'UCMLogCollectionConnector'
]
