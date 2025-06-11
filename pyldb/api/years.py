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
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all available data years.

        Maps to: GET /years

        Args:
            sort: Optional sorting order, e.g. 'Id', '-Id'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of year metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort

        if all_pages:
            return self.fetch_all_results(
                "years",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("years", params=params, extra_query=extra_query)
            return resp.get("results", [])

    def get_year_info(
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
        return self._make_request(f"years/{year_id}", extra_query=extra_query)

    def get_years_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /years endpoint.

        Maps to: GET /years/metadata

        Args:
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self._make_request("years/metadata", extra_query=extra_query)
