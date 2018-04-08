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
from .user import User
from .dialplan import (
    RoutePartition,
    CallPickupGroup
)

_sql = [
    ThinAXL
]
_devices = [
    Line,
    Phone,
]
_user = [
    User
]
_dial_plan = [
    RoutePartition,
    CallPickupGroup,
]

_all = [
    _sql,
    _user,
    _devices,
    _dial_plan
]

__all__ = list(itertools.chain.from_iterable(_all))
