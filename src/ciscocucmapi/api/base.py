"""Base AXL APIs"""

import functools
from operator import methodcaller

from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from zeep.xsd.elements.element import Element
from zeep.xsd.elements.indicators import Choice
from zeep.xsd.elements.indicators import Sequence

from .._internal_utils import check_valid_attribute_req_dict
from .._internal_utils import downcase_string
from .._internal_utils import element_list_to_ordered_dict
from .._internal_utils import flatten_signature_kwargs
from .._internal_utils import nullstring_dict
from ..exceptions import IllegalSQLStatement
from ..helpers import get_model_dict
from ..helpers import sanitize_model_dict


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
        raise TypeError(f"Only Choice, Sequence and Element classes inspected, Type '{obj.__class__.__name__}' found.")


def check_identifiers(wsdl_obj, **kwargs):
    """Check identifiers by inspecting choices in zeep model object

    :param wsdl_obj: zeep AXL model object
    :param kwargs: supplied identifiers to test
    :return: None
    """
    identifiers = _get_choices(wsdl_obj.elements_nested[0][1][0])
    if not check_valid_attribute_req_dict(identifiers, kwargs):
        raise TypeError(f"Supplied identifiers not supported for API call: {identifiers}")


def classproperty(func):
    """Decorator function to denote class properties"""
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


class ClassPropertyDescriptor(object):
    """Decorator class for class properties"""
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
                raise AttributeError(
                    f"{self.__class__.__name__} API does not support '{func.__name__}' method.")
            return func(self, *args, **kwargs)

        return wrapper


class SimpleAXLAPI(BaseAXLAPI):
    """Simple AXL API with common method support"""
    supported_methods = ["model", "create", "add", "get", "update", "list", "remove"]  # doesn't include 'options'

    def __init__(self, connector, object_factory):
        super().__init__(connector, object_factory)
        if "add" in self.supported_methods:
            self._add_model_name = "".join(["X", self.__class__.__name__])
        if "get" in self.supported_methods:
            self._get_model_name = "".join(["R", self.__class__.__name__])
            self._get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
        if "list" in self.supported_methods:
            self._list_method_name = "".join(["List", self.__class__.__name__, "Req"])
            self._list_model_name = "".join(["L", self.__class__.__name__])

    def _fetch_add_model(self):
        return self._get_wsdl_obj(self._add_model_name)

    def _get_wsdl_obj(self, obj_name):
        """Get empty python-zeep complex type

        :param obj_name: name of AXL type
        :return: empty zeep complex type obj
        """
        return self.connector.client.get_type(f'ns0:{obj_name}')

    def _axl_methodcaller(self, action, **kwargs):
        """Map calling method to a concat of the action verb and the API class name

        :param action: (str) API verb - 'add', 'get', 'list', etc.
        :param kwargs: input kwargs for called method
        :return: axl response zeep object
        """
        axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
        return axl_method(self.connector.service)

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
            serialize_object(axl_resp)["return"][self._return_name])

    def _serialize_uuid_resp(self, action, **kwargs):
        """Serialize commons responses that return a uuid string only

        :param action: axl method verb
        :param kwargs: dict of method attributes
        :return: (str) uuid
        """
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return serialize_object(axl_resp)["return"]

    @BaseAXLAPI.assert_supported
    def model(self, target_model="add", sanitized=True, include_types=False):
        """Get a empty serialized 'add' model for the API endpoint

        Useful for inspecting the endpoint's schema and future template generation.

        :param target_model: target model for api - 'add', 'get', 'update' etc.
        :param sanitized: collapse zeep's interpretation of the xsd nested dicts
        with '_value_1' and 'uuid' keys into a simple k,v pair with v as a (str)
        :param include_types: (bool) include zeep model type inspection
        :return: empty data model dictionary
        """
        if target_model == "add":
            model = get_model_dict(self._fetch_add_model(), include_types=include_types)
            return sanitize_model_dict(model) if sanitized else model
        else:
            raise NotImplementedError

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
        get_method = self._get_wsdl_obj(self._get_method_name)
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
        if not searchCriteria:
            # this is presumptive and may not work in all cases.
            list_method = self._get_wsdl_obj(self._list_method_name)
            supported_criteria = [element[0] for element in list_method.elements[0][1].type.elements]
            searchCriteria = {supported_criteria[0]: "%"}
        if not returnedTags:
            list_model = self._get_wsdl_obj(self._list_model_name)
            returnedTags = get_model_dict(list_model)
        elif isinstance(returnedTags, list):
            returnedTags = nullstring_dict(returnedTags)
        axl_resp = self._axl_methodcaller("list", searchCriteria=searchCriteria, returnedTags=returnedTags,
                                          skip=skip, first=first)
        try:
            axl_list = serialize_object(axl_resp)["return"][self._return_name]
            return [self.object_factory(self.__class__.__name__, item) for item in axl_list]
        except TypeError:
            return []

    @BaseAXLAPI.assert_supported
    def remove(self, **kwargs):
        """Remove method for API endpoint"""
        return self._serialize_uuid_resp("remove", **kwargs)

    @BaseAXLAPI.assert_supported
    def options(self, uuid, returnedChoices=None):
        """Return options for selected API endpoints"""
        kwargs = {
            "uuid": uuid,
            "returnedChoices": returnedChoices
        }
        options_method = methodcaller("".join(["get", self.__class__.__name__, "Options"]), **kwargs)
        axl_resp = options_method(self.connector.service)
        return self.object_factory(
            "".join([self.__class__.__name__, "Options"]),
            serialize_object(axl_resp)["return"][self._return_name]
        )


class DeviceAXLAPI(SimpleAXLAPI):
    """AXL API support additional device-related methods"""
    supported_methods = [
        "model", "create", "add", "get", "list", "update", "remove",
        "apply", "restart", "reset"
    ]

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
    """API extension for Thin AXL"""
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
                    serialize_object(axl_resp)["return"]["rows"])
            except KeyError:
                # single tuple response
                serialized_resp = element_list_to_ordered_dict(
                    serialize_object(axl_resp)["return"]["row"])
            except TypeError:
                # no SQL tuples
                serialized_resp = serialize_object(axl_resp)["return"]
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


class Device(BaseAXLAPI):
    """API Extension for restartable CUCM Devices"""
    _factory_descriptor = "device"
    supported_methods = ["login", "logout", "reset"]

    @BaseAXLAPI.assert_supported
    def login(self, deviceName, profileName, userId,
              loginDuration=0):
        axl_resp = self.connector.service.doDeviceLogin(deviceName, profileName, userId, loginDuration)
        return serialize_object(axl_resp)["return"]

    @BaseAXLAPI.assert_supported
    def logout(self, deviceName):
        axl_resp = self.connector.service.doDeviceLogout(deviceName)
        return serialize_object(axl_resp)["return"]

    @BaseAXLAPI.assert_supported
    def reset(self, deviceName, **kwargs):
        reset_kwargs = flatten_signature_kwargs(self.reset, locals())
        axl_resp = self.connector.service.doDeviceLogin(**reset_kwargs)
        return serialize_object(axl_resp)["return"]
