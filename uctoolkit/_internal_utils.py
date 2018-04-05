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

from collections import OrderedDict
import os
import sys
import json


def check_type(o, acceptable_types, may_be_none=True):
    """Object is an instance of one of the acceptable types or None.

    :param o: The object to be inspected.
    :param acceptable_types: A type or tuple of acceptable types.
    :param may_be_none: Whether or not the object may be None.
    :return: None
    :raises TypeError: If the object is None and may_be_none=False, or if the
            object is not an instance of one of the acceptable types.
    """
    if not isinstance(acceptable_types, tuple):
        acceptable_types = (acceptable_types,)

    if may_be_none and o is None:
        # Object is None, and that is OK!
        pass
    elif isinstance(o, acceptable_types):
        # Object is an instance of an acceptable type.
        pass
    else:
        # Object is something else.
        error_message = (
            "We were expecting to receive an instance of one of the following "
            "types: {types}{none}; but instead we received {o} which is a "
            "{o_type}.".format(
                types=", ".join([repr(t.__name__) for t in acceptable_types]),
                none="or 'None'" if may_be_none else "",
                o=o,
                o_type=repr(type(o).__name__)
            )
        )
        raise TypeError(error_message)


def is_local_file(string):
    """Check to see if string is a valid local file path."""
    assert isinstance(string, basestring)
    return os.path.isfile(string)


def to_unicode(string):
    """Convert a string (bytes, str or unicode) to unicode."""
    assert isinstance(string, basestring)
    if sys.version_info[0] >= 3:
        if isinstance(string, bytes):
            return string.decode('utf-8')
        else:
            return string
    else:
        if isinstance(string, str):
            return string.decode('utf-8')
        else:
            return string


def to_bytes(string):
    """Convert a string (bytes, str or unicode) to bytes."""
    assert isinstance(string, basestring)
    if sys.version_info[0] >= 3:
        if isinstance(string, str):
            return string.encode('utf-8')
        else:
            return string
    else:
        if isinstance(string, unicode):
            return string.encode('utf-8')
        else:
            return string


def to_json_dict(json_data):
    """Given a dictionary/OrderedDict or JSON string; return a dictionary.

    :param json_data: json_data(dict, OrderedDict, str): Input JSON object.
    :return: A Python dictionary/OrderedDict with the contents of the JSON object.
    :raises TypeError: If the input object is not a dictionary/OrderedDict or string.
    """
    if isinstance(json_data, OrderedDict):
        return json_data
    elif isinstance(json_data, dict):
        return json_data
    elif isinstance(json_data, basestring):
        return json.loads(json_data, object_hook=OrderedDict)
    else:
        raise TypeError(
            "'json_data' must be a dictionary, OrderedDict or valid JSON string; "
            "received: {!r}".format(json_data)
        )


def element_list_to_ordered_dict(element_list):
    """Converts a list of lists of zeep Element objects to a list of OrderedDicts

    :param element_list: list of lists of zeep Element objects
    :return: list of OrderedDicts
    """
    return [OrderedDict((element.tag, element.text) for element in row) for row in element_list]


def dict_from_items_with_values(*dictionaries, **items):
    """Creates a dict with the inputted items; pruning any that are `None`.
    Args:
        *dictionaries(dict): Dictionaries of items to be pruned and included.
        **items: Items to be pruned and included.
    Returns:
        dict: A dictionary containing all of the items with a 'non-None' value.
    """
    dict_list = list(dictionaries)
    dict_list.append(items)
    result = {}
    for d in dict_list:
        for key, value in d.items():
            if value is not None:
                result[key] = value
    return result


def has_valid_kwargs_keys(kwargs, supported_keys):
    """Tests if dictionary is only comprised of supported keys
    :param kwargs: kwargs dict
    :param supported_keys: supported keys for method
    :return: True if all keys in kwargs are supported for method
    """
    return set(kwargs) - set(supported_keys) == set()


def has_single_identifier(identifiers, kwargs):
    """Tests if one and only one identifier is included in kwargs

    :param identifiers: list of identifiers for API call, of which only one is allows
    :param kwargs: method kwargs
    :return: True if only one identifier present in kwargs
    """
    return len(set(kwargs) & set(identifiers)) == 1


def has_mandatory_keys(kwargs, mandatory_keys):
    """Tests if a minimal list of keys exist in dictionary

    :param kwargs: method kwargs dictionary
    :param mandatory_keys: mandatory keys for method
    :return: True if all mandatory keys in kwargs dictionary
    """
    return all(k in kwargs for k in mandatory_keys)

