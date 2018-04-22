# -*- coding: utf-8 -*-
"""Base AXL APIs"""

from operator import methodcaller
from collections import OrderedDict
import functools

from zeep.helpers import serialize_object
from zeep.exceptions import Fault
from zeep.xsd.elements.indicators import Choice
from zeep.xsd.elements.indicators import Sequence
from zeep.xsd.elements.element import Element

from ..exceptions import (
    AXLFault,
    IllegalSQLStatement
)
from .._internal_utils import (
    check_valid_attribute_req_dict,
    element_list_to_ordered_dict,
    downcase_string,
    flatten_signature_kwargs,
    nullstring_dict
)
from ..helpers import (
    model_dict,
    sanitize_model_dict
)


def _get_choices(obj):
    """Create tuple of available choices as defined in xsd

    Recursively inspects a zeep object and extracts the available choices available when performing
    the specific AXL call, as defined in AXL xsd.

    :param obj: zeep Element data structure type
    :return: nested tuple of the xsd-defined choices for the AXL method
    """
    if isinstance(obj, (Choice, Sequence)):
        return tuple([_get_choices(_) for _ in obj])
    elif isinstance(obj, Element):
        return obj.name
    else:
        raise TypeError("Only Choice, Sequence and Element classes inspected, Type '{cls}' found.".format(
            cls=obj.__class__.__name__
            )
        )


def check_identifiers(wsdl_obj, **kwargs):
    identifiers = _get_choices(wsdl_obj.elements_nested[0][1][0])
    if not check_valid_attribute_req_dict(identifiers, kwargs):
        raise TypeError("Supplied identifiers not supported for API call: {identifiers}".format(
            identifiers=identifiers)
        )


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


class ClassPropertyDescriptor(object):
    # setter wont work, but we don't want it at the class level in any case
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, obj_class=None):
        if obj_class is None:
            obj_class = type(obj)
        return self.fget.__get__(obj, obj_class)()


class BaseAXLAPI(object):
    """Base API Class for AXL objects"""
    _factory_descriptor = ValueError

    def __init__(self, connector, object_factory):
        self.connector = connector
        self.object_factory = object_factory
        self._return_name = downcase_string(self.__class__.__name__)

    @classproperty
    def factory_descriptor(cls):  # noqa
        return cls._factory_descriptor

    @classmethod
    def assert_supported(cls, func):
        """Decorator looks up func's name in self.supported_methods."""

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if func.__name__ not in self.supported_methods:
                raise AttributeError("{api_endpoint} API does not support '{function_name}' method.".format(
                    api_endpoint=self.__class__.__name__,
                    function_name=func.__name__
                ))
            return func(self, *args, **kwargs)

        return wrapper

    def _get_wsdl_obj(self, obj_name):
        """Get an empty python-zeep complex type

        :param obj_name: name of AXL type
        :return: empty zeep complex type obj
        """
        return self.connector.client.get_type('ns0:{name}'.format(
            name=obj_name
        ))

    def _axl_methodcaller(self, action, **kwargs):
        """Map calling method to a concat of the action verb and the API class name

        :param action: (str) API verb - 'add', 'get', 'list', etc.
        :param kwargs: input kwargs for called method
        :return: axl response zeep object
        """
        try:
            axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
            return axl_method(self.connector.service)
        except Fault as fault:
            raise AXLFault(fault.message)

    def _serialize_axl_object(self, action, **kwargs):
        """Builds and AXL methodcaller using given action verb and the object type.

        Serializes the response and uses the resultant dict to instantiate a data model object

        :param action: AXL action verb - 'add', 'get', 'update', 'remove', etc.
        :param kwargs: AXL method attribute kwargs dictionary
        :return: Data Model object containing the serialized response data dict
        """
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return self.object_factory(
            self.__class__.__name__,
            serialize_object(axl_resp)["return"][self._return_name]
        )

    def _serialize_uuid_resp(self, action, **kwargs):
        """Serialize commons responses that return a uuid string only

        :param action: axl method verb
        :param kwargs: dict of method attributes
        :return: (str) uuid
        """
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return serialize_object(axl_resp)["return"]


class SimpleAXLAPI(BaseAXLAPI):
    """Simple AXL API with common method support"""

    supported_methods = ["model", "create", "add", "get", "update", "list", "remove"]  # doesn't include 'options'

    def _fetch_add_model(self):
        add_model_name = "".join(["X", self.__class__.__name__])
        return self._get_wsdl_obj(add_model_name)

    @BaseAXLAPI.assert_supported
    def model(self, sanitized=True, target_cls=OrderedDict, include_types=False):
        """Get a empty serialized 'add' model for the API endpoint

        Useful for inspecting the endpoint's schema and future template generation.

        :param sanitized: collapse zeep's interpretation of the xsd nested dicts
        with '_value_1' and 'uuid' keys into a simple k,v pair with v as a (str)
        :param target_cls: dict or OrderedDict
        :param include_types: (bool) include zeep model type inspection
        :return: empty data model dictionary
        """
        model = model_dict(self._fetch_add_model(), target_cls=target_cls, include_types=include_types)
        return sanitize_model_dict(model) if sanitized else model

    @BaseAXLAPI.assert_supported
    def create(self, **kwargs):
        """Create AXL object locally for pre-processing"""
        axl_add_method = methodcaller(self._fetch_add_model().__class__.__name__, **kwargs)
        axl_add_obj = axl_add_method(self.connector.model_factory)
        return self.object_factory(self.__class__.__name__, serialize_object(axl_add_obj))

    @BaseAXLAPI.assert_supported
    def add(self, **kwargs):
        """Add method for API endpoint"""
        wrapped_kwargs = {
            self._return_name: kwargs
        }
        return self._serialize_uuid_resp("add", **wrapped_kwargs)

    @BaseAXLAPI.assert_supported
    def get(self, returnedTags=None, **kwargs):
        """Get method for API endpoint"""
        if isinstance(returnedTags, list):
            returnedTags = nullstring_dict(returnedTags)
        # define zeep objects for method generically
        get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
        get_model_name = "".join(["R", self.__class__.__name__])
        get_method = self._get_wsdl_obj(get_method_name)
        check_identifiers(get_method, **kwargs)
        get_kwargs = flatten_signature_kwargs(self.get, locals())
        return self._serialize_axl_object("get", **get_kwargs)

    @BaseAXLAPI.assert_supported
    def update(self, **kwargs):
        """Update method for API endpoint"""
        return self._serialize_uuid_resp("update", **kwargs)

    @BaseAXLAPI.assert_supported
    def list(self, searchCriteria=None, returnedTags=None, skip=None, first=None):
        """Fetch a list of API endpoint objects.

        Note:
        'searchCriteria=None' or 'returnedTags=None' may have VERY verbose output
        and create large responses over 8MB, potentially resulting in AXL errors for large data sets.

        :param searchCriteria: (dict) search criteria for "list' method.  Wraps a 'fetch-all' if unspecified.
        :param returnedTags: (dict) returned attributes.  If none, wrapper
        :param skip: (int) skip number of results
        :param first: (int) return first number of results
        :return: list of Data Models for API Endpoint
        """
        list_method_name = "".join(["List", self.__class__.__name__, "Req"])
        list_model_name = "".join(["L", self.__class__.__name__])
        list_method = self._get_wsdl_obj(list_method_name)
        list_model = self._get_wsdl_obj(list_model_name)

        if not searchCriteria:
            # this is presumptive and may not work in all cases.
            supported_criteria = [element[0] for element in list_method.elements[0][1].type.elements]
            searchCriteria = {supported_criteria[0]: "%"}
        if not returnedTags:
            returnedTags = model_dict(list_model)
        elif isinstance(returnedTags, list):
            returnedTags = nullstring_dict(returnedTags)
        axl_resp = self._axl_methodcaller("list",
                                          searchCriteria=searchCriteria,
                                          returnedTags=returnedTags,
                                          skip=skip,
                                          first=first)
        try:
            axl_list = serialize_object(axl_resp)["return"][self._return_name]
            return [self.object_factory(self.__class__.__name__, item) for item in axl_list]
        except TypeError:
            return []

    @BaseAXLAPI.assert_supported
    def remove(self, **kwargs):
        """Remove method for API endpoint"""
        # check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_uuid_resp("remove", **kwargs)

    @BaseAXLAPI.assert_supported
    def options(self, uuid, returnedChoices=None):
        try:
            kwargs = {
                "uuid": uuid,
                "returnedChoices": returnedChoices
            }
            options_method = methodcaller("".join(["get", self.__class__.__name__, "Options"]), **kwargs)
            print("".join(["get", self.__class__.__name__, "Options"]))
            print(kwargs)
            axl_resp = options_method(self.connector.service)
            return self.object_factory(
                "".join([self.__class__.__name__, "Options"]),
                serialize_object(axl_resp)["return"][self._return_name]
            )
        except Fault as fault:
            print("herro")
            raise AXLFault(fault.message)


class DeviceAXLAPI(SimpleAXLAPI):
    """AXL API support additional device-related methods"""

    supported_methods = ["model", "create", "add", "get", "list", "update", "remove", "apply", "restart", "reset"]

    @BaseAXLAPI.assert_supported
    def apply(self, **kwargs):
        """Apply config to API endpoint

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        return self._serialize_uuid_resp("apply", **kwargs)

    @BaseAXLAPI.assert_supported
    def restart(self, **kwargs):
        """Restart API endpoint

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        return self._serialize_uuid_resp("restart", **kwargs)

    @BaseAXLAPI.assert_supported
    def reset(self, **kwargs):
        """Reset API endpoint

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        return self._serialize_uuid_resp("reset", **kwargs)


class ThinAXLAPI(BaseAXLAPI):
    _factory_descriptor = "sql"
    supported_methods = ["query", "update"]

    @BaseAXLAPI.assert_supported
    def query(self, sql_statement):
        """Execute SQL query via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: SQL Thin AXL data model object
        """
        try:
            axl_resp = self.connector.service.executeSQLQuery(sql=sql_statement)
            try:
                serialized_resp = element_list_to_ordered_dict(
                    serialize_object(axl_resp)["return"]["rows"]
                )
            # AXL supplies different keyword for single row return
            except KeyError:
                serialized_resp = element_list_to_ordered_dict(
                    serialize_object(axl_resp)["return"]["row"]
                )
            return self.object_factory(self.__class__.__name__, serialized_resp)
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)

    @BaseAXLAPI.assert_supported
    def update(self, sql_statement):
        """Execute SQL update via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: (int) number of rows updated
        """
        try:
            axl_resp = self.connector.service.executeSQLUpdate(sql=sql_statement)
            return serialize_object(axl_resp)["return"]["rowsUpdated"]
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)


# class AbstractAXLAPI(object):
#     """Abstract API Class enforcing common methods for AXL objects"""
#     _factory_descriptor = NotImplementedError
#
#     def __init__(self, connector, object_factory):
#         self.connector = connector
#         self.object_factory = object_factory
#         self._return_name = downcase_string(self.__class__.__name__)
#
#         # add_model_name = "".join(["X", self.__class__.__name__])
#         # get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
#         # get_model_name = "".join(["R", self.__class__.__name__])
#         # update_method_name = "".join(["Update", self.__class__.__name__, "Req"])
#         # list_method_name = "".join(["List", self.__class__.__name__, "Req"])
#         # list_model_name = "".join(["L", self.__class__.__name__])
#
#         # this looks expensive during __init__.
#         # may need to time this and move to individul methods.  cleaner code if here though
#         self._wsdl_objects = {
#             # "add_model": self._get_wsdl_obj(add_model_name),
#             # "get_method": self._get_wsdl_obj(get_method_name),
#             # "get_model": self._get_wsdl_obj(get_model_name),
#             # "list_method": self._get_wsdl_obj(list_method_name),
#             # "list_model": self._get_wsdl_obj(list_model_name),
#             # "update_method": self._get_wsdl_obj(update_method_name),
#             # "name_and_guid_model": self._get_wsdl_obj("NameAndGUIDRequest")  # used in many AXL requests
#         }
#
#     @classproperty
#     def factory_descriptor(cls):  # noqa
#         return cls._factory_descriptor
#
#     def _get_wsdl_obj(self, obj_name):
#         """Get an empty python-zeep complex type
#
#         :param obj_name: name of AXL type
#         :return: empty zeep complex type obj
#         """
#         return self.connector.client.get_type('ns0:{name}'.format(
#             name=obj_name
#         ))
#
#     def _axl_methodcaller(self, action, **kwargs):
#         """Map calling method to a concat of the action verb and the API class name
#
#         :param action: (str) API verb - 'add', 'get', 'list', etc.
#         :param kwargs: input kwargs for called method
#         :return: axl response zeep object
#         """
#         try:
#             axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
#             return axl_method(self.connector.service)
#         except Fault as fault:
#             raise AXLError(fault.message)
#
#     def _serialize_axl_object(self, action, **kwargs):
#         """Builds and AXL methodcaller using given action verb and the object type.
#
#         Serializes the response and uses the resultant dict to instantiate a data model object
#
#         :param action: AXL action verb - 'add', 'get', 'update', 'remove', etc.
#         :param kwargs: AXL method attribute kwargs dictionary
#         :return: Data Model object containing the serialized response data dict
#         """
#         axl_resp = self._axl_methodcaller(action, **kwargs)
#         return self.object_factory(
#             self.__class__.__name__,
#             serialize_object(axl_resp)["return"][self._return_name]
#         )
#
#     def _serialize_uuid_resp(self, action, **kwargs):
#         """Serialize commons responses that return a uuid string only
#
#         :param action: axl method verb
#         :param kwargs: dict of method attributes
#         :return: (str) uuid
#         """
#         axl_resp = self._axl_methodcaller(action, **kwargs)
#         return serialize_object(axl_resp)["return"]
#
#     def _fetch_add_model(self):
#         add_model_name = "".join(["X", self.__class__.__name__])
#         return self._get_wsdl_obj(add_model_name)
#
#     def model(self, sanitized=True, target_cls=OrderedDict, include_types=False):
#         """Get a empty serialized 'add' model for the API endpoint
#
#         Useful for inspecting the endpoint's schema and future template generation.
#
#         :param sanitized: collapse zeep's interpretation of the xsd nested dicts
#         with '_value_1' and 'uuid' keys into a simple k,v pair with v as a (str)
#         :param target_cls: dict or OrderedDict
#         :return: empty data model dictionary
#         """
#         model = model_dict(self._fetch_add_model(), target_cls=target_cls, include_types=include_types)
#         return sanitize_model_dict(model) if sanitized else model
#
#     def create(self, **kwargs):
#         """Create AXL object locally for pre-processing"""
#         axl_add_method = methodcaller(self._fetch_add_model().__class__.__name__, **kwargs)
#         axl_add_obj = axl_add_method(self.connector.model_factory)
#         return self.object_factory(self.__class__.__name__, serialize_object(axl_add_obj))
#
#     def add(self, **kwargs):
#         """Add method for API endpoint"""
#         wrapped_kwargs = {
#             self._return_name: kwargs
#         }
#         return self._serialize_uuid_resp("add", **wrapped_kwargs)
#
#     def get(self, returnedTags=None, **kwargs):
#         """Get method for API endpoint"""
#         if isinstance(returnedTags, list):
#             returnedTags = nullstring_dict(returnedTags)
#         # define zeep objects for method generically
#         get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
#         get_model_name = "".join(["R", self.__class__.__name__])
#         get_method = self._get_wsdl_obj(get_method_name)
#         check_identifiers(get_method, **kwargs)
#         get_kwargs = flatten_signature_kwargs(self.get, locals())
#         return self._serialize_axl_object("get", **get_kwargs)
#
#     def update(self, **kwargs):
#         """Update method for API endpoint"""
#         return self._serialize_uuid_resp("update", **kwargs)
#
#     def list(self, searchCriteria=None, returnedTags=None, skip=None, first=None):
#         """Fetch a list of API endpoint objects.
#
#         Note:
#         'searchCriteria=None' or 'returnedTags=None' may have VERY verbose output
#         and create large responses over 8MB, potentially resulting in AXL errors for large data sets.
#
#         :param searchCriteria: (dict) search criteria for "list' method.  Wraps a 'fetch-all' if unspecified.
#         :param returnedTags: (dict) returned attributes.  If none, wrapper
#         :param skip: (int) skip number of results
#         :param first: (int) return first number of results
#         :return: list of Data Models for API Endpoint
#         """
#         list_method_name = "".join(["List", self.__class__.__name__, "Req"])
#         list_model_name = "".join(["L", self.__class__.__name__])
#         list_method = self._get_wsdl_obj(list_method_name)
#         list_model = self._get_wsdl_obj(list_model_name)
#
#         if not searchCriteria:
#             # this is presumptive and may not work in all cases.
#             supported_criteria = [element[0] for element in list_method.elements[0][1].type.elements]
#             searchCriteria = {supported_criteria[0]: "%"}
#         if not returnedTags:
#             returnedTags = model_dict(list_model)
#         elif isinstance(returnedTags, list):
#             returnedTags = nullstring_dict(returnedTags)
#         axl_resp = self._axl_methodcaller("list",
#                                           searchCriteria=searchCriteria,
#                                           returnedTags=returnedTags,
#                                           skip=skip,
#                                           first=first)
#         try:
#             axl_list = serialize_object(axl_resp)["return"][self._return_name]
#             return [self.object_factory(self.__class__.__name__, item) for item in axl_list]
#         except TypeError:
#             return []
#
#     def remove(self, **kwargs):
#         """Remove method for API endpoint"""
#         # check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
#         return self._serialize_uuid_resp("remove", **kwargs)
#
#
# class AbstractAXLDeviceAPI(AbstractAXLAPI):
#     """Abstract Device API class with additional device methods"""
#
#     def apply(self, **kwargs):
#         """Apply config to API endpoint
#
#         :param kwargs: uuid or name
#         :return: (str) uuid
#         """
#         return self._serialize_uuid_resp("apply", **kwargs)
#
#     def restart(self, **kwargs):
#         """Restart API endpoint
#
#         :param kwargs: uuid or name
#         :return: (str) uuid
#         """
#         return self._serialize_uuid_resp("restart", **kwargs)
#
#     def reset(self, **kwargs):
#         """Reset API endpoint
#
#         :param kwargs: uuid or name
#         :return: (str) uuid
#         """
#         return self._serialize_uuid_resp("reset", **kwargs)
#
#
# class ThinAXL(object):
#     """Abstract API Class enforcing common methods for Thin AXL objects"""
#     _factory_descriptor = "sql"
#
#     def __init__(self, connector, object_factory):
#         self._connector = connector
#         self._object_factory = object_factory
#
#     @classproperty
#     def factory_descriptor(cls):  # noqa
#         return cls._factory_descriptor
#
#     def query(self, sql_statement):
#         """Execute SQL query via Thin AXL
#
#         :param sql_statement: Informix-compliant SQL statement
#         :return: SQL Thin AXL data model object
#         """
#         try:
#             axl_resp = self._connector.service.executeSQLQuery(sql=sql_statement)
#             try:
#                 serialized_resp = element_list_to_ordered_dict(
#                     serialize_object(axl_resp)["return"]["rows"]
#                 )
#             # AXL supplies different keyword for single row return
#             except KeyError:
#                 serialized_resp = element_list_to_ordered_dict(
#                     serialize_object(axl_resp)["return"]["row"]
#                 )
#             return self._object_factory(self.__class__.__name__, serialized_resp)
#         except Fault as fault:
#             raise IllegalSQLStatement(message=fault.message)
#
#     def update(self, sql_statement):
#         """Execute SQL update via Thin AXL
#
#         :param sql_statement: Informix-compliant SQL statement
#         :return: (int) number of rows updated
#         """
#         try:
#             axl_resp = self._connector.service.executeSQLUpdate(sql=sql_statement)
#             return serialize_object(axl_resp)["return"]["rowsUpdated"]
#         except Fault as fault:
#             raise IllegalSQLStatement(message=fault.message)
