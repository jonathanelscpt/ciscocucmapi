# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

from inspect import signature
from collections import OrderedDict, Iterable


def element_list_to_ordered_dict(element_list):
    """Converts a list of lists of zeep Element objects to a list of OrderedDicts

    :param element_list: list of lists of zeep Element objects
    :return: list of OrderedDicts
    """
    return [OrderedDict((element.tag, element.text) for element in row) for row in element_list]


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


# def all_attributes_exist_with_null_intersection(iterable, d):
#     """Test if any value (or all values, if nested) in an Iterable matches
#     the keys in a dict, and that the dict has no matching keys
#     for any other values (incl. if nested) in the Iterable.
#
#     Limitations:
#
#     Currently doesn't supportive arbitrary recursive calling on Iterable nesting.
#     Depth can only be 1.
#
#     :param iterable: Iterable
#     :param d: dict
#     :return: True if all attributes exist in dict, with null intersection for remaining
#     """
#     return sum((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
#                and frozenset(d.keys()).isdisjoint(_flatten([x for x in i if x != i]))
#                for i in iterable) == 1


def check_valid_attribute_req_dict(iterable, d):
    return any((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
               for i in iterable)


def downcase_string(s):
    return s[:1].lower() + s[1:] if s else ''


def _get_signature_kwargs_key(f):
    keys = [k for k, v in signature(f).parameters.items() if v.kind == v.VAR_KEYWORD]
    return keys[0] if len(keys) == 1 else None


def flatten_signature_args(f, loc):
    kwargs_name = _get_signature_kwargs_key(f)
    attributes = loc.copy()
    # remove unwanted metadata for class methods
    for meta in ['__class__', 'self']:
        try:
            del attributes[meta]
        except KeyError:
            pass
    attributes.pop(kwargs_name)
    attributes.update(loc[kwargs_name])
    return attributes
