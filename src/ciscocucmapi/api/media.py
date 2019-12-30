"""CUCM Media Configuration APIs."""

from .._internal_utils import flatten_signature_kwargs
from .base import DeviceAXLAPI
from .base import SimpleAXLAPI


class Announcement(SimpleAXLAPI):
    _factory_descriptor = "announcement"

    def add(self, name,
            announcementFile=None,
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Annunciator(SimpleAXLAPI):
    _factory_descriptor = "annunciator"
    supported_methods = ["get", "list", "update"]


class ConferenceBridge(DeviceAXLAPI):
    _factory_descriptor = "conference_bridge"

    def add(self, name, devicePoolName, product="Cisco IOS Conference Bridge", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MediaResourceGroup(SimpleAXLAPI):
    _factory_descriptor = "mrg"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MediaResourceList(SimpleAXLAPI):
    _factory_descriptor = "mrgl"

    def add(self, name, members, **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class MohServer(SimpleAXLAPI):
    _factory_descriptor = "moh_server"
    supported_methods = ["get", "list", "update"]


class Mtp(DeviceAXLAPI):
    _factory_descriptor = "mtp"

    def add(self, name, devicePoolName, mtpType="Cisco IOS Enhanced Software Media Termination Point", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class Transcoder(DeviceAXLAPI):
    _factory_descriptor = "transcoder"
    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "reset"]

    def add(self, name, devicePoolName, product="Cisco IOS Enhanced Media Termination Point",
            **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)


class VohServer(SimpleAXLAPI):
    _factory_descriptor = "voh_server"

    def add(self, name, sipTrunkName, defaultVideoStreamId="SampleVideo", **kwargs):
        add_kwargs = flatten_signature_kwargs(self.add, locals())
        return super().add(**add_kwargs)
