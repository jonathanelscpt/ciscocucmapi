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
    IllegalSQLStatement

)
from .._internal_utils import (
    has_valid_kwargs_keys,
    has_mandatory_keys,
    has_single_identifier,
    element_list_to_ordered_dict
)


class AbstractAXLAPI(ABC):
    """Abstract API Class enforcing common methods for AXL objects"""

    def __init__(self, client, object_factory):
        self._client = client
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

    def _axl_methodcaller(self, instance, action, **kwargs):
        try:
            axl_method = methodcaller("".join([action, instance.__class__.__name__]), **kwargs)
            return axl_method(self._client)
        except Fault as fault:
            raise AXLError(fault.message)

    def _serialize_axl_object(self, cls, action, **kwargs):
        axl_resp = self._axl_methodcaller(cls, action, **kwargs)
        return self._object_factory(
            cls.object_type(),
            serialize_object(axl_resp)["return"][cls.return_object_name()]
        )

    def _check_identifiers(self, **kwargs):
        if not has_single_identifier(self.identifiers(), kwargs):
            raise TypeError("Single identifier must be supplied from list: {identifiers}".format(
                identifiers=self.identifiers())
            )

    def _check_mandatory_attributes(self, **kwargs):
        if not has_mandatory_keys(kwargs, self.add_api_mandatory_attributes()):
            raise TypeError("Mandatory 'add' API attributes were not all provided: {mandatory}".format(
                mandatory=self.add_api_mandatory_attributes())
            )

    def add(self, **kwargs):
        self._check_mandatory_attributes(**kwargs)
        return self._serialize_axl_object(self, "add", **kwargs)

    def get(self, **kwargs):
        self._check_identifiers(**kwargs)
        return self._serialize_axl_object(self, "get", **kwargs)

    def update(self, **kwargs):
        self._check_identifiers(**kwargs)
        return self._serialize_axl_object(self, "update", **kwargs)

    def remove(self, **kwargs):
        self._check_identifiers(**kwargs)
        # todo - fix defect with return parsing - 'TypeError: string indices must be integers'
        self._serialize_axl_object(self, "remove", **kwargs)

    def list(self, search_criteria, returned_tags, skip=None, first=None):
        # todo - clean up
        if not has_valid_kwargs_keys(search_criteria, self.list_api_search_criteria()):
            raise IllegalSearchCriteria("Invalid Search Criteria for list API.  Supported criteria are: "
                                        "{search_criteria}".format(search_criteria=self.list_api_search_criteria())
                                        )
        axl_resp = self._client.listPhone(searchCriteria=search_criteria,
                                          returnedTags=returned_tags,
                                          skip=skip,
                                          first=first
                                          )
        axl_list = serialize_object(axl_resp)["return"][self.return_object_name()]
        return [self._object_factory(self.object_type(), _) for _ in axl_list]


class AbstractAXLDeviceAPI(AbstractAXLAPI):
    """Abstract Device API class with additional device methods"""

    def __init__(self, client, object_factory):
        super(AbstractAXLDeviceAPI, self).__init__(client, object_factory)

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
        self._serialize_axl_object(self, "apply", **kwargs)

    def restart(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._serialize_axl_object(self, "restart", **kwargs)

    def reset(self, **kwargs):
        self._check_identifiers(**kwargs)
        self._serialize_axl_object(self, "reset", **kwargs)


class AbstractThinAXLAPI(ABC):
    """Abstract API Class enforcing common methods for Thin AXL objects"""

    def __init__(self, client, object_factory):
        self._client = client
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

    def _extract_thin_axl_resp(self, axl_resp):
        thin_axl_resp = element_list_to_ordered_dict(
            serialize_object(axl_resp)["return"][self.return_object_name()]
        )
        return self._object_factory(self.object_type(), thin_axl_resp)

    def query(self, sql_statement=None):
        """Execute SQL query via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: SQL Thin AXL object
        """
        try:
            axl_resp = self._client.executeSQLQuery(sql=sql_statement)
            return self._extract_thin_axl_resp(axl_resp)
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)

    def update(self, sql_statement=None):
        """Execute SQL update via Thin AXL

        :param sql_statement: Informix-compliant SQL statement
        :return: SQL Thin AXL object
        """
        try:
            axl_resp = self._client.executeSQLQuery(sql=sql_statement)
            return self._extract_thin_axl_resp(axl_resp)
        except Fault as fault:
            raise IllegalSQLStatement(message=fault.message)
