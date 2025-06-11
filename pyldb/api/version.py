from typing import Any

from pyldb.api.client import BaseAPIClient


class VersionAPI(BaseAPIClient):
    """
    Client for the BDL /version endpoint.

    Provides access to version and build information for the Bank Danych Lokalnych (BDL) API.
    """

    def get_version(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve API version and build information.

        Maps to: GET /version

        Args:
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.

        Returns:
            Dictionary with version and build information.
        """
        return self._make_request("version", extra_query=extra_query)
