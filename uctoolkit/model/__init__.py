# -*- coding: utf-8 -*-
"""AXL Data Model Classes"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

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
    """Cisco CUCM AXL Phone data model."""


class LineDataModel(AXLDataModel):
    """Cisco CUCM AXL Line data model."""


class UserDataModel(AXLDataModel):
    """Cisco CUCM AXL User data model."""


class RoutePartitionDataModel(AXLDataModel):
    """Cisco CUCM AXL RoutePartition data model."""


class CallPickupGroupDataModel(AXLDataModel):
    """Cisco CUCM AXL CallPickupGroup data model."""


axl_data_models = defaultdict(
    lambda: AXLDataModel,
    sql=ThinAXLDataModel,
    phone=PhoneDataModel,
    user=UserDataModel,
    line=LineDataModel,
    route_partition=RoutePartitionDataModel,
    call_pickup_group=CallPickupGroupDataModel
)


def axl_factory(model, axl_data):
    """Factory function for creating AXLData objects.

    :param model: (basestring) Data model to use when creating the AXLData object
    :param axl_data: dictionary data used to initialize the AXLData object
    :return: (AXLData) object
    :raises TypeError: If the json_data parameter is not a JSON string or dictionary.
    """
    return axl_data_models[model](axl_data)
