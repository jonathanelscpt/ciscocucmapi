# -*- coding: utf-8 -*-

import pytest
from ciscocucmapi import UCMAXLConnector
from ciscocucmapi.definitions import WSDL_PATH


@pytest.fixture(scope="module")
def fake_axl_client(version="current"):
    """Fake connector for generating models"""
    _wsdl = str(WSDL_PATH / version / "AXLAPI.wsdl")
    return UCMAXLConnector(username="fakeadmin", password="fakepwd", wsdl=_wsdl, timeout=3)


@pytest.fixture(scope="module")
def guid():
    return "{BE3CF0D3-8666-332D-13A1-5411B8F53618}"


@pytest.fixture(scope="module")
def pkid():
    return "be3cf0d3-8666-332d-13a1-5411b8f53618"

