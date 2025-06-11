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
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all measure units, optionally sorted.

        Maps to: GET /measures

        Args:
            sort: Optional sorting order, e.g. 'Id', '-Id', 'Name', '-Name'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of measure unit metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort

        if all_pages:
            return self.fetch_all_results(
                "measures",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("measures", params=params, extra_query=extra_query)
            return resp.get("results", [])

    def get_measure_info(
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
        return self._make_request(f"measures/{measure_id}", extra_query=extra_query)

    def get_measures_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /measures endpoint.

        Maps to: GET /measures/metadata

        Args:
            extra_query: Additional query parameters, e.g., {'lang': 'en'}.

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self._make_request("measures/metadata", extra_query=extra_query)
