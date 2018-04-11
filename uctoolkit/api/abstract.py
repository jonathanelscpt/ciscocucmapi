# -*- coding: utf-8 -*-


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from abc import (
    ABC,
    abstractmethod
)
from operator import methodcaller

from zeep.helpers import serialize_object
from zeep.exceptions import Fault

from ..exceptions import (
    AXLError,
    IllegalSQLStatement

)
from .._internal_utils import (
    has_mandatory_keys,
    check_valid_attribute_req_dict,
    element_list_to_ordered_dict,
    extract_get_choices
)
from ..utils import get_model_dict


class AbstractAXLAPI(ABC):
    """Abstract API Class enforcing common methods for AXL objects"""

    def __init__(self, connector, object_factory):
        super(AbstractAXLAPI, self).__init__()
        self.connector = connector
        self.object_factory = object_factory

        _add_model_name = "".join(["X", self.__class__.__name__])
        _get_method_name = "".join(["Get", self.__class__.__name__, "Req"])
        _get_model_name = "".join(["R", self.__class__.__name__])
        _update_method_name = "".join(["Update", self.__class__.__name__, "Req"])
        _list_method_name = "".join(["List", self.__class__.__name__, "Req"])
        _list_model_name = "".join(["L", self.__class__.__name__])

        self._wsdl_objects = {
            "add_method": NotImplementedError,  # not used in class
            "add_model": self._get_wsdl_obj(_add_model_name),
            "get_method": self._get_wsdl_obj(_get_method_name),
            "get_model": self._get_wsdl_obj(_get_model_name),
            "list_method":self._get_wsdl_obj(_list_method_name),
            "list_model": self._get_wsdl_obj(_list_model_name),
            "update_method": self._get_wsdl_obj(_update_method_name),
            "update_model": NotImplementedError,  # doesn't exist in schema
            "name_and_guid_model": self._get_wsdl_obj("NameAndGUIDRequest")  # used in many AXL requests
        }

    @property
    @abstractmethod
    def object_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def return_object_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def add_api_mandatory_attributes(self):
        raise NotImplementedError

    @staticmethod
    def _check_identifiers(method_obj, **kwargs):
        _identifiers = extract_get_choices(method_obj.elements_nested[0][1][0])
        if not check_valid_attribute_req_dict(_identifiers, kwargs):
            raise TypeError("Supplied identifiers not supported for 'get' API call: {identifiers}".format(
                identifiers=_identifiers)
            )

    def _axl_methodcaller(self, action, **kwargs):
        try:
            axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
            return axl_method(self.connector.service)
        except Fault as fault:
            raise AXLError(fault.message)

    def _serialize_axl_object(self, action, **kwargs):
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return self.object_factory(
            self.object_type,
            serialize_object(axl_resp)["return"][self.return_object_name]
        )

    def _get_wsdl_obj(self, obj_name):
        return self.connector.client.get_type('ns0:{req_obj_name}'.format(
            req_obj_name=obj_name
        ))

    def create(self, **kwargs):
        """Create AXL object locally for pre-processing"""
        _create = methodcaller(self._wsdl_objects["add_model"].__class__.__name__, **kwargs)
        _add_obj = _create(self.connector.model_factory)
        return self.object_factory(self.object_type, serialize_object(_add_obj))

    def add(self, **kwargs):
        if not has_mandatory_keys(kwargs, self.add_api_mandatory_attributes):
            raise TypeError("Mandatory 'add' API attributes were not all provided: {mandatory}".format(
                mandatory=self.add_api_mandatory_attributes)
            )
        # wrap kwargs ourselves to simplify the 'add' method.
        wrapped_kwargs = {
            self.return_object_name: kwargs
        }
        self._axl_methodcaller("add", **wrapped_kwargs)

    def get(self, returned_tags=None, **kwargs):
        kwargs["returnedTags"] = returned_tags
        self._check_identifiers(self._wsdl_objects["get_method"], **kwargs)
        return self._serialize_axl_object("get", **kwargs)

    def update(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["update_method"], **kwargs)
        self._axl_methodcaller("update", **kwargs)

    def list(self, search_criteria=None, returned_tags=None, skip=None, first=None):
        _supported_criteria = [element[0] for element in self._wsdl_objects["list_method"].elements[0][1].type.elements]
        list_api_kwargs = {
            "searchCriteria": search_criteria if search_criteria else {_supported_criteria[0]: "%"},
            "returnedTags": returned_tags if returned_tags else get_model_dict(self._wsdl_objects["list_model"]),
            "skip": skip,
            "first": first
        }
        axl_resp = self._axl_methodcaller("list", **list_api_kwargs)
        axl_list = serialize_object(axl_resp)["return"][self.return_object_name]
        return [self.object_factory(self.object_type, item) for item in axl_list]

    def remove(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._axl_methodcaller("remove", **kwargs)


class AbstractAXLDeviceAPI(AbstractAXLAPI):
    """Abstract Device API class with additional device methods"""

    def __init__(self, connector, object_factory):
        super(AbstractAXLDeviceAPI, self).__init__(connector, object_factory)

    @property
    @abstractmethod
    def object_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def return_object_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def add_api_mandatory_attributes(self):
        raise NotImplementedError

    def apply(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._axl_methodcaller("apply", **kwargs)

    def restart(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._axl_methodcaller("restart", **kwargs)

    def reset(self, **kwargs):
        self._check_identifiers(self._wsdl_objects["name_and_guid_model"], **kwargs)
        self._axl_methodcaller("reset", **kwargs)


class AbstractThinAXLAPI(ABC):
    """Abstract API Class enforcing common methods for Thin AXL objects"""

    def __init__(self, connector, object_factory):
        self._connector = connector
        self._object_factory = object_factory
        super(AbstractThinAXLAPI, self).__init__()

    @property
    @abstractmethod
    def object_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def return_object_name(self):
        raise NotImplementedError

    def _extract_thin_axl_query_resp(self, axl_resp):
        thin_axl_resp = element_list_to_ordered_dict(
            serialize_object(axl_resp)["return"]["rows"]
        )
        return self._object_factory(self.object_type(), thin_axl_resp)

    def query(self, sql_statement=None):
        """Execute SQL query via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: SQL Thin AXL object
        """
        try:
            axl_resp = self._connector.service.executeSQLQuery(sql=sql_statement)
            return self._extract_thin_axl_query_resp(axl_resp)
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)

    def update(self, sql_statement=None):
        """Execute SQL update via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: (int) rows updated
        """
        try:
            axl_resp = self._connector.service.executeSQLUpdate(sql=sql_statement)
            # todo - confirm that update returns an int
            return serialize_object(axl_resp)["return"]["rowsUpdated"]
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)
