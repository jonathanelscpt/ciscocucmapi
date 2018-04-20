# -*- coding: utf-8 -*-
"""CUCM AXL Advanced APIs."""

from .base import DeviceAXLAPI, SimpleAXLAPI
from .._internal_utils import flatten_signature_kwargs


class VoiceMailPilot(SimpleAXLAPI):
    _factory_descriptor = "voicemail_pilot"

    def add(self, dirn, isDefault=False, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VoiceMailProfile(DeviceAXLAPI):
    _factory_descriptor = "voicemail_profile"

    def add(self, name, voiceMailPilot, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
