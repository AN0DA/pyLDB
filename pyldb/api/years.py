from typing import Any

from pyldb.api.client import BaseAPIClient


class YearsAPI(BaseAPIClient):
    """
    Client for the LDB /years endpoints.

    Provides access to available data years in the Local Data Bank (LDB), including
    listing all years, retrieving year details, and accessing years API metadata.
    """

    def list_years(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        List all available data years.

        Maps to: GET /years

        Args:
            sort: Optional sorting order, e.g. 'Id', '-Id'.
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.

        Returns:
            List of year metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        return self.fetch_all_results("years", params=params)

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

    async def alist_years(
        self,
        sort: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Async version of list_years.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        return await self.afetch_all_results("years", params=params)

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
