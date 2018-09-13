# -*- coding: utf-8 -*-

import pytest

from ciscocucmapi.exceptions import ParseError
from ciscocucmapi.helpers import (
    extract_pkid_from_uuid,
    filter_dict_to_target_model,
    get_model_dict,
    sanitize_model_dict
)


@pytest.fixture()
def xaargroup_model(fake_axl_client):
    _target_model_name = "XAarGroup"
    return fake_axl_client.client.get_type(f'ns0:{_target_model_name}')


@pytest.fixture()
def unsanitized_basic_obj(guid):
    _unsanitized_obj = {
        "callingSearchSpaceName": {
            "_value_1": "custom value",
            "uuid": guid
        }
    }
    return _unsanitized_obj


@pytest.fixture()
def unsanitized_basic_model():
    _unsanitized_model = {
        "callingSearchSpaceName": {
            "_value_1": None,
            "uuid": None
        }
    }
    return _unsanitized_model


@pytest.fixture()
def unsanitized_nested_obj(guid):
    _unsanitized_object = {
        "name": "name",
        "nested": {
            "key1": "val1",
            "nested_key": {
                "_value_1": 234324,
                "uuid": guid
            }
        }
    }
    return _unsanitized_object


def test_uuid_valid_guid(guid, pkid):
    assert extract_pkid_from_uuid(guid) == pkid


def test_uuid_valid_pkid(pkid):
    assert extract_pkid_from_uuid(pkid) == pkid


def test_uuid_none_input():
    with pytest.raises(TypeError):
        extract_pkid_from_uuid(None)


def test_uuid_numeric_input():
    with pytest.raises(TypeError):
        extract_pkid_from_uuid(12345)


def test_model_dict_simple_obj(xaargroup_model):
    assert get_model_dict(xaargroup_model) == {"name": ""}


def test_model_dict_invalid_input():
    with pytest.raises(ValueError):
        get_model_dict(obj="invalid string")


def test_filter_to_target_model_simple(xaargroup_model):
    model_dict = get_model_dict(xaargroup_model)
    _filtered = filter_dict_to_target_model(obj={"name": "TestAARG", "fakeAttr": 12345},
                                            target_model=model_dict)
    assert _filtered == {"name": "TestAARG"}


def test_filter_to_target_model_nested(xaargroup_model):
    raise NotImplementedError


def test_filter_to_target_model_list_of_dicts(xaargroup_model):
    raise NotImplementedError


def test_filter_to_target_model_list_of_str(xaargroup_model):
    raise NotImplementedError


def test_filter_to_target_model_unsanitized(xaargroup_model):
    raise NotImplementedError


def test_filter_model_invalid_input_str(xaargroup_model):
    model_dict = get_model_dict(xaargroup_model)
    with pytest.raises(ParseError):
        filter_dict_to_target_model(obj="invalid string", target_model=model_dict)


def test_sanitize_basic_obj(unsanitized_basic_obj):
    _sanitized_obj = {"callingSearchSpaceName": "custom value"}
    assert sanitize_model_dict(unsanitized_basic_obj) == _sanitized_obj


def test_sanitize_nested_obj(unsanitized_nested_obj):
    _sanitized_obj = {
        "name": "name",
        "nested": {
            "key1": "val1",
            "nested_key": 234324
            }
        }
    assert sanitize_model_dict(unsanitized_nested_obj) == _sanitized_obj


def test_sanitize_model(unsanitized_basic_model):
    _sanitized_model = {"callingSearchSpaceName": None}
    assert sanitize_model_dict(unsanitized_basic_model) == _sanitized_model


def test_sanitize_dict_unchanged():
    _unchanged_dict = {"pattern": 123453, "index": 1}
    assert sanitize_model_dict(_unchanged_dict) == _unchanged_dict


def test_sanitize_str_unchanged():
    _sample_str = "sample string"
    assert sanitize_model_dict(_sample_str) == _sample_str


def test_sanitize_invalid_list():
    _invalid_list = [{"index": 1}, {"index": 2}, {"index": 3}]
    with pytest.raises(ParseError):
        sanitize_model_dict(_invalid_list)
