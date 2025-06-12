from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.levels import LevelsAPI
from pyldb.config import LDBConfig


@pytest.fixture
def levels_api(dummy_config: LDBConfig) -> LevelsAPI:
    return LevelsAPI(dummy_config)


@responses.activate
def test_list_levels(levels_api: LevelsAPI, api_url: str) -> None:
    url = f"{api_url}/levels?lang=en"
    payload = {"results": [{"id": 1, "name": "Country"}, {"id": 2, "name": "Region"}]}
    responses.add(responses.GET, url, json=payload, status=200)
    # Also register page 1 as empty for pagination to finish (if paginated)
    url1 = f"{api_url}/levels?lang=en&page=1&page-size=100"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    result = levels_api.list_levels()
    assert isinstance(result, list)
    assert any(r["name"] == "Country" for r in result)
    called_url = responses.calls[0].request.url
    assert called_url is not None and "lang=en" in called_url


@responses.activate
def test_list_levels_with_sort(levels_api: LevelsAPI, api_url: str) -> None:
    # The first request will be just with sort and lang
    params = {"sort": "Name", "lang": "en"}
    url = f"{api_url}/levels?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also register page 1 as empty (if paginated)
    url1 = f"{api_url}/levels?{urlencode({**params, 'page': '1', 'page-size': '100'})}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    levels_api.list_levels(sort="Name")
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "sort=Name" in called_url
    assert "lang=en" in called_url


@responses.activate
def test_get_level_info(levels_api: LevelsAPI, api_url: str) -> None:
    url = f"{api_url}/levels/3?lang=en"
    payload = {"id": 3, "name": "Powiat"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = levels_api.get_level_info(level_id=3)
    assert result["id"] == 3
    assert result["name"] == "Powiat"


@responses.activate
def test_get_levels_metadata(levels_api: LevelsAPI, api_url: str) -> None:
    url = f"{api_url}/levels/metadata?lang=en"
    payload = {"version": "1.0"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = levels_api.get_levels_metadata()
    assert result["version"] == "1.0"
