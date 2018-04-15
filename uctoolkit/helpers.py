# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

import json
import csv
from collections import OrderedDict
from pathlib import Path

from zeep.helpers import serialize_object


def to_json_dict(json_data):
    """Given a dictionary or JSON string; return a dictionary.

    :param json_data: json_data(dict, str): Input JSON object.
    :return: A Python dictionary/OrderedDict with the contents of the JSON object.
    :raises TypeError: If the input object is not a dictionary or string.
    """
    if isinstance(json_data, dict):
        return json_data
    elif isinstance(json_data, str):
        return json.loads(json_data, object_hook=OrderedDict)
    else:
        raise TypeError(
            "'json_data' must be a dict or valid JSON string; "
            "received: {!r}".format(json_data)
        )


def to_csv(data_model_list, destination_path):
    """Write list of AXL data models to disk

    :param data_model_list: list of dicts or ordered dicts of data model
    :param destination_path: (Path) file destination Path object or (str)
    :return: None.  csv file written to disk
    """
    if isinstance(destination_path, Path):
        destination_path = destination_path.resolve()
    try:
        with open(destination_path, "w", newline='') as _:
            dict_writer = csv.DictWriter(_, fieldnames=data_model_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(data_model_list)
    except FileNotFoundError:
        # just creating a placeholder for pre-3.6 support...
        # No intention to boil the ocean yet, so just let if die a horrible death for now
        raise FileNotFoundError


def sanitize_data_model_dict(obj):
    """Sanitize zeep output dict with `_value_N` references.

    This is useful for data processing where one wishes to consume the 'get' api data instead of re-purposing
    it in e.g. an 'update' api call. Achieved by flattening the nested OrderedDict by replacing
    the nested dict for AXL's 'XFkType' with the value specified in zeep's `_value_N` key.

    Note: Doing so disregards 'uuid' values.

    Example:

    sample_model_dict = {
        'name': 'SEPAAAABBBBCCCC',
        'callingSearchSpaceName': {
            '_value_1': 'US_NYC_NATIONAL_CSS',
            'uuid': '{987345984385093485gd09df8g}'
        }
    }

    is sanitized to:

    sanitized_sample_model_dict = {
        'name': 'SEPAAAABBBBCCCC',
        'callingSearchSpaceName': 'US_NYC_NATIONAL_CSS'
    }

    :param obj: (dict) AXL data model
    :return: sanitized AXL data model
    """
    # flatten zeep's handling of AXL's XFkType into a k, v pair
    # we need to support the two cases for an instantiated response and
    # where an "X" api endpoint model was created using zeep's 'client.get_type' method
    if set(obj.keys()) == {"uuid", "_value_1"} or set(obj.keys()) == {"_value_1"}:
        return obj["_value_1"]
    else:
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = sanitize_data_model_dict(v)
    return obj


def extract_pkid_from_uuid(pkid_or_uuid):
    """Removes all braces braces encapsulation included with AXL uuid if it exists.

    Does not use regex matching on start/finish for speed.  No validation is provided on uuid format.
    If braces do not exist, the original string should be returned as-is.

    :param pkid_or_uuid: (str) pkid or uuid
    :return: (str) pkid with stripped encapsulation
    """
    # double replace implemented for speed
    return pkid_or_uuid.replace('{', '').replace('}', '')


def filter_mandatory_attributes(zeep_axl_factory_object):
    """Inspect the AXL schema and return a generator of an API endpoint's mandatory attributes.

    Intended use if for local validation prior to submitting an 'add' AXL request to reduce the cost of
    remote error responses from the AXL server.

    Note:
    EXPERIMENTAL ONLY.

    Inconsistencies noted for determinations on minOccurs and nillable.  Suggested not to use.

    :param zeep_axl_factory_object: zeep AXL object generated from a 'get_type' factory call
    :return: generator of mandatory axl elements
    """
    for element in serialize_object(zeep_axl_factory_object).elements:
        # filter on minimum occurrence and no default value
        if element[1].min_occurs >= 1 \
                and not element[1].is_optional \
                and not element[1].nillable \
                and not element[1].default:
            yield element[1]


def get_model_dict(api_endpoint, target_cls=dict, include_types=False):
    """Get an empty model dict or OrderedDict for an api endpoint from a complex zeep type

    "target_cls' an output data structrure preference (default is dict, for speed) as xml element ordering
    is not important for AXL requests.  Alternatively, an OrderedDict is useful for debugging and for
    dumping to JSON objects for local template generation.

    'include_types' is useful for quickly determining the API endpoints expected attribute type
    (e.g. "hostName": "String128") without delving into the .xsd or API documentation.
    Note that some output (e.g. "ldapPortNumber": "anySimpleType") may actually be of a sub-type
    (i.e. "XInteger" in the case of "ldapPortNumber"), but this util does not yet provide that level of granularity
    in its schema inspection.

    :param api_endpoint: zeep data structure
    :param target_cls: (bool) requested model data structure - dict or OrderedDict
    :param include_types: (bool) replace null string with string name of AXL type for each attr
    :return: (dict or OrderedDict) of soap api endpoint
    """
    if target_cls is OrderedDict:
        return OrderedDict((e[0], "" if not include_types else e[1].type.name)
                           if not hasattr(e[1].type, 'elements') else (e[0], get_model_dict(
                                e[1].type,
                                target_cls=target_cls,
                                include_types=include_types))
                           for e in api_endpoint.elements)
    elif target_cls is dict:
        return {e[0]: "" if not include_types else e[1].type.name
                if not hasattr(e[1].type, 'elements') else get_model_dict(
                    e[1].type,
                    target_cls=target_cls,
                    include_types=include_types)
                for e in api_endpoint.elements}
    else:
        raise TypeError("Invalid target class - dict or DefaultDict supported")
