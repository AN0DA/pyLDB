Configuration
=============

.. automodule:: pyldb.config
    :members:
    :undoc-members:
    :show-inheritance:

The `LDBConfig` class manages all configuration for authentication, language, caching, and proxy settings.

Proxy Configuration
-------------------

The library supports HTTP/HTTPS proxy configuration through the following settings:

- ``proxy_url``: The URL of the proxy server (e.g., "http://proxy.example.com:8080")
- ``proxy_username``: Optional username for proxy authentication
- ``proxy_password``: Optional password for proxy authentication

These settings can be configured in three ways (in order of precedence):

1. Direct parameter passing when creating the config
2. Environment variables:
   - ``LDB_PROXY_URL``
   - ``LDB_PROXY_USERNAME``
   - ``LDB_PROXY_PASSWORD``
3. Default values (all None)

Example:

.. code-block:: python

    # Direct configuration
    config = LDBConfig(
        api_key="your-api-key",
        proxy_url="http://proxy.example.com:8080",
        proxy_username="user",
        proxy_password="pass"
    )

    # Or through environment variables
    # export LDB_PROXY_URL="http://proxy.example.com:8080"
    # export LDB_PROXY_USERNAME="user"
    # export LDB_PROXY_PASSWORD="pass"
