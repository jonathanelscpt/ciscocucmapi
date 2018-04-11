# -*- coding: utf-8 -*-
"""AXL Data Model Classes"""

from collections import defaultdict

from .axldata import AXLDataModel


class ThinAXLDataModel(AXLDataModel):
    """Cisco CUCM Thin AXL data model."""

    def __str__(self):
        # todo
        raise NotImplementedError("")

    def __repr__(self):
        raise NotImplementedError("")

    @property
    def sql_response(self):
        """Return sql response table"""
        return self._axl_data


class PhoneDataModel(AXLDataModel):
    """Phone data model."""


class LineDataModel(AXLDataModel):
    """Line data model."""


class UserDataModel(AXLDataModel):
    """CUCM User data model."""


class RoutePartitionDataModel(AXLDataModel):
    """RoutePartition data model."""


class CallPickupGroupDataModel(AXLDataModel):
    """CallPickupGroup data model."""


class AarGroupDataModel(AXLDataModel):
    """AarGroup data model."""


class CallManagerGroupDataModel(AXLDataModel):
    """CUCM Group data model"""


class DirectedCallParkDataModel(AXLDataModel):
    """DirectedCallPark data model"""


class CallParkDataModel(AXLDataModel):
    """CallPark data model"""


class CalledPartyTransformationPatternDataModel(AXLDataModel):
    """CalledPartyTransformationPattern data model"""


class CallingPartyTransformationPatternDataModel(AXLDataModel):
    """CallingPartyTransformationPattern data model"""


class CmcInfoDataModel(AXLDataModel):
    """CmcInfo data model"""


class ConferenceBridgeDataModel(AXLDataModel):
    """ConferenceBridge data model"""


class CssDataModel(AXLDataModel):
    """Css data model"""


class CtiRoutePointDataModel(AXLDataModel):
    """Css data model"""


class DevicePoolDataModel(AXLDataModel):
    """Device Pool data model"""


axl_data_models = defaultdict(
    lambda: AXLDataModel,
    sql=ThinAXLDataModel,
    phone=PhoneDataModel,
    user=UserDataModel,
    line=LineDataModel,
    route_partition=RoutePartitionDataModel,
    call_pickup_group=CallPickupGroupDataModel,
    aar_group=AarGroupDataModel,
    callmanager_group=CallManagerGroupDataModel,
    directed_call_park=DirectedCallParkDataModel,
    call_park=CallParkDataModel,
    called_party_xform_pattern=CalledPartyTransformationPatternDataModel,
    calling_party_xform_pattern=CallingPartyTransformationPatternDataModel,
    cmc=CmcInfoDataModel,
    conference_bridge=ConferenceBridgeDataModel,
    css=CssDataModel,
    cti_route_point=CtiRoutePointDataModel,
    device_pool=DevicePoolDataModel
)


def axl_factory(model, axl_data):
    """Factory function for creating AXLData objects.

    :param model: (basestring) Data model to use when creating the AXLData object
    :param axl_data: dictionary data used to initialize the AXLData object
    :return: (AXLData) object
    :raises TypeError: If the json_data parameter is not a JSON string or dictionary.
    """
    return axl_data_models[model](axl_data)
