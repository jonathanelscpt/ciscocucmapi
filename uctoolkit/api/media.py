# -*- coding: utf-8 -*-
"""CUCM Media Configuration APIs."""

from .abstract import AbstractAXLAPI, AbstractAXLDeviceAPI


class ConferenceBridge(AbstractAXLDeviceAPI):

    _OBJECT_TYPE = 'conference_bridge'
    _RETURN_OBJECT_NAME = 'conferenceBridge'
    # locationName defaults to Hub_None, but is marked mandatory in the UI
    _ADD_API_MANDATORY_ATTRIBUTES = (
        "name",
        "product",
        "devicePoolName",
        # "locationName",
    )

    def __init__(self, client, object_factory):
        super(ConferenceBridge, self).__init__(client, object_factory)

    @property
    def object_type(self):
        return self._OBJECT_TYPE

    @property
    def return_object_name(self):
        return self._RETURN_OBJECT_NAME

    @property
    def add_api_mandatory_attributes(self):
        return self._ADD_API_MANDATORY_ATTRIBUTES

    def add(self,
            product="Cisco IOS Conference Bridge",
            **kwargs):
        default_kwargs = {
            "product": product,
        }
        kwargs.update(default_kwargs)
        return super(ConferenceBridge, self).add(**kwargs)
