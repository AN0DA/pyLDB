from collections.abc import Iterator
from typing import Any

from pyldb.api.utils.rate_limiter import AsyncRateLimiter, PersistentQuotaCache, RateLimiter

import httpx
from requests import HTTPError, Response, Session
from requests_cache import CachedSession
from tqdm import tqdm

from pyldb.config import DEFAULT_QUOTAS, LDB_API_BASE_URL, LDBConfig


class BaseAPIClient:
    """Base client for LDB API interactions.

    This client handles common functionality for all API endpoints including:
    - Authentication
    - Request caching
    - Proxy configuration
    - Response handling
    - Pagination with optional progress bars

    The client supports HTTP/HTTPS proxy configuration through the LDBConfig settings.
    Proxy authentication is supported by providing proxy_username and proxy_password.
    
    Progress bars can be displayed during paginated requests using the show_progress
    parameter in fetch_all_results() and afetch_all_results() methods. Progress bars
    show the number of pages fetched, current item count, and estimated total when
    available from the API response.
    """

    _global_sync_limiter = None
    _global_async_limiter = None
    _quota_cache = None

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

        # Determine quotas
        quotas = getattr(config, "quotas", None)
        if quotas is None:
            # Use default quotas based on registration
            is_registered = bool(getattr(config, "api_key", None))
            quotas = {k: v[1] if is_registered else v[0] for k, v in DEFAULT_QUOTAS.items()}
        # Quota cache
        if BaseAPIClient._quota_cache is None:
            BaseAPIClient._quota_cache = PersistentQuotaCache(getattr(config, "quota_cache_enabled", True))
        # Set global limiters if not set
        if BaseAPIClient._global_sync_limiter is None:
            BaseAPIClient._global_sync_limiter = RateLimiter(quotas, is_registered, BaseAPIClient._quota_cache)
        if BaseAPIClient._global_async_limiter is None:
            BaseAPIClient._global_async_limiter = AsyncRateLimiter(quotas, is_registered, BaseAPIClient._quota_cache)
        self._sync_limiter = BaseAPIClient._global_sync_limiter
        self._async_limiter = BaseAPIClient._global_async_limiter

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
        self._sync_limiter.acquire()
        url = self._build_url(endpoint)
        query = params.copy() if params else {}
        if extra_query:
            query.update(extra_query)

        # Always include language setting
        lang = self.config.language.value if hasattr(self.config.language, "value") else self.config.language
        query.setdefault("lang", lang)

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
        lang = self.config.language.value if hasattr(self.config.language, "value") else self.config.language
        query.setdefault("lang", lang)
        query["page-size"] = page_size

        fetched = 0
        next_url = None
        first = True

        while True:
            if first:
                # First request: use endpoint and params
                resp = self._make_request(endpoint, method=method, params=query, headers=headers)
                first = False
            else:
                # Next requests: use the next_url directly
                if not next_url:
                    break
                response = self.session.request(method, next_url, headers=self.session.headers)
                resp = self._handle_response(response)

            if results_key not in resp or not resp[results_key]:
                break
            yield resp

            fetched += 1
            if not return_all or (max_pages and fetched >= max_pages):
                break
            # Get next page URL from response; stop if 'next' is not present in links
            links = resp.get("links", {})
            next_url = links.get("next")
            if "next" not in links:
                break

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
        return_metadata: bool = False,
        show_progress: bool = True,
    ) -> list[dict[str, Any]] | tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        Convenience method to fetch and combine all paginated results.

        Args:
            endpoint: API endpoint
            method: HTTP method (default: GET)
            params: Query parameters (e.g., year, lang, page, page-size, etc.)
            extra_query: Additional query parameters to merge in.
            headers: Optional request headers.
            results_key: Key to extract results array from response
            page_size: Number of items per page
            max_pages: Max pages to fetch (None = all)
            return_metadata: If True, also return metadata dict (see docstring).
            show_progress: If True, show a progress bar during fetching.

        Returns:
            List of all results across pages, or (results, metadata) tuple if return_metadata is True.
        """
        all_results = []
        metadata: dict[str, Any] = {}
        first_page = True
        
        # Create progress bar if requested
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(
                desc=f"Fetching {endpoint.split('/')[-1]}",
                unit="pages",
                leave=True
            )
        
        try:
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
                if first_page and return_metadata:
                    # Collect metadata from the first page
                    metadata = {k: v for k, v in page.items() if k not in {results_key, "page", "pageSize", "links"}}
                    # Try to get total count for progress bar
                    if show_progress and progress_bar is not None and "totalCount" in page:
                        total_pages = (page["totalCount"] + page_size - 1) // page_size
                        progress_bar.total = total_pages
                    first_page = False
                
                all_results.extend(page.get(results_key, []))
                
                if show_progress and progress_bar is not None:
                    progress_bar.update(1)
                    progress_bar.set_postfix({
                        "items": len(all_results),
                        "current_page": len(all_results) // page_size + (1 if len(all_results) % page_size else 0)
                    })
        finally:
            if show_progress and progress_bar is not None:
                progress_bar.close()
        
        if return_metadata:
            return all_results, metadata
        return all_results

    def fetch_single_result(
        self,
        endpoint: str,
        results_key: str | None = None,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_metadata: bool = False,
    ) -> dict[str, Any] | list[dict[str, Any]] | tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        Fetch a single (non-paginated) result from an endpoint.

        Args:
            endpoint: API endpoint
            results_key: Key to extract results from response (default: None, returns full response)
            method: HTTP method (default: GET)
            params: Query parameters
            extra_query: Additional query parameters
            headers: Optional request headers
            return_metadata: If True, also return metadata dict (see docstring).

        Returns:
            Dictionary or list of dictionaries with result data, or (results, metadata) tuple if return_metadata is True and results_key is not None.
        """
        response = self._make_request(
            endpoint=endpoint,
            method=method,
            params=params,
            extra_query=extra_query,
            headers=headers,
        )

        if results_key is not None:
            if isinstance(response, dict) and results_key in response:
                results = response[results_key]
                if return_metadata:
                    metadata = {
                        k: v for k, v in response.items() if k not in {results_key, "page", "pageSize", "links"}
                    }
                    return results, metadata
                return results
            else:
                raise ValueError(f"Response does not contain key '{results_key}'")
        return response

    async def _amake_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Async version of _make_request using httpx.AsyncClient.
        """
        await self._async_limiter.acquire()
        url = self._build_url(endpoint)
        query = params.copy() if params else {}
        if extra_query:
            query.update(extra_query)
        lang = self.config.language.value if hasattr(self.config.language, "value") else self.config.language
        query.setdefault("lang", lang)
        req_headers: dict[str, str] = {k: str(v) for k, v in self.session.headers.items()}
        if headers:
            req_headers.update(headers)
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=query, headers=req_headers)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            try:
                error_detail = response.json()
            except Exception:
                error_detail = response.text
            raise RuntimeError(f"HTTP error {response.status_code}: {error_detail}") from exc
        data = response.json()
        if "error" in data:
            raise ValueError(f"API Error: {data['error']}")
        return data

    async def _apaginated_request(
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
    ):
        """
        Async version of _paginated_request using httpx.AsyncClient.
        Yields each page's result dictionary.
        """
        query = params.copy() if params else {}
        if extra_query:
            query.update(extra_query)
        lang = self.config.language.value if hasattr(self.config.language, "value") else self.config.language
        query.setdefault("lang", lang)
        query["page-size"] = page_size
        fetched = 0
        next_url = None
        first = True
        async with httpx.AsyncClient() as client:
            while True:
                if first:
                    resp = await self._amake_request(endpoint, method=method, params=query, headers=headers)
                    first = False
                else:
                    if not next_url:
                        break
                    response = await client.request(method, next_url, headers=self.session.headers)
                    try:
                        response.raise_for_status()
                    except httpx.HTTPStatusError as exc:
                        try:
                            error_detail = response.json()
                        except Exception:
                            error_detail = response.text
                        raise RuntimeError(f"HTTP error {response.status_code}: {error_detail}") from exc
                    resp = response.json()
                if results_key not in resp or not resp[results_key]:
                    break
                yield resp
                fetched += 1
                if not return_all or (max_pages and fetched >= max_pages):
                    break
                links = resp.get("links", {})
                next_url = links.get("next")
                if "next" not in links:
                    break

    async def afetch_all_results(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        results_key: str = "results",
        page_size: int = 100,
        max_pages: int | None = None,
        return_metadata: bool = False,
        show_progress: bool = True,
    ) -> list[dict[str, Any]] | tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        Async version of fetch_all_results.

        Args:
            endpoint: API endpoint
            method: HTTP method (default: GET)
            params: Query parameters (e.g., year, lang, page, page-size, etc.)
            extra_query: Additional query parameters to merge in.
            headers: Optional request headers.
            results_key: Key to extract results array from response
            page_size: Number of items per page
            max_pages: Max pages to fetch (None = all)
            return_metadata: If True, also return metadata dict (see docstring).
            show_progress: If True, show a progress bar during fetching.

        Returns:
            List of all results across pages, or (results, metadata) tuple if return_metadata is True.
        """
        all_results = []
        metadata: dict[str, Any] = {}
        first_page = True
        
        # Create progress bar if requested
        progress_bar = None
        if show_progress:
            progress_bar = tqdm(
                desc=f"Fetching {endpoint.split('/')[-1]} (async)",
                unit="pages",
                leave=True
            )
        
        try:
            async for page in self._apaginated_request(
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
                if first_page and return_metadata:
                    metadata = {k: v for k, v in page.items() if k not in {results_key, "page", "pageSize", "links"}}
                    # Try to get total count for progress bar
                    if show_progress and progress_bar is not None and "totalCount" in page:
                        total_pages = (page["totalCount"] + page_size - 1) // page_size
                        progress_bar.total = total_pages
                    first_page = False
                
                all_results.extend(page.get(results_key, []))
                
                if show_progress and progress_bar is not None:
                    progress_bar.update(1)
                    progress_bar.set_postfix({
                        "items": len(all_results),
                        "current_page": len(all_results) // page_size + (1 if len(all_results) % page_size else 0)
                    })
        finally:
            if show_progress and progress_bar is not None:
                progress_bar.close()
        
        if return_metadata:
            return all_results, metadata
        return all_results

    async def afetch_single_result(
        self,
        endpoint: str,
        results_key: str | None = None,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        extra_query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        return_metadata: bool = False,
    ) -> dict[str, Any] | list[dict[str, Any]] | tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        Async version of fetch_single_result.
        """
        response = await self._amake_request(
            endpoint=endpoint,
            method=method,
            params=params,
            extra_query=extra_query,
            headers=headers,
        )
        if results_key is not None:
            if isinstance(response, dict) and results_key in response:
                results = response[results_key]
                if return_metadata:
                    metadata = {
                        k: v for k, v in response.items() if k not in {results_key, "page", "pageSize", "links"}
                    }
                    return results, metadata
                return results
            else:
                raise ValueError(f"Response does not contain key '{results_key}'")
        return response
