# -*- coding: utf-8 -*-
"""CUCM Media Configuration APIs."""

from .base import AbstractAXLAPI, AbstractAXLDeviceAPI


class ConferenceBridge(AbstractAXLDeviceAPI):

    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "devicePoolName",
    )

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            product="Cisco IOS Conference Bridge",
            **kwargs):
        default_kwargs = {
            "product": product,
        }
        default_kwargs.update(kwargs)
        return super().add(**default_kwargs)
