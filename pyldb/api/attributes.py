from typing import Any

from pyldb.api.client import BaseAPIClient


class AttributesAPI(BaseAPIClient):
    """
    Client for the LDB /attributes endpoints.

    Provides paginated, filterable access to attribute metadata, attribute details,
    and API metadata for attributes in the Local Data Bank (LDB).
    """

    def list_attributes(
        self,
        variable_id: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all attributes, optionally filtered by variable.

        Maps to: GET /attributes

        Args:
            variable_id: Optional variable ID to filter attributes.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of attribute metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if variable_id:
            params["variable-id"] = variable_id

        if all_pages:
            return self.fetch_all_results(
                "attributes",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            resp = self._make_request("attributes", params=params, extra_query=extra_query)
            return resp.get("results", [])

    def get_attribute_info(self, attribute_id: str) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific attribute.

        Maps to: GET /attributes/{id}

        Args:
            attribute_id: Attribute identifier.

        Returns:
            Dictionary with attribute metadata.
        """
        return self._make_request(f"attributes/{attribute_id}")

    def get_attributes_metadata(
        self,
        extra_query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /attributes endpoint.

        Maps to: GET /attributes/metadata

        Args:
            extra_query: Additional query parameters, e.g., {'lang': 'en'}.

        Returns:
            Dictionary with API metadata and versioning info.
        """
        return self._make_request("attributes/metadata", extra_query=extra_query)
