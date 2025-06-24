from typing import Any

from pyldb.api.client import BaseAPIClient


class UnitsAPI(BaseAPIClient):
    """
    Client for the LDB /units endpoints.

    Provides access to administrative unit metadata in the Local Data Bank (LDB),
    including listing units (with filtering by level, parent, etc.), retrieving unit details,
    and accessing general units API metadata.
    """

    def list_units(
        self,
        level: int | None = None,
        parent_id: str | None = None,
        name: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all administrative units, optionally filtered by level, parent, or name.

        Maps to: GET /units

        Args:
            level: Optional administrative level (integer).
            parent_id: Optional parent unit ID.
            name: Optional substring to search in unit name.
            sort: Optional sorting order, e.g. 'id', '-id', 'name', '-name'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of unit metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if name:
            params["name"] = name
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "units",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_all_results("units", params=params)

    def get_unit(
        self,
        unit_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific administrative unit.

        Maps to: GET /units/{id}

        Args:
            unit_id: Administrative unit identifier.
            extra_query: Additional query parameters.

        Returns:
            Dictionary with unit metadata.
        """
        params = extra_query if extra_query else None
        return self.fetch_single_result(f"units/{unit_id}", params=params)

    def search_units(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Search for administrative units by name and optional filters.

        Maps to: GET /units/search

        Args:
            name: Substring to search in unit name.
            level: Optional administrative level (integer).
            parent_id: Optional parent unit ID.
            sort: Optional sorting order.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of unit metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "units/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("units/search", results_key="results", params=params)

    def list_localities(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all statistical localities, optionally filtered by name, level, or parent.

        Maps to: GET /units/localities

        Args:
            name: Substring to search in locality name.
            level: Optional administrative level (integer).
            parent_id: Optional parent unit ID.
            sort: Optional sorting order.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of locality metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "units/localities",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("units/localities", results_key="results", params=params)

    def get_locality(
        self,
        locality_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific statistical locality.

        Maps to: GET /units/localities/{id}

        Args:
            locality_id: Locality identifier.
            extra_query: Additional query parameters.

        Returns:
            Dictionary with locality metadata.
        """
        params = extra_query if extra_query else None
        return self.fetch_single_result(f"units/localities/{locality_id}", params=params)

    def search_localities(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Search for statistical localities by name and optional filters.

        Maps to: GET /units/localities/search

        Args:
            name: Substring to search in locality name.
            level: Optional administrative level (integer).
            parent_id: Optional parent unit ID.
            sort: Optional sorting order.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of locality metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return self.fetch_all_results(
                "units/localities/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("units/localities/search", results_key="results", params=params)

    def get_units_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /units endpoint.

        Maps to: GET /units/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self.fetch_single_result("units/metadata")

    async def alist_units(
        self,
        level: int | None = None,
        parent_id: str | None = None,
        name: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Async version of list_units.
        """
        params: dict[str, Any] = {}
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if name:
            params["name"] = name
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "units",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("units", results_key="results", params=params)

    async def aget_unit(
        self,
        unit_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of get_unit.
        """
        params = extra_query if extra_query else None
        return await self.afetch_single_result(f"units/{unit_id}", params=params)

    async def asearch_units(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Async version of search_units.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "units/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("units/search", results_key="results", params=params)

    async def alist_localities(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Async version of list_localities.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "units/localities",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("units/localities", results_key="results", params=params)

    async def aget_locality(
        self,
        locality_id: str,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of get_locality.
        """
        params = extra_query if extra_query else None
        return await self.afetch_single_result(f"units/localities/{locality_id}", params=params)

    async def asearch_localities(
        self,
        name: str | None = None,
        level: int | None = None,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Async version of search_localities.
        """
        params: dict[str, Any] = {}
        if name:
            params["name"] = name
        if level is not None:
            params["level"] = level
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort
        if extra_query:
            params.update(extra_query)
        if all_pages:
            return await self.afetch_all_results(
                "units/localities/search",
                params=params,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return await self.afetch_single_result("units/localities/search", results_key="results", params=params)

    async def aget_units_metadata(self) -> dict[str, Any]:
        """
        Async version of get_units_metadata.
        """
        return await self.afetch_single_result("units/metadata")
