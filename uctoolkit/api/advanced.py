# -*- coding: utf-8 -*-
"""CUCM AXL Advanced APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args


class VoiceMailPilot(AbstractAXLDeviceAPI):
    _factory_descriptor = "voicemail_pilot"

    def add(self, dirn, isDefault="false", **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))


class VoiceMailProfile(AbstractAXLDeviceAPI):
    _factory_descriptor = "voicemail_profile"

    def add(self, name, voiceMailPilot, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))

