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

        return self.fetch_single_result("levels", results_key="results", params=params, extra_query=extra_query)

    def get_level(
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
        return self.fetch_single_result(f"levels/{level_id}", extra_query=extra_query)

    def get_levels_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /levels endpoint.

        Maps to: GET /levels/metadata

        Returns:
            Dictionary with API metadata and versioning info.
        """
        return self.fetch_single_result("levels/metadata")
