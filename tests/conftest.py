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
    - page=0 returns the supplied data
    - page=1 returns an empty result list
    Accepts extra_params dict for additional query params (e.g. lang).
    """
    params = extra_params.copy() if extra_params else {}
    params["page-size"] = str(page_size)
    params["lang"] = "en"

    # Page 0
    params["page"] = "0"
    url_0 = f"{base_url}?{urlencode(params)}"
    responses.add(responses.GET, url_0, json={"results": data, "totalRecords": len(data) + 1}, status=200)
    # Page 1
    params["page"] = "1"
    url_1 = f"{base_url}?{urlencode(params)}"
    responses.add(responses.GET, url_1, json={"results": []}, status=200)
