# -*- coding: utf-8 -*-
"""Abstract AXL APIs"""

from abc import (
    ABC,
    abstractmethod
)
from operator import methodcaller
from collections import OrderedDict

from zeep.helpers import serialize_object
from zeep.exceptions import Fault
from zeep.xsd.elements.indicators import Choice
from zeep.xsd.elements.indicators import Sequence
from zeep.xsd.elements.element import Element

from ..exceptions import (
    AXLError,
    IllegalSQLStatement
)
from .._internal_utils import (
    has_mandatory_keys,
    check_valid_attribute_req_dict,
    element_list_to_ordered_dict,
    downcase_string
)
from ..helpers import (
    get_model_dict,
    sanitize_data_model_dict
)


def _extract_get_choices(obj):
    """Recursively inspects a zeep object and extracts the available choices available when performing
    the specific AXL call, as defined in AXL xsd.

    :param obj: zeep Element data structure type
    :return: nested tuple of the xsd-defined choices for the AXL method
    """
    if isinstance(obj, (Choice, Sequence)):
        return tuple([_extract_get_choices(_) for _ in obj])
    elif isinstance(obj, Element):
        return obj.name
    else:
        raise TypeError("Only Choice, Sequence and Element classes inspected, Type '{cls}' found.".format(
            cls=obj.__class__.__name__
            )
        )


class AbstractAXLAPI(ABC):
    """Abstract API Class enforcing common methods for AXL objects"""

    def __init__(self, connector, object_factory):
        super().__init__()
        self.connector = connector
        self.object_factory = object_factory
        self._return_name = downcase_string(self.__class__.__name__)

        add_model_name = "".join(["X", self.__class__.__name__])
        get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
        get_model_name = "".join(["R", self.__class__.__name__])
        update_method_name = "".join(["Update", self.__class__.__name__, "Req"])
        list_method_name = "".join(["List", self.__class__.__name__, "Req"])
        list_model_name = "".join(["L", self.__class__.__name__])

        self._wsdl_objects = {
            "add_method": NotImplementedError,  # not used in class
            "add_model": self._get_wsdl_obj(add_model_name),
            "get_method": self._get_wsdl_obj(get_method_name),
            "get_model": self._get_wsdl_obj(get_model_name),
            "list_method": self._get_wsdl_obj(list_method_name),
            "list_model": self._get_wsdl_obj(list_model_name),
            "update_method": self._get_wsdl_obj(update_method_name),
            "update_model": NotImplementedError,  # doesn't exist in schema
            "name_and_guid_model": self._get_wsdl_obj("NameAndGUIDRequest")  # used in many AXL requests
        }

    @property
    @abstractmethod
    def add_api_mandatory_attributes(self):
        raise NotImplementedError

    @staticmethod
    def _check_identifiers(obj, **kwargs):
        identifiers = _extract_get_choices(obj.elements_nested[0][1][0])
        if not check_valid_attribute_req_dict(identifiers, kwargs):
            raise TypeError("Supplied identifiers not supported for 'get' API call: {identifiers}".format(
                identifiers=identifiers)
            )

    def _get_wsdl_obj(self, obj_name):
        """Get an empty python-zeep complex type

        :param obj_name: name of AXL type
        :return: empty zeep complex type obj
        """
        return self.connector.client.get_type('ns0:{name}'.format(
            name=obj_name
        ))

    def _axl_methodcaller(self, action, **kwargs):
        try:
            axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
            return axl_method(self.connector.service)
        except Fault as fault:
            raise AXLError(fault.message)

    def _serialize_axl_object(self, action, **kwargs):
        """Builds and AXL methodcaller using given action verb and the object type,
        serializes the response and uses the resultant dict to instantiate a data model object

        :param action: AXL action verb - 'add', 'get', 'update', 'remove', etc.
        :param kwargs: AXL method attribute kwargs dictionary
        :return: Data Model object containing the serialized response data dict
        """
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return self.object_factory(
            self.__name__,
            serialize_object(axl_resp)["return"][self._return_name]
        )

    def _serialize_uuid_only_resp(self, action, **kwargs):
        """Serialize commons responses that return a uuid string only

        :param action: axl method verb
        :param kwargs: dict of method attributes
        :return: (str) uuid
        """
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return serialize_object(axl_resp)["return"]

    def model(self, sanitized=True, target_cls=OrderedDict):
        """Get a empty serialized 'add' model for the API endpoint useful for inspecting the endpoint's
        schema and future template generation.

        :param sanitized: collapse zeep's interpretation of the xsd nested dicts
        with '_value_1' and 'uuid' keys into a simple k,v pair with v as a (str)
        :param target_cls: dict or OrderedDict
        :return: empty data model dictionary
        """
        if sanitized:
            return sanitize_data_model_dict(
                get_model_dict(self._wsdl_objects["add_model"], target_cls=target_cls)
            )
        else:
            return get_model_dict(self._wsdl_objects["add_model"], target_cls=target_cls)

    def create(self, **kwargs):
        """Create AXL object locally for pre-processing"""
        axl_add_method = methodcaller(self._wsdl_objects["add_model"].__class__.__name__, **kwargs)
        axl_add_obj = axl_add_method(self.connector.model_factory)
        return self.object_factory(self.__name__, serialize_object(axl_add_obj))

    def add(self, **kwargs):
        if not has_mandatory_keys(kwargs, self.add_api_mandatory_attributes):
            raise TypeError("Mandatory 'add' API attributes were not all provided: {mandatory}".format(
                mandatory=self.add_api_mandatory_attributes)
            )
        # wrap kwargs ourselves to simplify the 'add' method.
        wrapped_kwargs = {
            self._return_name: kwargs
        }
        return self._serialize_uuid_only_resp("add", **wrapped_kwargs)

    def get(self, returned_tags=None, **kwargs):
        kwargs["returnedTags"] = returned_tags
        self._check_identifiers(self._wsdl_objects["get_method"], **kwargs)
        return self._serialize_axl_object("get", **kwargs)

    def update(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["update_method"], **kwargs)
        return self._serialize_uuid_only_resp("update", **kwargs)

    def list(self, search_criteria=None, returned_tags=None, skip=None, first=None):
        supported_criteria = [element[0] for element in self._wsdl_objects["list_method"].elements[0][1].type.elements]
        list_api_kwargs = {
            "searchCriteria": search_criteria if search_criteria else {supported_criteria[0]: "%"},
            "returnedTags": returned_tags if returned_tags else get_model_dict(self._wsdl_objects["list_model"]),
            "skip": skip,
            "first": first
        }
        axl_resp = self._axl_methodcaller("list", **list_api_kwargs)
        axl_list = serialize_object(axl_resp)["return"][self._return_name]
        return [self.object_factory(self.__name__, item) for item in axl_list]

    def remove(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_uuid_only_resp("remove", **kwargs)


class AbstractAXLDeviceAPI(AbstractAXLAPI):
    """Abstract Device API class with additional device methods"""

    @property
    @abstractmethod
    def add_api_mandatory_attributes(self):
        raise NotImplementedError

    def apply(self, **kwargs):
        """Apply config to CUCM device

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_uuid_only_resp("apply", **kwargs)

    def restart(self, **kwargs):
        """Restart CUCM device

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_uuid_only_resp("restart", **kwargs)

    def reset(self, **kwargs):
        """Reset CUCM device

        :param kwargs: uuid or name
        :return: (str) uuid
        """
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        return self._serialize_uuid_only_resp("reset", **kwargs)


class ThinAXL:
    """Abstract API Class enforcing common methods for Thin AXL objects"""

    def __init__(self, connector, object_factory):
        self._connector = connector
        self._object_factory = object_factory

    def query(self, sql_statement):
        """Execute SQL query via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: SQL Thin AXL data model object
        """
        try:
            axl_resp = self._connector.service.executeSQLQuery(sql=sql_statement)
            try:
                serialized_thin_axl_resp = element_list_to_ordered_dict(
                    serialize_object(axl_resp)["return"]["rows"]
                )
            # AXL supplies different keyword used for single row return
            except KeyError:
                serialized_thin_axl_resp = element_list_to_ordered_dict(
                    serialize_object(axl_resp)["return"]["row"]
                )
            return self._object_factory(self.__name__, serialized_thin_axl_resp)
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)

    def update(self, sql_statement):
        """Execute SQL update via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: (int) rows updated
        """
        try:
            axl_resp = self._connector.service.executeSQLUpdate(sql=sql_statement)
            return serialize_object(axl_resp)["return"]["rowsUpdated"]
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)
