# -*- coding: utf-8 -*-
"""AXL Data Model Classes"""

from collections import defaultdict

from .axldata import AXLDataModel, ThinAXLDataModel


axl_data_models = defaultdict(
    lambda: AXLDataModel,
    ThinAXL=ThinAXLDataModel,
)


def axl_factory(model, axl_data):
    """Factory function for creating AXLData objects.

    :param model: (basestring) Data model to use when creating the AXLData object
    :param axl_data: dictionary data used to initialize the AXLData object
    :return: (AXLData) object
    :raises TypeError: If the json_data parameter is not a JSON string or dictionary.
    """
    return axl_data_models[model](axl_data)
