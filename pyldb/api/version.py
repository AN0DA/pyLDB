from typing import Any

from pyldb.api.client import BaseAPIClient


class VersionAPI(BaseAPIClient):
    """
    Client for the LDB /version endpoint.

    Provides access to version and build information for the Local Data Bank (LDB) API.
    """

    def get_version(self) -> dict[str, Any]:
        """
        Retrieve API version and build information.

        Maps to: GET /version

        Returns:
            Dictionary with version and build information.
        """
        return self.fetch_single_result("version")

    async def aget_version(self) -> dict[str, Any]:
        """
        Async version of get_version.
        """
        return await self.afetch_single_result("version")
