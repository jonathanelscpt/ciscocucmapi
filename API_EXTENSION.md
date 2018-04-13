# Steps to adding New API

The following are steps to adding a new AXL API endpoint to the the `uctoolkit` package:

 1. check method support for api endpoint, specifically checking for `apply`, `restart` and `reset` *(i.e. for devices)*
 1. add class API to correct `uctoolkit.api` module
 1. define class-level mandatory add attributes
 1. Assess any defaults and potential method overriding
 1. add api Class to `.api.__init__.py`'s `__all__` list
 1. add api to connectors import and `UCMAXLConnector` class `__init__` method
 1. review of any custom data model extensions, and update `.model.__init__.py`'s factory `defaultdict` if necessary
 1. analyze AXL schema for any custom method extensions to api or data model classes
