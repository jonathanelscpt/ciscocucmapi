=====================
Environment Variables
=====================

.. inclusion-marker-do-not-remove

 The following env vars are supported for ease of use:

 - :code:`AXL_USERNAME`
 - :code:`AXL_PASSWORD`
 - :code:`AXL_FQDN`
 - :code:`AXL_WSDL_URL`


This allows for simplified usage in single-integration scenarios:

.. code-block:: python

    UCMAXLConnector()


Alternatively, axl-related variables can be supplied directly to :code:`UCMAXLConnector()`:

.. code-block:: python

    UCMAXLConnector(username='axl', password='password', fqdn='192.168.99.99')
