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
    IllegalSearchCriteria,
    IllegalSQLStatement,
    AXLAttributeError

)
from .._internal_utils import (
    has_valid_kwargs_keys,
    has_mandatory_keys,
    all_attributes_exist_with_null_intersection,
    element_list_to_ordered_dict
)
from ..model import AXLDataModel


class AbstractAXLAPI(ABC):
    """Abstract API Class enforcing common methods for AXL objects"""

    def __init__(self, connector, object_factory):
        self._connector = connector
        self._object_factory = object_factory
        super(AbstractAXLAPI, self).__init__()

    @classmethod
    @abstractmethod
    def identifiers(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def object_type(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def return_object_name(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def add_api_mandatory_attributes(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def list_api_search_criteria(cls):
        raise NotImplementedError

    def _axl_methodcaller(self, action, **kwargs):
        try:
            axl_method = methodcaller("".join([action, self.__class__.__name__]), **kwargs)
            return axl_method(self._connector.service)
        except Fault as fault:
            raise AXLError(fault.message)

    def _serialize_axl_object(self, action, **kwargs):
        axl_resp = self._axl_methodcaller(action, **kwargs)
        return self._object_factory(
            self.object_type(),
            serialize_object(axl_resp)["return"][self.return_object_name()]
        )

    def _check_identifiers(self, **kwargs):
        if not all_attributes_exist_with_null_intersection(self.identifiers(), kwargs):
            raise TypeError("Single identifier must be supplied from list: {identifiers}".format(
                identifiers=self.identifiers())
            )

    def _check_mandatory_attributes(self, **kwargs):
        if not has_mandatory_keys(kwargs, self.add_api_mandatory_attributes()):
            raise TypeError("Mandatory 'add' API attributes were not all provided: {mandatory}".format(
                mandatory=self.add_api_mandatory_attributes())
            )

    def create(self, **kwargs):
        try:
            # all AXL API endpoints include an "X" naming prefix, so we can safely using the
            # __class__.__name__ concat paradigm as is already used for method-calling
            create_method = methodcaller("".join(["X", self.__class__.__name__]), **kwargs)
            x_obj = create_method(self._connector.model_factory)
            return self._object_factory(self.object_type(), serialize_object(x_obj))
        except TypeError as type_error:
            raise AXLAttributeError(type_error)

    def add(self, *args, **kwargs):
        # AXL's 'add' APIs expects kwargs options wrapped in tags with the api endpoint's return object name
        # We wrap this ourselves to simplify the Python 'add' interface.
        wrapped_kwargs = {
            self.return_object_name(): serialize_object(args[0]) if len(args) == 1 and isinstance(args[0], AXLDataModel)
            else kwargs
        }
        self._check_mandatory_attributes(**wrapped_kwargs[self.return_object_name()])
        self._axl_methodcaller("add", **wrapped_kwargs)

    def get(self, **kwargs):
        self._check_identifiers(**kwargs)
        return self._serialize_axl_object("get", **kwargs)

    def update(self, **kwargs):
        self._check_identifiers(**kwargs)  # todo - is this required in AXL or not?
        self._axl_methodcaller("update", **kwargs)

    def list(self, search_criteria, returned_tags, skip=None, first=None):
        # todo - simply leave skip and first - ignored if not in use?
        if not has_valid_kwargs_keys(search_criteria, self.list_api_search_criteria()):
            raise IllegalSearchCriteria(
                "Invalid Search Criteria for list API.  Supported criteria are: "
                "{search_criteria}".format(search_criteria=self.list_api_search_criteria())
            )
        list_api_kwargs = {
            "searchCriteria": search_criteria,
            "returnedTags": returned_tags,
            "skip": skip,
            "first": first
        }
        axl_resp = self._axl_methodcaller("list", **list_api_kwargs)
        axl_list = serialize_object(axl_resp)["return"][self.return_object_name()]
        return [self._object_factory(self.object_type(), _) for _ in axl_list]

    def remove(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._axl_methodcaller("remove", **kwargs)


class AbstractAXLDeviceAPI(AbstractAXLAPI):
    """Abstract Device API class with additional device methods"""

    def __init__(self, connector, object_factory):
        super(AbstractAXLDeviceAPI, self).__init__(connector, object_factory)

    @classmethod
    @abstractmethod
    def identifiers(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def object_type(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def return_object_name(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def add_api_mandatory_attributes(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def list_api_search_criteria(cls):
        raise NotImplementedError

    def apply(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._axl_methodcaller("apply", **kwargs)

    def restart(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._axl_methodcaller("restart", **kwargs)

    def reset(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._axl_methodcaller("reset", **kwargs)


class AbstractThinAXLAPI(ABC):
    """Abstract API Class enforcing common methods for Thin AXL objects"""

    def __init__(self, connector, object_factory):
        self._connector = connector
        self._object_factory = object_factory
        super(AbstractThinAXLAPI, self).__init__()

    @classmethod
    @abstractmethod
    def object_type(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def return_object_name(cls):
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
            # todo - confirm that update returns an int!
            return serialize_object(axl_resp)["return"]["rowsUpdated"]
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)
