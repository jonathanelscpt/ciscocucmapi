# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

from inspect import signature
from collections import OrderedDict, Iterable


def element_list_to_ordered_dict(element_list):
    """Converts a list of lists of zeep Element objects to a list of OrderedDicts"""
    return [OrderedDict((element.tag, element.text) for element in row) for row in element_list]


def _flatten(l):
    """Flattens nested Iterable of arbitrary depth"""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el


def check_valid_attribute_req_dict(iterable, d):
    """Check if iterable all of any elements in an iterable are in a dict"""
    return any((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
               for i in iterable)


def downcase_string(s):
    """Convert initial char to lowercase"""
    return s[:1].lower() + s[1:] if s else ''


def _get_signature_kwargs_key(f):
    """Get the key name for kwargs if a method signature"""
    keys = [k for k, v in signature(f).parameters.items() if v.kind == v.VAR_KEYWORD]
    # return keys[0] if len(keys) == 1 else None
    return keys.pop() if len(keys) == 1 else None


def flatten_signature_args(f, loc):
    """flatten a signature dict to include all kwargs as dict members instead of a nested dict"""
    kwargs_name = _get_signature_kwargs_key(f)
    attributes = loc.copy()
    # todo - clean this up with a dict comprehension checked against signature(f).parameters.keys()
    # remove unwanted metadata for class methods
    for meta in ['__class__', 'self']:
        try:
            del attributes[meta]
        except KeyError:
            pass
    if kwargs_name:
        attributes.pop(kwargs_name)
        attributes.update(loc[kwargs_name])
    return attributes
