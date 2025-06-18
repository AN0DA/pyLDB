from typing import Any

from pyldb.api.client import BaseAPIClient


class AttributesAPI(BaseAPIClient):
    """
    Client for the LDB /attributes endpoints.

    Provides paginated, filterable access to attribute metadata, attribute details,
    and API metadata for attributes in the Local Data Bank (LDB).
    """

    def list_attributes(self) -> list[dict[str, Any]]:
        """
        List all attributes, optionally filtered by variable.

        Maps to: GET /attributes

        Returns:
            List of attribute metadata dictionaries.
        """

        return self.fetch_single_result("attributes", results_key="results")

    def get_attribute(self, attribute_id: str) -> dict[str, Any]:
        """
        Retrieve metadata details for a specific attribute.

        Maps to: GET /attributes/{id}

        Args:
            attribute_id: Attribute identifier.

        Returns:
            Dictionary with attribute metadata.
        """
        return self.fetch_single_result(f"attributes/{attribute_id}")

    def get_attributes_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /attributes endpoint.

        Maps to: GET /attributes/metadata

        Returns:
            Dictionary with API metadata and versioning info.
        """
        return self.fetch_single_result("attributes/metadata")
