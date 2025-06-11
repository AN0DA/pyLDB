from typing import Any

from pyldb.api.client import BaseAPIClient


class AggregatesAPI(BaseAPIClient):
    """
    Client for the LDB /aggregates endpoints.

    Provides access to aggregation level metadata, listing and detail of
    aggregates, and aggregates API metadata within the Local Data Bank (LDB).
    """

    def list_aggregates(
        self,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all aggregates, optionally sorted.

        Maps to: GET /aggregates

        Args:
            sort: Sorting order, e.g., 'Id', '-Id', 'Name', '-Name', etc.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of aggregate metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort

        if all_pages:
            return self.fetch_all_results(
                "aggregates",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("aggregates", params=params, extra_query=extra_query)
            return resp.get("results", [])

    def get_aggregate_info(self, aggregate_id: str) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific aggregate.

        Maps to: GET /aggregates/{id}

        Args:
            aggregate_id: Aggregate identifier.

        Returns:
            Dictionary with aggregate metadata.
        """
        return self._make_request(f"aggregates/{aggregate_id}")

    def list_aggregates_metadata(
        self,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all aggregates metadata.

        Maps to: GET /aggregates/metadata

        Args:
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of aggregate metadata dictionaries.
        """
        if all_pages:
            return self.fetch_all_results(
                "aggregates/metadata",
                params={},
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("aggregates/metadata", params={}, extra_query=extra_query)
            return resp.get("results", [])

    def get_aggregate_metadata_info(self, aggregate_id: str) -> dict[str, Any]:
        """
        Retrieve metadata for a specific aggregate (from /aggregates/metadata/{id}).

        Maps to: GET /aggregates/metadata/{id}

        Args:
            aggregate_id: Aggregate identifier.

        Returns:
            Dictionary with aggregate metadata details.
        """
        return self._make_request(f"aggregates/metadata/{aggregate_id}")

    def get_aggregates_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata for the /aggregates endpoint.

        Maps to: GET /aggregates/metadata (returns API info, not list of aggregates)

        Args:
            extra_query: Additional query parameters, e.g., {'lang': 'en'}.

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self._make_request("aggregates/metadata", extra_query=extra_query)
