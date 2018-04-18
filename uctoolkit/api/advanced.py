# -*- coding: utf-8 -*-
"""CUCM AXL Advanced APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_kwargs


class VoiceMailPilot(AbstractAXLAPI):
    _factory_descriptor = "voicemail_pilot"

    def add(self, dirn, isDefault="false", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VoiceMailProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "voicemail_profile"

    def add(self, name, voiceMailPilot, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
