# -*- coding: utf-8 -*-

import itertools

from .sql import ThinAXL
from .device import (
    Line,
    Phone,
    CtiRoutePoint,
    DeviceProfile,
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
    Css,
    FacInfo,
    HuntList,
    HuntPilot,
    LineGroup
)
from .system import (
    CallManagerGroup,
    DevicePool,
    DateTimeGroup,
    LdapDirectory,
    LdapFilter,
    LdapSyncCustomField
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
    DeviceProfile,
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
    Css,
    FacInfo,
    HuntList,
    HuntPilot,
    LineGroup
]
_system = [
    CallManagerGroup,
    DevicePool,
    DateTimeGroup,
    LdapDirectory,
    LdapFilter,
    LdapSyncCustomField
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
