# TODOs

## UCM AXL Changes
 - rename references to MixIn classes
 - add `__copy__` and `__deep__` to base model class
 - implement manageable inheritance for `uuid`
 - determine how to cater for singleton classes
 - add environment variable support for AXL Connectors
 - Look at how best to make use of `__getattr__`, `__setattr__`, `__delattr__` and `__getattribute__`.  Check this
   between 3.6 and 2.7
 - Consider if `__hash__` is useful for working with object sets
 - Uniqueness based on `uuid` or `name`?  Is `name` globally significant for the whole api?
   Perhaps an `if` to support both?
 
## Future Extensions
 - add notes for incorporating PAWS and CUCM AXL WSDLs.  Should not be included in library.


## Clean-up
 - move `ucdevops` samples to separate repo
  