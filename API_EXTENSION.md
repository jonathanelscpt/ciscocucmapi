# Steps to adding New API

The following are steps to adding a new AXL API endpoint to the the `uctoolkit` package:

 1. check method support for api endpoint, specifically checking for `apply`, `restart` and `reset` *(i.e. for devices)*
 1. add class API to correct `uctoolkit.api` module
 1. define class-level mandatory add attributes
 1. Assess any defaults and potential method overriding
 1. add api to connectors import and `UCMAXLConnector` class `__init__` method
