# -*- coding: utf-8 -*-
"""Package helper functions and classes."""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

from builtins import *
from past.builtins import basestring, unicode

import json
from collections import OrderedDict


def to_json_dict(json_data):
    """Given a dictionary or JSON string; return a dictionary.

    :param json_data: json_data(dict, str): Input JSON object.
    :return: A Python dictionary/OrderedDict with the contents of the JSON object.
    :raises TypeError: If the input object is not a dictionary or string.
    """
    if isinstance(json_data, dict):
        return json_data
    elif isinstance(json_data, basestring):
        return json.loads(json_data, object_hook=OrderedDict)
    else:
        raise TypeError(
            "'json_data' must be a dict or valid JSON string; "
            "received: {!r}".format(json_data)
        )


def to_csv(data_model):
    """Convert API Data model to csv object.  This is useful for writing API data model objects to files and
    for converting sql output into a familiar tabulated format.
    """
    raise NotImplementedError


def sanitize_data_model_dict(data_model):
    """Sanitize zeep output dict with `_value_N` references.  This is useful for
    data processing where one wishes to consume the 'get' api data instead of re-purposing
    it in e.g. an 'update' api call.

    This is achieved by flattening the nested OrderedDict by replacing the nested dict for AXL's 'XFkType'
    with the value specified in zeep's `_value_N` key.

    Note:

    Doing so disregards 'uuid' values.

    Example:

    {
        'name': 'SEPAAAABBBBCCCC'
        'callingSearchSpaceName': {
            '_value_1': 'US_NYC_NATIONAL_CSS'
            'uuid': '{987345984385093485gd09df8g}'
        }
    }

    is sanitized to:

    {
        'name': 'SEPAAAABBBBCCCC'
        'callingSearchSpaceName': 'US_NYC_NATIONAL_CSS'
    }
    """
    raise NotImplementedError


def extract_pkid_from_uuid(pkid_or_uuid):
    return pkid_or_uuid.replace('{', '').replace('}', '')  # double replace chosen for speed

