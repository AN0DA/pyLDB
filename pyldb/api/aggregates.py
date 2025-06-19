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
        extra_query: dict[str, Any] | None = None,
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

        return self.fetch_single_result("aggregates", results_key="results", params=params, extra_query=extra_query)

    def get_aggregate(self, aggregate_id: str) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific aggregate.

        Maps to: GET /aggregates/{id}

        Args:
            aggregate_id: Aggregate identifier.

        Returns:
            Dictionary with aggregate metadata.
        """
        return self.fetch_single_result(f"aggregates/{aggregate_id}")

    def get_aggregates_metadata(self) -> dict[str, Any]:
        """
        List all aggregates metadata.

        Maps to: GET /aggregates/metadata

        Returns:
            List of aggregate metadata dictionaries.
        """
        return self.fetch_single_result("aggregates/metadata")

    async def alist_aggregates(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Async version of list_aggregates.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        return await self.afetch_single_result(
            "aggregates", results_key="results", params=params, extra_query=extra_query
        )

    async def aget_aggregate(self, aggregate_id: str) -> dict[str, Any]:
        """
        Async version of get_aggregate.
        """
        return await self.afetch_single_result(f"aggregates/{aggregate_id}")

    async def aget_aggregates_metadata(self) -> dict[str, Any]:
        """
        Async version of get_aggregates_metadata.
        """
        return await self.afetch_single_result("aggregates/metadata")
