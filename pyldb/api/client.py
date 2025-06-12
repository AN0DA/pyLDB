from collections.abc import Iterator
from typing import Any

from requests import HTTPError, Response, Session
from requests_cache import CachedSession

from pyldb.config import LDB_API_BASE_URL, LDBConfig


class BaseAPIClient:
    """Base client for LDB API interactions.

    This client handles common functionality for all API endpoints including:
    - Authentication
    - Request caching
    - Proxy configuration
    - Response handling
    - Pagination

    The client supports HTTP/HTTPS proxy configuration through the LDBConfig settings.
    Proxy authentication is supported by providing proxy_username and proxy_password.
    """

    def __init__(self, config: LDBConfig, extra_headers: dict[str, str] | None = None):
        """
        Initialize base API client.

        Args:
            config: LDB configuration.
            extra_headers: Optional extra headers (e.g. Accept-Language).
        """
        self.config = config
        self.session: CachedSession | Session

        # Initialize session with caching if enabled
        if config.use_cache:
            self.session = CachedSession(
                expire_after=config.cache_expire_after,
                backend="memory",
            )
        else:
            self.session = Session()

        if config.proxy_url:
            proxies = {
                "http": config.proxy_url,
                "https": config.proxy_url,
            }
            if config.proxy_username and config.proxy_password:
                from urllib.parse import urlparse, urlunparse

                parsed = urlparse(config.proxy_url)
                auth = f"{config.proxy_username}:{config.proxy_password}"
                new_netloc = f"{auth}@{parsed.netloc}"
                auth_proxy_url = urlunparse(parsed._replace(netloc=new_netloc))
                proxies = {
                    "http": auth_proxy_url,
                    "https": auth_proxy_url,
                }
            self.session.proxies.update(proxies)

        # Set default headers
        self.session.headers.update(
            {
                "X-ClientId": config.api_key,  # type: ignore[dict-item]
                "Content-Type": "application/json",
            }
        )
        if extra_headers:
            self.session.headers.update(extra_headers)

    def _build_url(self, endpoint: str) -> str:
        """Build full API URL."""
        endpoint = endpoint.strip("/")
        return f"{LDB_API_BASE_URL}/{endpoint}"

    def _handle_response(self, response: Response) -> dict[str, Any]:
        """Process and validate API response."""
        try:
            response.raise_for_status()
        except HTTPError as exc:
            try:
                error_detail = response.json()
            except Exception:
                error_detail = response.text
            raise RuntimeError(f"HTTP error {response.status_code}: {error_detail}") from exc

        data = response.json()
        if "error" in data:
            raise ValueError(f"API Error: {data['error']}")
        return data

    def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Make a single HTTP request to LDB API.

        Args:
            endpoint: API endpoint
            method: HTTP method (default: GET)
            params: Query parameters (e.g., year, lang, page, page-size, etc.)
            extra_query: Additional query parameters to merge in.
            headers: Optional request headers.

        Returns:
            API response as dictionary.

        Raises:
            requests.exceptions.RequestException: If request fails
            ValueError: If response contains error
        """
        url = self._build_url(endpoint)
        query = params.copy() if params else {}
        if extra_query:
            query.update(extra_query)

        # Always include language setting
        query.setdefault("lang", self.config.language)

        # Merge headers if provided
        req_headers: dict[str, str] = {k: str(v) for k, v in self.session.headers.items()}
        if headers:
            req_headers.update(headers)

        response = self.session.request(method, url, params=query, headers=req_headers)
        return self._handle_response(response)

    def _paginated_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        results_key: str = "results",
        page_size: int = 100,
        max_pages: int | None = None,
        return_all: bool = True,
    ) -> Iterator[dict[str, Any]]:
        """
        Fetch all paginated results from an endpoint.

        Args:
            endpoint: API endpoint
            method: HTTP method
            params: Query parameters
            extra_query: Additional query parameters
            headers: Request headers
            results_key: Key to extract results array from response
            page_size: Number of items per page
            max_pages: Max pages to fetch (None = all)
            return_all: If True, yields all pages; if False, yield first page only.

        Yields:
            Each page's result dictionary.
        """
        query = params.copy() if params else {}
        if extra_query:
            query.update(extra_query)
        query.setdefault("lang", self.config.language)
        query["page-size"] = page_size

        page = 0
        fetched = 0

        while True:
            query["page"] = page
            resp = self._make_request(endpoint, method=method, params=query, headers=headers)
            if results_key not in resp or not resp[results_key]:
                break
            yield resp

            fetched += 1
            if not return_all or (max_pages and fetched >= max_pages):
                break
            if resp.get("totalRecords") is not None:
                # Stop if we've got all records
                total = resp["totalRecords"]
                if (page + 1) * page_size >= total:
                    break
            page += 1

    def fetch_all_results(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        results_key: str = "results",
        page_size: int = 100,
        max_pages: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Convenience method to fetch and combine all paginated results.

        Returns:
            List of all results across pages.
        """
        all_results = []
        for page in self._paginated_request(
            endpoint,
            method=method,
            params=params,
            extra_query=extra_query,
            headers=headers,
            results_key=results_key,
            page_size=page_size,
            max_pages=max_pages,
            return_all=True,
        ):
            all_results.extend(page.get(results_key, []))
        return all_results
