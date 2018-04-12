# -*- coding: utf-8 -*-
"""Package helper functions and classes."""

from collections import OrderedDict, Iterable


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


def downcase_string(s):
    return s[:1].lower() + s[1:] if s else ''
