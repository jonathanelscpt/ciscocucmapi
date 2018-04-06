# TODOs

## UCM AXL Changes
 - **[DONE]** rename references to MixIn classes
 - add `__copy__` and `__deep__` to base model class
 - **[DONE]** implement manageable inheritance for `uuid`
 - determine how to cater for singleton classes
 - **[DONE]** add environment variable support for AXL Connectors
 - **[DONE]** Look at how best to make use of `__getattr__`, `__setattr__`, `__delattr__` and `__getattribute__`.  Check this
   between 3.6 and 2.7
 - Consider if `__hash__` is useful for working with object sets
 - Uniqueness based on `uuid` or `name`?  Is `name` globally significant for the whole api?
   Best to change to entire attr dict?
 - consider renaming zeep's `ServiceProxy` object for to allow for correct native inspection of zeep client
 
 
 ## Known Issues
 - `first` and `skip` for list not available for all apis - need child class extension to 
   include support for this for limited set of endpoints apis
 - **[DONE]** listPhone current hardcoded in`AbstractAXLAPI`
 - `__getitem__` and `__getattr__` interference
 
## Future Extensions
 - add notes for incorporating PAWS and CUCM AXL WSDLs.  Should not be included in library.


## Clean-up
 - move `ucdevops` samples to separate repo
 - convert `AbstractAXLDeviceAPI` to a mixin and move `_serialize_axl_object` and 
   `_axl_methodcaller` to module methods to prevent abstract inheritance mess
 - split `reset` method to separate mixin so that it is possible to segregate devices that 
   are not able to be reset (e.g. RoutePartition).  Clean up RoutePartition once done.
 - rename `_RETURN_OBJECT_NAME` to `_API_ENDPOINT_NAME`
  
## Steps to adding New API

 1. define class-level attributes
 1. add cl
 1. create api Classes to .api `__all__`
 1. add api to connectors import and `UCMAXLConnector` class `__init__` method
 1. add new data model class to `.model.__init__.py`
 1. add data model to `axl_data_models`, mapping to api class `object_type(cls)` return value
 1. analyze AXL schema for any custom method extensions to api or data model classes
