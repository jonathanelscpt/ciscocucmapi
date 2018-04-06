# -*- coding: utf-8 -*-


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import itertools

from .sql import ThinAXL
from .device import (
    Line,
    Phone
)
from .dialplan import (
    RoutePartition
)

_sql = [
    ThinAXL
]
_devices = [
    Line,
    Phone,
]
_dial_plan = [
    RoutePartition
]

_apis = [
    _sql,
    _devices,
    _dial_plan
]

__all__ = list(itertools.chain.from_iterable(_apis))
