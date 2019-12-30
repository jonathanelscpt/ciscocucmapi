"""Package helper functions and classes."""

from collections import Iterable
from collections import OrderedDict
from inspect import signature


def element_list_to_ordered_dict(elements):
    """Converts a list of lists of zeep Element objects to a list of OrderedDicts"""
    return [OrderedDict((element.tag, element.text) for element in row) for row in elements]


def flatten(l):
    """Flattens nested Iterable of arbitrary depth"""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def check_valid_attribute_req_dict(iterable, d):
    """Check if iterable all of any elements in an iterable are in a dict"""
    return any((i in d if not isinstance(i, tuple) else (all(sub_i in d for sub_i in i)))
               for i in iterable)


def downcase_string(s):
    """Convert initial char to lowercase"""
    return s[:1].lower() + s[1:] if s else ''


def get_signature_kwargs_key(f):
    """Get the key name for kwargs if a method signature"""
    keys = [k for k, v in signature(f).parameters.items() if v.kind == v.VAR_KEYWORD]
    try:
        return keys.pop()
    except IndexError:  # empty list
        return None


def flatten_signature_kwargs(func, loc):
    """flatten a signature dict by one level to move kwargs keys to locals dict"""
    kwargs_name = get_signature_kwargs_key(func)
    # remove unwanted metadata for class methods
    attributes = get_signature_locals(func, loc)
    if kwargs_name:
        attributes.pop(kwargs_name)
        attributes.update(loc[kwargs_name])
    return attributes


def get_signature_locals(f, loc):
    """Filters locals to only include keys in original method signature"""
    return {k: v for k, v in loc.items() if k in signature(f).parameters}


def nullstring_dict(returnedTags):
    """Convert list to nullstring dict"""
    return {_: "" for _ in returnedTags}
