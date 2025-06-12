from typing import Any

from pyldb.api.client import BaseAPIClient


class VariablesAPI(BaseAPIClient):
    """
    Client for the LDB /variables endpoints.

    Provides access to variable metadata in the Local Data Bank (LDB),
    including listing variables (with filtering by category or aggregate), retrieving
    variable details, and accessing general variables API metadata.
    """

    def list_variables(
        self,
        category_id: str | None = None,
        aggregate_id: str | None = None,
        name: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all variables, optionally filtered by category, aggregate, or name.

        Maps to: GET /variables

        Args:
            category_id: Optional category ID to filter variables.
            aggregate_id: Optional aggregate ID to filter variables.
            name: Optional substring to search in variable name.
            sort: Optional sorting order, e.g. 'id', '-id', 'name', '-name'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of variable metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if category_id:
            params["category-id"] = category_id
        if aggregate_id:
            params["aggregate-id"] = aggregate_id
        if name:
            params["name"] = name
        if sort:
            params["sort"] = sort

        if all_pages:
            return self.fetch_all_results(
                "variables",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("variables", params=params, extra_query=extra_query)
            return resp.get("results", [])

    def get_variable_info(
        self,
        variable_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific variable.

        Maps to: GET /variables/{id}

        Args:
            variable_id: Variable identifier.
            extra_query: Additional query parameters.

        Returns:
            Dictionary with variable metadata.
        """
        return self._make_request(f"variables/{variable_id}", extra_query=extra_query)

    def get_variables_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /variables endpoint.

        Maps to: GET /variables/metadata

        Args:
            extra_query: Additional query parameters, e.g. {'lang': 'en'}.

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self._make_request("variables/metadata", extra_query=extra_query)
