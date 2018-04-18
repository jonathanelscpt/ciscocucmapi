# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

from inspect import signature
from collections import OrderedDict, Iterable


def element_list_to_ordered_dict(elements):
    """Converts a list of lists of zeep Element objects to a list of OrderedDicts"""
    return [OrderedDict((element.tag, element.text) for element in row) for row in elements]


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


def flatten_signature_kwargs(f, loc):
    """flatten a signature dict by one level to move kwargs keys to locals dict"""
    kwargs_name = _get_signature_kwargs_key(f)
    # remove unwanted metadata for class methods
    attributes = get_signature_locals(f, loc)
    if kwargs_name:
        attributes.pop(kwargs_name)
        attributes.update(loc[kwargs_name])
    return attributes


def get_signature_locals(f, loc):
    """Filters locals to only include keys in original method signature"""
    return {k: v for k, v in loc.items() if k in signature(f).parameters}
