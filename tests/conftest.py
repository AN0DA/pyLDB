from typing import Any
from urllib.parse import urlencode

import pytest
import responses

from pyldb.config import LDBConfig


@pytest.fixture
def dummy_config() -> LDBConfig:
    """Provide a dummy LDBConfig for testing."""
    return LDBConfig(api_key="dummy-api-key", language="en", use_cache=False, cache_expire_after=100)


@pytest.fixture
def api_url() -> str:
    return "https://bdl.stat.gov.pl/api/v1"


def paginated_mock(
    base_url: str, data: list[dict[str, Any]], page_size: int = 100, extra_params: dict[str, Any] | None = None
) -> None:
    """
    Mocks two paginated responses using the `responses` library:
    - First page returns the supplied data and a links.next to the next page
    - Second page returns an empty result list and a links object with navigation fields but no next
    Accepts extra_params dict for additional query params (e.g. lang).
    """
    params = extra_params.copy() if extra_params else {}
    params["page-size"] = str(page_size)
    params["lang"] = "en"

    # First page: no 'page' param
    url_0 = f"{base_url}?{urlencode(params)}"
    params_next = params.copy()
    params_next["page"] = "1"
    url_1 = f"{base_url}?{urlencode(params_next)}"
    responses.add(
        responses.GET,
        url_0,
        json={
            "results": data,
            "totalRecords": len(data) + 1,
            "links": {"next": url_1},
        },
        status=200,
    )
    # Second page: with 'page=1', links has navigation fields but no 'next'
    responses.add(
        responses.GET,
        url_1,
        json={
            "results": [],
            "links": {
                "first": url_0,
                "prev": url_0,
                "self": url_1,
                "last": url_1,
            },
        },
        status=200,
    )
