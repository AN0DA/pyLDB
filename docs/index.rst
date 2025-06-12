pyLDB documentation
===================

pyLDB is a modern, Pythonic client library for the Local Data Bank (LDB, Bank Danych Lokalnych) API,
enabling easy, robust access to Polish official statistics for data science, research,
and applications.

Features
--------

- Clean, modular API client for all LDB endpoints
- Pandas DataFrame integration for tabular data
- Full support for pagination, filtering, and internationalization
- Built-in API key, language, and cache configuration
- Open source, tested, and ready for data analysis and visualization

Quick Start
-----------

.. code-block:: python

    from pyldb import LDB, LDBConfig
    ldb = LDB(LDBConfig(api_key="your-api-key"))  # Reads config from environment or defaults
    df = ldb.api.data.get_data_by_variable(variable_id="3643", year=2021)
    print(df.head())

Configuration
-------------

Configure your API key and options via environment variables or directly:

.. code-block:: python

    from pyldb import LDBConfig
    config = LDBConfig(api_key="your-api-key", language="en", use_cache=True)
    ldb = LDB(config=config)

Or set environment variables::

    export LDB_API_KEY=your-api-key
    export LDB_LANGUAGE=en

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   main_client
   api_clients
   config

Configuration Reference
-----------------------

.. toctree::
   :maxdepth: 2

   config

Contributing & License
----------------------

pyLDB is open source under the MIT license. Contributions and issues are welcome!
For details, see the `GitHub repository <https://github.com/AN0DA/pyldb>`_.

