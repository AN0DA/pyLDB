from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.data import DataAPI
from pyldb.config import LDBConfig


@pytest.fixture
def data_api(dummy_config: LDBConfig) -> DataAPI:
    return DataAPI(dummy_config)


@responses.activate
def test_get_data_by_variable(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-variable/3643?lang=en"
    payload = {"results": [{"id": "A", "value": 123}]}
    responses.add(responses.GET, url, json=payload, status=200)
    response = data_api.get_data_by_variable(variable_id="3643", all_pages=False)
    assert isinstance(response, tuple)
    assert response[0][0]["id"] == "A"


@responses.activate
def test_get_data_by_unit(data_api: DataAPI, api_url: str) -> None:
    params = {"var-id": "3643", "lang": "en"}
    url = f"{api_url}/data/by-unit/999?{urlencode(params)}"
    payload = {"results": [{"id": "B", "value": 555}]}
    responses.add(responses.GET, url, json=payload, status=200)
    response = data_api.get_data_by_unit(unit_id="999", variable="3643")
    assert isinstance(response, tuple)
    assert response[0][0]["id"] == "B"
    request_url = responses.calls[0].request.url
    assert request_url is not None and "var-id=3643" in request_url


@responses.activate
def test_get_data_by_variable_locality(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-variable/7/locality/2?lang=en"
    payload = {"results": [{"id": "C", "value": 42}]}
    responses.add(responses.GET, url, json=payload, status=200)
    response = data_api.get_data_by_variable_locality(variable_id="7", locality_id="2", all_pages=False)
    assert isinstance(response, tuple)
    assert response[0][0]["id"] == "C"


@responses.activate
def test_get_data_locality_by_unit(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/localities/by-unit/44?lang=en"
    payload = {"results": [{"id": "D", "value": 10}]}
    responses.add(responses.GET, url, json=payload, status=200)
    response = data_api.get_data_by_unit_locality(unit_id="44", all_pages=False)
    assert isinstance(response, tuple)
    assert response[0][0]["id"] == "D"


@responses.activate
def test_get_data_metadata(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/metadata?lang=en"
    payload = {"info": "data metadata"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_metadata()
    assert result["info"] == "data metadata"
