from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.units import UnitsAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def units_api(dummy_config: LDBConfig) -> UnitsAPI:
    return UnitsAPI(dummy_config)


@responses.activate
def test_list_units(units_api: UnitsAPI, api_url: str) -> None:
    url = f"{api_url}/units"
    paginated_mock(url, [{"id": "PL", "name": "Poland"}])
    result = units_api.list_units()
    assert isinstance(result, list)
    assert result[0]["name"] == "Poland"


@responses.activate
def test_list_units_with_filters(units_api: UnitsAPI, api_url: str) -> None:
    params = {
        "level": "2",
        "parent-id": "PL",
        "name": "Warsaw",
        "sort": "name",
        "lang": "en",
        "page-size": "100",
    }
    url = f"{api_url}/units?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also add page 1 for completeness
    params["page"] = "1"
    url1 = f"{api_url}/units?{urlencode(params)}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    units_api.list_units(level=2, parent_id="PL", name="Warsaw", sort="name")
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "level=2" in called_url
    assert "parent-id=PL" in called_url
    assert "name=Warsaw" in called_url
    assert "sort=name" in called_url


@responses.activate
def test_get_unit_info(units_api: UnitsAPI, api_url: str) -> None:
    url = f"{api_url}/units/PL?lang=en"
    payload = {"id": "PL", "name": "Poland"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = units_api.get_unit_info(unit_id="PL")
    assert result["id"] == "PL"
    assert result["name"] == "Poland"


@responses.activate
def test_get_units_metadata(units_api: UnitsAPI, api_url: str) -> None:
    url = f"{api_url}/units/metadata?lang=en"
    payload = {"info": "Units API"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = units_api.get_units_metadata()
    assert result["info"] == "Units API"
