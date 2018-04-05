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
from .line import LineBasicPropertiesMixin
from .phone import PhoneBasicPropertiesMixin
from .user import UserBasicPropertiesMixin
from .thin_axl import ThinAXLeBasicPropertiesMixin


class ThinAXLDataModel(ThinAXLeBasicPropertiesMixin):
    """Cisco CUCM Thin AXL data model."""


class PhoneDataModel(PhoneBasicPropertiesMixin):
    """Cisco CUCM AXL Phone data model."""


class LineDataModel(LineBasicPropertiesMixin):
    """Cisco CUCM AXL Line data model."""


class UserDataModel(UserBasicPropertiesMixin):
    """Cisco CUCM AXL User data model."""


axl_data_models = defaultdict(
    lambda: AXLDataModel,
    phone=PhoneDataModel,
    user=UserDataModel,
    line=LineDataModel,
    thin_axl=ThinAXLDataModel
)


def axl_factory(model, axl_data):
    """
    Factory function for creating AXLData objects.

    :param model: (basestring) Data model to use when creating the AXLData object
    :param axl_data: dictionary data used to initialize the AXLData object
    :return: (AXLData) object
    :raise TypeError: If the json_data parameter is not a JSON string or dictionary.
    :raises TypeError: If the json_data parameter is not a JSON string or dictionary.
    """
    return axl_data_models[model](axl_data)
