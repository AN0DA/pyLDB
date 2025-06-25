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
        if extra_query:
            params.update(extra_query)
        return self.fetch_all_results("measures", params=params)

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
        params = extra_query if extra_query else None
        return self.fetch_single_result(f"measures/{measure_id}", params=params)

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
        Asynchronously list all measure units, optionally sorted.

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
        if extra_query:
            params.update(extra_query)
        return await self.afetch_single_result("measures", results_key="results", params=params)

    async def aget_measure(
        self,
        measure_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Asynchronously retrieve metadata for a specific measure unit.

        Maps to: GET /measures/{id}

        Args:
            measure_id: Measure unit identifier (integer).
            extra_query: Additional query parameters.

        Returns:
            Dictionary with measure unit metadata.
        """
        params = extra_query if extra_query else None
        return await self.afetch_single_result(f"measures/{measure_id}", params=params)

    async def aget_measures_metadata(self) -> dict[str, Any]:
        """
        Asynchronously retrieve general metadata and version information for the /measures endpoint.

        Maps to: GET /measures/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return await self.afetch_single_result("measures/metadata")
