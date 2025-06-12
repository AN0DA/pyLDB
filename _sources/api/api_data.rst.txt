Data API
========

.. automodule:: pyldb.api.data
    :members:
    :undoc-members:
    :show-inheritance:

The `DataAPI` class provides access to all /data endpoints, including:

- Fetching data by variable, unit, attribute, locality, etc.
- Checking data availability for any entity
- Querying the /data/metadata endpoint
- Full support for pagination, filtering, and result normalization as Pandas DataFrames

Example usage:

.. code-block:: python

    df = ldb.api.data.get_data_by_variable(variable_id="3643", year=2021)
    print(df.head())
