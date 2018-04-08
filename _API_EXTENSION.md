# Steps to adding New API

The following are steps to adding a new AXL API endpoint to the the `uctoolkit` package:

 1. check method support for api endpoint, specfically checking for 
 `apply`, `restart` and `reset` *(i.e. for devices)*
 1. add class API to correct `uctoolkit.api` module
 1. define custom class-level attributes
 1. add api Class to `.api.__init__.py`'s `__all__` list
 1. add api to connectors import and `UCMAXLConnector` class `__init__` method
 1. add new data model class to `.model.__init__.py`
 1. add data model to `axl_data_models` in `.model.__init__.py`, mapping to 
    api class `object_type(cls)` return value
 1. analyze AXL schema for any custom method extensions to api or data model classes
