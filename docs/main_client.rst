Main Client
===========

.. automodule:: pyldb.client
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

The :class:`pyldb.client.LDB` class is the main entry point for the library. It provides access to all LDB API endpoints via the ``.api`` attribute.

.. seealso::
   - :doc:`api_clients` for endpoint details
   - :doc:`config` for configuration options

API Access
----------

The main functionality is provided through the ``.api`` attribute, which gives access to all LDB API endpoints. For example:

.. code-block:: python

    from pyldb import LDB
    ldb = LDB()
    data = ldb.api.data.get_data_by_variable(variable_id="3643", year=2021)

See the :doc:`API Clients <api_clients>` documentation for details about available endpoints.

Future Features
---------------

The main client is being developed to include:

- Data processing capabilities
- Statistical analysis tools
- Data visualization helpers
- Geographic data processing
- Caching and performance optimizations
