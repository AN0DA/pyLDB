from typing import Any, cast

import pytest
import responses
from requests import PreparedRequest

from pyldb.api.client import BaseAPIClient
from pyldb.config import Language, LDBConfig


# Type for PreparedRequest with req_kwargs added by responses
class ResponsesPreparedRequest(PreparedRequest):
    req_kwargs: dict[str, Any]


@pytest.fixture
def base_client(dummy_config: LDBConfig) -> BaseAPIClient:
    """Fixture for BaseAPIClient."""
    return BaseAPIClient(dummy_config)


@pytest.fixture
def api_url() -> str:
    return "https://bdl.stat.gov.pl/api/v1"


def test_build_url(base_client: BaseAPIClient) -> None:
    assert base_client._build_url("data/xyz") == "https://bdl.stat.gov.pl/api/v1/data/xyz"
    assert base_client._build_url("/data/xyz/") == "https://bdl.stat.gov.pl/api/v1/data/xyz"


@responses.activate
def test_make_request_success(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/test"
    url = f"{api_url}/data/test"
    expected = {"results": [{"id": 1}, {"id": 2}, {"id": 3}]}
    responses.add(responses.GET, url + "?lang=en", json=expected, status=200)
    result = base_client._make_request(endpoint)
    assert result == expected


@responses.activate
def test_make_request_includes_language(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/lang"
    url = f"{api_url}/data/lang"
    responses.add(responses.GET, url + "?lang=en", json={"results": []}, status=200)
    base_client._make_request(endpoint)
    request_url = responses.calls[0].request.url
    assert request_url is not None and "lang=en" in request_url


@responses.activate
def test_make_request_with_params(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/params"
    url = f"{api_url}/data/params"
    full_url = url + "?foo=bar&lang=en"
    responses.add(responses.GET, full_url, json={"results": []}, status=200)
    base_client._make_request(endpoint, params={"foo": "bar"})
    request_url = responses.calls[0].request.url
    assert request_url is not None and "foo=bar" in request_url


@responses.activate
def test_make_request_http_error(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/fail"
    url = f"{api_url}/data/fail?lang=en"
    responses.add(responses.GET, url, json={"detail": "Not found"}, status=404)
    with pytest.raises(RuntimeError) as excinfo:
        base_client._make_request(endpoint)
    assert "HTTP error" in str(excinfo.value)


@responses.activate
def test_make_request_api_error_field(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/api_error"
    url = f"{api_url}/data/api_error?lang=en"
    responses.add(responses.GET, url, json={"error": "Oops"}, status=200)
    with pytest.raises(ValueError) as excinfo:
        base_client._make_request(endpoint)
    assert "API Error" in str(excinfo.value)


@responses.activate
def test_make_request_with_headers(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/headers"
    url = f"{api_url}/data/headers?lang=en"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    base_client._make_request(endpoint, headers={"X-Test-Header": "foo"})
    req_headers = responses.calls[0].request.headers
    assert req_headers["X-Test-Header"] == "foo"
    assert req_headers["X-ClientId"] == "dummy-api-key"


@responses.activate
def test_paginated_request_all_pages(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/paged"
    url = f"{api_url}/data/paged"
    # Page 0
    url0 = url + "?lang=en&page-size=2"
    url1 = url + "?lang=en&page-size=2&page=1"
    responses.add(
        responses.GET,
        url0,
        json={
            "results": [{"id": 1}, {"id": 2}],
            "totalRecords": 4,
            "links": {"next": url1},
        },
        status=200,
    )
    # Page 1 (last): links has navigation fields but no 'next'
    responses.add(
        responses.GET,
        url1,
        json={
            "results": [{"id": 3}, {"id": 4}],
            "totalRecords": 4,
            "links": {
                "first": url0,
                "prev": url0,
                "self": url1,
                "last": url1,
            },
        },
        status=200,
    )
    pages = list(base_client._paginated_request(endpoint, results_key="results", page_size=2, return_all=True))
    assert len(pages) == 2
    assert pages[0]["results"] == [{"id": 1}, {"id": 2}]
    assert pages[1]["results"] == [{"id": 3}, {"id": 4}]
    # Ensure the correct URLs were called
    assert responses.calls[0].request.url.startswith(url0)
    assert responses.calls[1].request.url.startswith(url1)


@responses.activate
def test_fetch_all_results(base_client: BaseAPIClient, api_url: str) -> None:
    endpoint = "data/paged"
    url = f"{api_url}/data/paged"
    url0 = url + "?lang=en&page-size=2"
    url1 = url + "?lang=en&page-size=2&page=1"
    responses.add(
        responses.GET,
        url0,
        json={
            "results": [{"id": 1}, {"id": 2}],
            "totalRecords": 3,
            "links": {"next": url1},
        },
        status=200,
    )
    responses.add(
        responses.GET,
        url1,
        json={
            "results": [{"id": 3}],
            "totalRecords": 3,
            "links": {
                "first": url0,
                "prev": url0,
                "self": url1,
                "last": url1,
            },
        },
        status=200,
    )
    results = base_client.fetch_all_results(endpoint, results_key="results", page_size=2)
    assert results == [{"id": 1}, {"id": 2}, {"id": 3}]
    # Ensure the correct URLs were called
    assert responses.calls[0].request.url.startswith(url0)
    assert responses.calls[1].request.url.startswith(url1)


def test_client_with_proxy() -> None:
    config = LDBConfig(api_key="dummy-api-key", proxy_url="http://proxy.example.com:8080")
    client = BaseAPIClient(config)
    assert client.session.proxies["http"] == "http://proxy.example.com:8080"
    assert client.session.proxies["https"] == "http://proxy.example.com:8080"


def test_client_with_authenticated_proxy() -> None:
    config = LDBConfig(
        api_key="dummy-api-key", proxy_url="http://proxy.example.com:8080", proxy_username="user", proxy_password="pass"
    )
    client = BaseAPIClient(config)
    expected_proxy = "http://user:pass@proxy.example.com:8080"
    assert client.session.proxies["http"] == expected_proxy
    assert client.session.proxies["https"] == expected_proxy


@responses.activate
def test_make_request_with_proxy(base_client: BaseAPIClient, api_url: str) -> None:
    # Configure client with proxy
    config = LDBConfig(
        api_key="dummy-api-key",
        proxy_url="http://proxy.example.com:8080",
        language=Language.EN,
    )
    client = BaseAPIClient(config)

    endpoint = "data/proxy"
    url = f"{api_url}/data/proxy?lang=en"
    responses.add(responses.GET, url, json={"results": []}, status=200)

    client._make_request(endpoint)
    request = cast(ResponsesPreparedRequest, responses.calls[0].request)
    # Verify proxy settings in the request kwargs
    assert request.req_kwargs["proxies"]["http"] == "http://proxy.example.com:8080"
    assert request.req_kwargs["proxies"]["https"] == "http://proxy.example.com:8080"
