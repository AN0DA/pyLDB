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
