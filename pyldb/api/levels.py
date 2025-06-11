from typing import Any

from pyldb.api.client import BaseAPIClient


class LevelsAPI(BaseAPIClient):
    """
    Client for the LDB /levels endpoints.

    Provides access to administrative unit aggregation levels and their metadata
    in the Local Data Bank (LDB).
    """

    def list_levels(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        List all administrative unit aggregation levels.

        Maps to: GET /levels

        Args:
            sort: Optional sorting order, e.g., 'Id', '-Id', 'Name', '-Name'.
            extra_query: Additional query parameters.

        Returns:
            List of aggregation level metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort

        resp = self._make_request("levels", params=params, extra_query=extra_query)
        return resp.get("results", [])

    def get_level_info(
        self,
        level_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata for a specific aggregation level.

        Maps to: GET /levels/{id}

        Args:
            level_id: Aggregation level identifier (integer).
            extra_query: Additional query parameters.

        Returns:
            Dictionary with level metadata.
        """
        return self._make_request(f"levels/{level_id}", extra_query=extra_query)

    def get_levels_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /levels endpoint.

        Maps to: GET /levels/metadata

        Args:
            extra_query: Additional query parameters, e.g., {'lang': 'en'}.

        Returns:
            Dictionary with API metadata and versioning info.
        """
        return self._make_request("levels/metadata", extra_query=extra_query)
