# -*- coding: utf-8 -*-
"""CUCM AXL User APIs."""

from .base import AbstractAXLDeviceAPI, AbstractAXLAPI
from .._internal_utils import flatten_signature_args


class User(AbstractAXLAPI):
    _factory_descriptor = "user"

    def add(self, userid, lastName, presenceGroupName, **kwargs):
        return super().add(**flatten_signature_args(self.add, locals()))
