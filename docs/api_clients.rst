API Clients
===========

The pyLDB library provides a comprehensive set of API clients for interacting with the Local Data Bank (LDB) API.
All API endpoints are accessible through the main client's `.api` attribute. See :doc:`Main Client <main_client>` for details about the main client.

.. list-table:: Available API Endpoints
   :header-rows: 1

   * - Endpoint
     - Class
     - Description
   * - Aggregates
     - :class:`pyldb.api.aggregates.AggregatesAPI`
     - Aggregation level metadata and details
   * - Attributes
     - :class:`pyldb.api.attributes.AttributesAPI`
     - Attribute metadata and details
   * - Data
     - :class:`pyldb.api.data.DataAPI`
     - Statistical data access (variables, units, localities)
   * - Levels
     - :class:`pyldb.api.levels.LevelsAPI`
     - Administrative unit aggregation levels
   * - Measures
     - :class:`pyldb.api.measures.MeasuresAPI`
     - Measure unit metadata
   * - Subjects
     - :class:`pyldb.api.subjects.SubjectsAPI`
     - Subject hierarchy and metadata
   * - Units
     - :class:`pyldb.api.units.UnitsAPI`
     - Administrative unit metadata
   * - Variables
     - :class:`pyldb.api.variables.VariablesAPI`
     - Variable metadata and details
   * - Version
     - :class:`pyldb.api.version.VersionAPI`
     - API version and build info
   * - Years
     - :class:`pyldb.api.years.YearsAPI`
     - Available years for data

.. note::
   All API clients are accessible via ``ldb.api.<endpoint>`` (e.g., ``ldb.api.data.get_data_by_variable(...)``).

.. seealso::
   For configuration options, see :doc:`config`.
   For main client usage, see :doc:`main_client`.

Async Usage
-----------

All API clients support async methods for high-performance and concurrent applications. Async methods are named with an `a` prefix (e.g., `aget_data_by_variable`).

.. code-block:: python

    import asyncio
    from pyldb import LDB

    async def main():
        ldb = LDB()
        data = await ldb.api.data.aget_data_by_variable(variable_id="3643", year=2021)
        print(data)

    asyncio.run(main())

.. note::
   Async methods are available for all endpoints. See the API reference below for details.

Aggregates
~~~~~~~~~~

.. automodule:: pyldb.api.aggregates
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Attributes
~~~~~~~~~~

.. automodule:: pyldb.api.attributes
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Data
~~~~

.. automodule:: pyldb.api.data
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Levels
~~~~~~

.. automodule:: pyldb.api.levels
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Measures
~~~~~~~~

.. automodule:: pyldb.api.measures
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Subjects
~~~~~~~~

.. automodule:: pyldb.api.subjects
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Units
~~~~~

.. automodule:: pyldb.api.units
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Variables
~~~~~~~~~

.. automodule:: pyldb.api.variables
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Version
~~~~~~~

.. automodule:: pyldb.api.version
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Years
~~~~~

.. automodule:: pyldb.api.years
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
    :noindex: