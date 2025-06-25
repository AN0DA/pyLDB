from typing import Any

from pyldb.api.client import BaseAPIClient


class VersionAPI(BaseAPIClient):
    """
    Client for the LDB /version endpoint.

    Provides access to version and build information for the Local Data Bank (LDB) API.
    """

    def get_version(self) -> dict[str, Any]:
        """
        Retrieve the API version and build information.

        Maps to: GET /version

        Returns:
            Dictionary with version and build metadata.
        """
        return self.fetch_single_result("version")

    async def aget_version(self) -> dict[str, Any]:
        """
        Asynchronously retrieve the API version and build information.

        Maps to: GET /version

        Returns:
            Dictionary with version and build metadata.
        """
        return await self.afetch_single_result("version")
