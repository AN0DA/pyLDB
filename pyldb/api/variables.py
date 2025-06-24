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
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "variables",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("variables", results_key="results", params=params)

    def get_variable(
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
        params = extra_query if extra_query else None
        return self.fetch_single_result(f"variables/{variable_id}", params=params)

    def search_variables(
        self,
        name: str | None = None,
        category_id: str | None = None,
        aggregate_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Search for variables by name and optional filters.

        Maps to: GET /variables/search

        Args:
            name: Substring to search in variable name.
            category_id: Optional category ID to filter variables.
            aggregate_id: Optional aggregate ID to filter variables.
            sort: Optional sorting order.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of variable metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if category_id:
            params["category-id"] = category_id
        if aggregate_id:
            params["aggregate-id"] = aggregate_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "variables/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("variables/search", results_key="results", params=params)

    def get_variables_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /variables endpoint.

        Maps to: GET /variables/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self.fetch_single_result("variables/metadata")

    async def alist_variables(
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
        Async version of list_variables.
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
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "variables",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("variables", results_key="results", params=params)

    async def aget_variable(
        self,
        variable_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of get_variable.
        """
        params = extra_query if extra_query else None
        return await self.afetch_single_result(f"variables/{variable_id}", params=params)

    async def asearch_variables(
        self,
        name: str | None = None,
        category_id: str | None = None,
        aggregate_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Async version of search_variables.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if category_id:
            params["category-id"] = category_id
        if aggregate_id:
            params["aggregate-id"] = aggregate_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "variables/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("variables/search", results_key="results", params=params)

    async def aget_variables_metadata(self) -> dict[str, Any]:
        """
        Async version of get_variables_metadata.
        """
        return await self.afetch_single_result("variables/metadata")
