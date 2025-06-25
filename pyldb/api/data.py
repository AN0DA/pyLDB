from typing import Any, Literal, overload

from pyldb.api.client import BaseAPIClient


class DataAPI(BaseAPIClient):
    """
    Client for all LDB /data endpoints.

    Provides Pythonic, paginated, and DataFrame-ready access to all public
    data endpoints in the Local Data Bank (LDB) API. Supports flexible
    parameterization, pagination, and format options for robust data retrieval.

    Methods map directly to documented LDB endpoints under the /data namespace,
    enabling users to fetch statistical data by variable, unit, and locality.
    """

    @overload
    def get_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    def get_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    def get_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Retrieve statistical data for a specific variable.

        Maps to: GET /data/by-variable/{var-id}

        Args:
            variable_id: Identifier of the variable.
            year: Optional year filter.
            unit_level: Optional administrative unit aggregation level.
            parent_id: Optional parent administrative unit ID.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict)
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if unit_level is not None:
            params["unit-level"] = unit_level
        if parent_id is not None:
            params["parent-id"] = parent_id
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-variable/{variable_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,
                )
            else:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,
                )
        else:
            if return_metadata:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,
                )
            else:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,
                )
        return result

    @overload
    def get_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    def get_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    def get_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Retrieve statistical data for a specific administrative unit.

        Maps to: GET /data/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the administrative unit.
            variable: Variable ID to get results.
            year: Optional year filter.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict)
        """
        params: dict[str, Any] = {"var-id": variable}
        if year is not None:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-unit/{unit_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if return_metadata:
            result = self.fetch_single_result(
                endpoint,
                results_key="results",
                params=params,
                return_metadata=True,
            )
        else:
            result = self.fetch_single_result(
                endpoint,
                results_key="results",
                params=params,
                return_metadata=False,
            )
        return result

    @overload
    def get_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    def get_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    def get_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Retrieve data for a variable within a specific locality.

        Maps to: GET /data/by-variable/{var-id}/locality/{locality-id}

        Args:
            variable_id: Identifier of the variable.
            locality_id: Identifier of the locality.
            year: Optional year filter.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict)
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-variable/{variable_id}/locality/{locality_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,
                )
            else:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,
                )
        else:
            if return_metadata:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,
                )
            else:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,
                )
        return result

    @overload
    def get_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    def get_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    def get_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Retrieve data for a single statistical locality by unit.

        Maps to: GET /data/localities/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the statistical locality.
            variable_id: Optional variable ID to filter.
            year: Optional year filter.
            format: Response format, e.g., 'json' or 'csv'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict)
        """
        params: dict[str, Any] = {}
        if variable_id:
            params["var-id"] = variable_id
        if year:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/localities/by-unit/{unit_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,
                )
            else:
                result = self.fetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,
                )
        else:
            if return_metadata:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,
                )
            else:
                result = self.fetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,
                )
        return result

    def get_data_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata for the /data endpoint.

        Maps to: GET /data/metadata

        Returns:
            dict: Metadata describing the /data resource, fields, and parameters.
        """
        return self.fetch_single_result("data/metadata")

    # ASYNC VERSIONS
    @overload
    async def aget_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    async def aget_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    async def aget_data_by_variable(
        self,
        variable_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Asynchronously retrieve statistical data for a specific variable.

        Maps to: GET /data/by-variable/{var-id}

        Args:
            variable_id: Identifier of the variable.
            year: Optional year filter.
            unit_level: Optional administrative unit aggregation level.
            parent_id: Optional parent administrative unit ID.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict) if return_metadata is True, else just the list of results.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if unit_level is not None:
            params["unit-level"] = unit_level
        if parent_id is not None:
            params["parent-id"] = parent_id
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-variable/{variable_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,
                )
            else:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,
                )
        else:
            if return_metadata:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,
                )
            else:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,
                )
        return result

    @overload
    async def aget_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    async def aget_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    async def aget_data_by_unit(
        self,
        unit_id: str,
        variable: str,
        year: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Asynchronously retrieve statistical data for a specific administrative unit.

        Maps to: GET /data/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the administrative unit.
            variable: Variable ID to get results.
            year: Optional year filter.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict) if return_metadata is True, else just the list of results.
        """
        params: dict[str, Any] = {"var-id": variable}
        if year is not None:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-unit/{unit_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if return_metadata:
            result = await self.afetch_single_result(
                endpoint,
                results_key="results",
                params=params,
                return_metadata=True,
            )
        else:
            result = await self.afetch_single_result(
                endpoint,
                results_key="results",
                params=params,
                return_metadata=False,
            )
        return result

    @overload
    async def aget_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    async def aget_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    async def aget_data_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        year: int | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Asynchronously retrieve data for a variable within a specific locality.

        Maps to: GET /data/by-variable/{var-id}/locality/{locality-id}

        Args:
            variable_id: Identifier of the variable.
            locality_id: Identifier of the locality.
            year: Optional year filter.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict) if return_metadata is True, else just the list of results.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/by-variable/{variable_id}/locality/{locality_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,
                )
            else:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,
                )
        else:
            if return_metadata:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,
                )
            else:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,
                )
        return result

    @overload
    async def aget_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[True] = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]: ...

    @overload
    async def aget_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: Literal[False] = False,
    ) -> list[dict[str, Any]]: ...

    async def aget_data_by_unit_locality(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
        return_metadata: bool = True,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]:
        """
        Asynchronously retrieve data for a single statistical locality by unit.

        Maps to: GET /data/localities/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the statistical locality.
            variable_id: Optional variable ID to filter.
            year: Optional year filter.
            format: Response format, e.g., 'json' or 'csv'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.
            return_metadata: If True, include metadata in the response.

        Returns:
            tuple: (List of results, metadata dict) if return_metadata is True, else just the list of results.
        """
        params: dict[str, Any] = {}
        if variable_id:
            params["var-id"] = variable_id
        if year:
            params["year"] = year
        if format:
            params["format"] = format
        if extra_query:
            params.update(extra_query)
        endpoint = f"data/localities/by-unit/{unit_id}"

        result: tuple[list[dict[str, Any]], dict[str, Any]] | list[dict[str, Any]]
        if all_pages:
            if return_metadata:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=True,  # Explicit Literal[True]
                )
            else:
                result = await self.afetch_all_results(
                    endpoint,
                    params=params,
                    page_size=page_size,
                    max_pages=max_pages,
                    results_key="results",
                    return_metadata=False,  # Explicit Literal[False]
                )
        else:
            if return_metadata:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=True,  # Explicit Literal[True]
                )
            else:
                result = await self.afetch_single_result(
                    endpoint,
                    results_key="results",
                    params=params,
                    return_metadata=False,  # Explicit Literal[False]
                )

        return result

    async def aget_data_metadata(self) -> dict[str, Any]:
        """
        Asynchronously retrieve general metadata for the /data endpoint.

        Maps to: GET /data/metadata

        Returns:
            dict: Metadata describing the /data resource, fields, and parameters.
        """
        return await self.afetch_single_result("data/metadata")
