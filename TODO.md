# TODO

## UCM AXL Changes

### Outstanding

 - add `__copy__` and `__deep__` to base model class
 - determine how to cater for singleton classes
 
 
 ## Known Issues
 
 - `first` and `skip` for list not available for all apis - need child class extension to 
   include support for this for limited set of endpoints apis
 - revisit `__getitem__` and `__getattr__` interference


## Clean-up

 - split `reset` method to separate mixin so that it is possible to segregate devices that 
   are not able to be reset (e.g. RoutePartition).  Clean up RoutePartition once done.

 
## Completed

 - **[DONE]** rename references to MixIn classes
 - **[DONE]** implement manageable inheritance for `uuid`
 - **[DONE]** add environment variable support for AXL Connectors
 - **[DONE]** Look at how best to make use of `__getattr__`, `__setattr__`, `__delattr__` and `__getattribute__`.  Check this
 - **[DONE]** consider renaming zeep's `ServiceProxy` object for to allow for correct native inspection of zeep client
 - **[DONE]** Uniqueness based on `uuid` or `name`?  Is `name` globally significant for the whole api?
 - **[DONE]** listPhone current hardcoded in`AbstractAXLAPI`
 - **[DONE]** move `ucdevops` samples to separate repo
 - **[DONE]** convert `AbstractAXLDeviceAPI` to a mixin and move `_serialize_axl_object` and 
   `_axl_methodcaller` to module methods to prevent abstract inheritance mess
 - **[DROPPED - private method issues]** convert to absolute package imports
 - **[DONE]** fix `__eq__` to compare `_axl_dict`
 - **[DONE]** clean up `ThinAXLAPI`
 - **[DROPPED - refactoring]**rename `_RETURN_OBJECT_NAME` to `_API_ENDPOINT_NAME`
 - **[DONE]** Check if sql updates are returning the number of rows affected
 - **[DONE]** extend use of zeep factory in connector to abstract classes


## Future Extensions
 - add notes for incorporating PAWS and CUCM AXL WSDLs.  Should not be included in library.
 - Add support for async client
