# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)
from builtins import *

from collections import OrderedDict, Iterable

from zeep.xsd.elements.indicators import Choice
from zeep.xsd.elements.indicators import Sequence
from zeep.xsd.elements.element import Element


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


def _flatten(l):
    """Flattens nested Iterable of arbitrary depth

    :param l: Iterable
    :return: flattened generator
    """
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el


def all_attributes_exist_with_null_intersection(iterable, d):
    """Test if any value (or all values, if nested) in an Iterable matches
    the keys in a dict, and that the dict has no matching keys
    for any other values (incl. if nested) in the Iterable.

    Limitations:

    Currently doesn't supportive arbitrary recursive calling on Iterable nesting.
    Depth can only be 1.

    :param iterable: Iterable
    :param d: dict
    :return: True if all attributes exist in dict, with null intersection for remaining
    """
    return sum((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
               and frozenset(d.keys()).isdisjoint(_flatten([x for x in i if x != i]))
               for i in iterable) == 1


def check_valid_attribute_req_dict(iterable, d):
    return any((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
               for i in iterable)


def has_mandatory_keys(kwargs, mandatory_keys):
    """Tests if a minimal list of keys exist in dictionary

    :param kwargs: method kwargs dictionary
    :param mandatory_keys: mandatory keys for method
    :return: True if all mandatory keys in kwargs dictionary
    """
    return all(k in kwargs for k in mandatory_keys)


def extract_get_choices(obj):
    if isinstance(obj, (Choice, Sequence)):
        return tuple([extract_get_choices(_) for _ in obj])
    elif isinstance(obj, Element):
        return obj.name
    else:
        raise TypeError("Only Choice, Sequence and Element classes inspected, Type '{cls}' found.".format(
            cls=obj.__class__.__name__
            )
        )
