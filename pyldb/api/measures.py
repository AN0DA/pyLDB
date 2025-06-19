from typing import Any

from pyldb.api.client import BaseAPIClient


class MeasuresAPI(BaseAPIClient):
    """
    Client for the LDB /measures endpoints.

    Provides access to measure unit metadata (e.g. "number", "percent", "kg")
    used for variables in the Local Data Bank (LDB).
    """

    def list_measures(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        List all measure units, optionally sorted.

        Maps to: GET /measures

        Args:
            sort: Optional sorting order, e.g. 'Id', '-Id', 'Name', '-Name'.
            extra_query: Additional query parameters.

        Returns:
            List of measure unit metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort

        return self.fetch_single_result("measures", results_key="results", params=params, extra_query=extra_query)

    def get_measure(
        self,
        measure_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata for a specific measure unit.

        Maps to: GET /measures/{id}

        Args:
            measure_id: Measure unit identifier (integer).
            extra_query: Additional query parameters.

        Returns:
            Dictionary with measure unit metadata.
        """
        return self.fetch_single_result(f"measures/{measure_id}", extra_query=extra_query)

    def get_measures_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /measures endpoint.

        Maps to: GET /measures/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self.fetch_single_result("measures/metadata")

    async def alist_measures(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Async version of list_measures.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        return await self.afetch_single_result("measures", results_key="results", params=params, extra_query=extra_query)

    async def aget_measure(
        self,
        measure_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of get_measure.
        """
        return await self.afetch_single_result(f"measures/{measure_id}", extra_query=extra_query)

    async def aget_measures_metadata(self) -> dict[str, Any]:
        """
        Async version of get_measures_metadata.
        """
        return await self.afetch_single_result("measures/metadata")
