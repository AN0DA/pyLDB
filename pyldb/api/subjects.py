from typing import Any

from pyldb.api.client import BaseAPIClient


class SubjectsAPI(BaseAPIClient):
    """
    Client for the LDB /subjects endpoints.

    Provides access to the subject hierarchy (thematic areas) in the Local Data Bank (LDB),
    including subject browsing, detail retrieval, and metadata.
    """

    def list_subjects(
        self,
        parent_id: str | None = None,
        sort: str | None = None,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
        all_pages: bool = True,
    ) -> list[dict[str, Any]]:
        """
        List all subjects, optionally filtered by parent subject.

        Maps to: GET /subjects

        Args:
            parent_id: Optional parent subject ID. If not specified, returns all top-level subjects.
            sort: Optional sorting order, e.g. 'id', '-id', 'name', '-name'.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.
            all_pages: If True, fetch all pages; otherwise, fetch only the first.

        Returns:
            List of subject metadata dictionaries.
        """
        params: dict[str, Any] = {}
        if parent_id:
            params["parent-id"] = parent_id
        if sort:
            params["sort"] = sort

        if all_pages:
            return self.fetch_all_results(
                "subjects",
                params=params,
                extra_query=extra_query,
                page_size=page_size,
                max_pages=max_pages,
                results_key="results",
            )
        else:
            return self.fetch_single_result("subjects", results_key="results", params=params, extra_query=extra_query)

    def get_subject(
        self,
        subject_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve metadata for a specific subject.

        Maps to: GET /subjects/{id}

        Args:
            subject_id: Subject identifier.

        Returns:
            Dictionary with subject metadata.
        """
        return self.fetch_single_result(f"subjects/{subject_id}")

    def search_subjects(
        self,
        name: str,
        page_size: int = 100,
        max_pages: int | None = None,
        extra_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for subjects by name.

        Maps to: GET /subjects/search

        Args:
            name: Subject name to search for.
            page_size: Number of results per page.
            max_pages: Maximum number of pages to fetch (None for all).
            extra_query: Additional query parameters.

        Returns:
            List of subject metadata dictionaries matching the search.
        """
        params = {"name": name}
        return self.fetch_all_results(
            "subjects/search",
            params=params,
            extra_query=extra_query,
            page_size=page_size,
            max_pages=max_pages,
            results_key="results",
        )

    def get_subjects_metadata(self) -> dict[str, Any]:
        """
        Retrieve general metadata and version information for the /subjects endpoint.

        Maps to: GET /subjects/metadata

        Returns:
            Dictionary with endpoint metadata and versioning info.
        """
        return self.fetch_single_result("subjects/metadata")
