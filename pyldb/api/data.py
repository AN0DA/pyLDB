from typing import Any

import pandas as pd

from pyldb.api.client import BaseAPIClient


class DataAPI(BaseAPIClient):
    """
    Client for all LDB /data endpoints.

    Provides Pythonic, paginated, and DataFrame-ready access to all public
    data endpoints in the Local Data Bank (LDB) API. Supports flexible
    parameterization, pagination, and format options for robust data retrieval.

    Methods map directly to documented LDB endpoints under the /data namespace,
    enabling users to fetch statistical data by variable, unit, attribute, or locality,
    as well as check data availability for any of these entities.
    """

    def get_data_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata for the /data endpoint.

        Maps to: GET /data/metadata

        Args:
            extra_query: Additional query parameters, e.g., {'lang': 'en'}.

        Returns:
            dict: Metadata describing the /data resource, fields, and parameters.
        """
        return self._make_request("data/metadata", extra_query=extra_query)

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
    ) -> pd.DataFrame:
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

        Returns:
            pd.DataFrame: Flattened results with one row per value.
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

        if all_pages:
            results = self.fetch_all_results(
                f"data/by-variable/{variable_id}",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                f"data/by-variable/{variable_id}",
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

    def get_data_by_unit(
        self,
        unit_id: str,
        year: int | None = None,
        variables: list[str] | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> pd.DataFrame:
        """
        Retrieve statistical data for a specific administrative unit.

        Maps to: GET /data/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the administrative unit.
            year: Optional year filter.
            variables: Optional list of variable IDs to include.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            pd.DataFrame: Flattened results with one row per value.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if variables:
            params["var-id"] = variables
        if format:
            params["format"] = format

        if all_pages:
            results = self.fetch_all_results(
                f"data/by-unit/{unit_id}",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                f"data/by-unit/{unit_id}",
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

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
    ) -> pd.DataFrame:
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

        Returns:
            pd.DataFrame: Flattened results with one row per value.
        """
        params: dict[str, Any] = {}
        if year is not None:
            params["year"] = year
        if format:
            params["format"] = format

        endpoint = f"data/by-variable/{variable_id}/locality/{locality_id}"

        if all_pages:
            results = self.fetch_all_results(
                endpoint,
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                endpoint,
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

    def get_data_locality_by_unit(
        self,
        unit_id: str,
        variable_id: str | None = None,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> pd.DataFrame:
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

        Returns:
            pd.DataFrame: Flattened results with one row per value.
        """
        params: dict[str, Any] = {}
        if variable_id:
            params["var-id"] = variable_id
        if year:
            params["year"] = year
        if format:
            params["format"] = format

        endpoint = f"data/localities/by-unit/{unit_id}"

        if all_pages:
            results = self.fetch_all_results(
                endpoint,
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                endpoint,
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

    def get_data_by_attribute(
        self,
        attribute_id: str,
        year: int | None = None,
        unit_level: int | None = None,
        parent_id: str | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> pd.DataFrame:
        """
        Retrieve data for a specific attribute.

        Maps to: GET /data/by-attribute/{attr-id}

        Args:
            attribute_id: Identifier of the attribute.
            year: Optional year filter.
            unit_level: Optional administrative unit aggregation level.
            parent_id: Optional parent administrative unit ID.
            format: Response format, e.g., 'json' or 'csv'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            pd.DataFrame: Flattened results with one row per value.
        """
        params: dict[str, Any] = {}
        if year:
            params["year"] = year
        if unit_level:
            params["unit-level"] = unit_level
        if parent_id:
            params["parent-id"] = parent_id
        if format:
            params["format"] = format

        endpoint = f"data/by-attribute/{attribute_id}"

        if all_pages:
            results = self.fetch_all_results(
                endpoint,
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                endpoint,
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

    def get_data_by_attribute_locality(
        self,
        attribute_id: str,
        locality_id: str,
        year: int | None = None,
        format: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> pd.DataFrame:
        """
        Retrieve data for a specific attribute within a locality.

        Maps to: GET /data/by-attribute/{attr-id}/locality/{locality-id}

        Args:
            attribute_id: Identifier of the attribute.
            locality_id: Identifier of the locality.
            year: Optional year filter.
            format: Response format, e.g., 'json' or 'csv'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            pd.DataFrame: Flattened results with one row per value.
        """
        params: dict[str, Any] = {}
        if year:
            params["year"] = year
        if format:
            params["format"] = format

        endpoint = f"data/by-attribute/{attribute_id}/locality/{locality_id}"

        if all_pages:
            results = self.fetch_all_results(
                endpoint,
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            response = self._make_request(
                endpoint,
                params=params,
                extra_query=extra_query,
            )
            results = response.get("results", [])

        if not results:
            raise ValueError("No data found for the specified criteria")
        return pd.json_normalize(results)

    def get_data_availability_by_variable(
        self,
        variable_id: str,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve data availability for a specific variable.

        Maps to: GET /data/availability/by-variable/{var-id}

        Args:
            variable_id: Identifier of the variable.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.

        Returns:
            dict: Availability information for the variable.
        """
        params: dict[str, Any] = {}
        if format:
            params["format"] = format

        endpoint = f"data/availability/by-variable/{variable_id}"
        return self._make_request(endpoint, params=params, extra_query=extra_query)

    def get_data_availability_by_unit(
        self,
        unit_id: str,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve data availability for a specific administrative unit.

        Maps to: GET /data/availability/by-unit/{unit-id}

        Args:
            unit_id: Identifier of the administrative unit.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.

        Returns:
            dict: Availability information for the unit.
        """
        params: dict[str, Any] = {}
        if format:
            params["format"] = format

        endpoint = f"data/availability/by-unit/{unit_id}"
        return self._make_request(endpoint, params=params, extra_query=extra_query)

    def get_data_availability_by_attribute(
        self,
        attribute_id: str,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve data availability for a specific attribute.

        Maps to: GET /data/availability/by-attribute/{attr-id}

        Args:
            attribute_id: Identifier of the attribute.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.

        Returns:
            dict: Availability information for the attribute.
        """
        params: dict[str, Any] = {}
        if format:
            params["format"] = format

        endpoint = f"data/availability/by-attribute/{attribute_id}"
        return self._make_request(endpoint, params=params, extra_query=extra_query)

    def get_data_availability_by_variable_locality(
        self,
        variable_id: str,
        locality_id: str,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve data availability for a variable in a specific locality.

        Maps to: GET /data/availability/by-variable/{var-id}/locality/{locality-id}

        Args:
            variable_id: Identifier of the variable.
            locality_id: Identifier of the locality.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.

        Returns:
            dict: Availability information for the variable and locality.
        """
        params: dict[str, Any] = {}
        if format:
            params["format"] = format

        endpoint = f"data/availability/by-variable/{variable_id}/locality/{locality_id}"
        return self._make_request(endpoint, params=params, extra_query=extra_query)

    def get_data_availability_by_attribute_locality(
        self,
        attribute_id: str,
        locality_id: str,
        format: str | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve data availability for an attribute in a specific locality.

        Maps to: GET /data/availability/by-attribute/{attr-id}/locality/{locality-id}

        Args:
            attribute_id: Identifier of the attribute.
            locality_id: Identifier of the locality.
            format: Response format, e.g., 'json' or 'csv'.
            extra_query: Additional query parameters.

        Returns:
            dict: Availability information for the attribute and locality.
        """
        params: dict[str, Any] = {}
        if format:
            params["format"] = format

        endpoint = f"data/availability/by-attribute/{attribute_id}/locality/{locality_id}"
        return self._make_request(endpoint, params=params, extra_query=extra_query)
