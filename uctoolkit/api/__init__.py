# -*- coding: utf-8 -*-

import itertools

from .sql import ThinAXL
from .device import (
    Line,
    Phone,
    CtiRoutePoint,
)
from .user import User
from .dialplan import (
    RoutePartition,
    CallPickupGroup,
    AarGroup,
    DirectedCallPark,
    CallPark,
    CalledPartyTransformationPattern,
    CallingPartyTransformationPattern,
    CmcInfo,
    Css
)
from .system import (
    CallManagerGroup,
    DevicePool
)
from .media import (
    ConferenceBridge,
)

_sql = [
    ThinAXL
]
_devices = [
    Line,
    Phone,
    CtiRoutePoint,
]
_user = [
    User,
]
_dial_plan = [
    RoutePartition,
    CallPickupGroup,
    AarGroup,
    DirectedCallPark,
    CallPark,
    CalledPartyTransformationPattern,
    CallingPartyTransformationPattern,
    CmcInfo,
    Css
]
_system = [
    CallManagerGroup,
    DevicePool,
]
_media = [
    ConferenceBridge
]
_all = [
    _sql,
    _user,
    _devices,
    _dial_plan,
    _system
]

__all__ = list(itertools.chain.from_iterable(_all))
