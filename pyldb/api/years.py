from typing import Any

from pyldb.api.client import BaseAPIClient


class YearsAPI(BaseAPIClient):
    """
    Client for the LDB /years endpoints.

    Provides access to available data years in the Local Data Bank (LDB), including
    listing all years, retrieving year details, and accessing years API metadata.
    """

    def list_years(self) -> list[int]:
        """
        List all available years for which data is present in the LDB API.

        Maps to: GET /years

        Returns:
            List of available years as integers.
        """
        return self.fetch_single_result("years", results_key="years")

    def get_year(
        self,
        year_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata for a specific year.

        Maps to: GET /years/{id}

        Args:
            year_id: Year identifier (integer, e.g. 2020).
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.

        Returns:
            Dictionary with year metadata.
        """
        params = extra_query if extra_query else None
        return self.fetch_single_result(f"years/{year_id}", params=params)

    def get_years_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /years endpoint.

        Maps to: GET /years/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self.fetch_single_result("years/metadata")

    async def alist_years(self) -> list[int]:
        """
        Asynchronously list all available years for which data is present in the LDB API.

        Maps to: GET /years

        Returns:
            List of available years as integers.
        """
        return await self.afetch_single_result("years", results_key="years")

    async def aget_year(
        self,
        year_id: int,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of get_year.
        """
        params = extra_query if extra_query else None
        return await self.afetch_single_result(f"years/{year_id}", params=params)

    async def aget_years_metadata(self) -> dict[str, Any]:
        """
        Async version of get_years_metadata.
        """
        return await self.afetch_single_result("years/metadata")
