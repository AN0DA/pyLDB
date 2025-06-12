import pytest
import responses

from pyldb.api.version import VersionAPI
from pyldb.config import LDBConfig


@pytest.fixture
def version_api(dummy_config: LDBConfig) -> VersionAPI:
    return VersionAPI(dummy_config)


@responses.activate
def test_get_version(version_api: VersionAPI, api_url: str) -> None:
    url = f"{api_url}/version?lang=en"
    payload = {"version": "1.2.3", "build": "2025-06-11"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = version_api.get_version()
    assert result["version"] == "1.2.3"
    assert result["build"] == "2025-06-11"


@responses.activate
def test_get_version_with_extra_query(version_api: VersionAPI, api_url: str) -> None:
    url = f"{api_url}/version?lang=pl"
    payload = {"version": "2.0"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = version_api.get_version(extra_query={"lang": "pl"})
    assert result["version"] == "2.0"
    request_url = responses.calls[0].request.url
    assert request_url is not None and request_url.endswith("lang=pl")
