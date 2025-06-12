Main Client
===========

.. automodule:: pyldb.client
    :members:
    :undoc-members:
    :show-inheritance:

The `LDB` class is the main entry point for the library. While it currently provides access to the LDB API through the `.api` attribute,
it is designed to be extended with additional features for data processing, analysis, and visualization in future versions.

API Access
---------

Currently, the main functionality is provided through the `.api` attribute, which gives access to all LDB API endpoints.
See the :doc:`API Clients <api_clients>` documentation for details about available endpoints.

Future Features
--------------

The main client is being developed to include:

- Data processing capabilities
- Statistical analysis tools
- Data visualization helpers
- Geographic data processing
- Caching and performance optimizations 
