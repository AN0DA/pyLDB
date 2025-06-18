from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.measures import MeasuresAPI
from pyldb.config import LDBConfig


@pytest.fixture
def measures_api(dummy_config: LDBConfig) -> MeasuresAPI:
    return MeasuresAPI(dummy_config)


@responses.activate
def test_list_measures(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures"
    payload = {"results": [{"id": 1, "name": "kg"}]}
    responses.add(responses.GET, url, json=payload, status=200)
    result = measures_api.list_measures()
    assert isinstance(result, list)
    assert result[0]["name"] == "kg"


@responses.activate
def test_list_measures_with_sort(measures_api: MeasuresAPI, api_url: str) -> None:
    params = {"sort": "Name", "lang": "en"}
    url = f"{api_url}/measures?{urlencode(params)}"
    payload = {"results": [{"id": 1, "name": "kg"}]}
    responses.add(responses.GET, url, json=payload, status=200)
    measures_api.list_measures(sort="Name")
    request_url = responses.calls[0].request.url
    assert request_url is not None and "sort=Name" in request_url


@responses.activate
def test_get_measure(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures/11?lang=en"
    payload = {"id": 11, "name": "percent"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = measures_api.get_measure(measure_id=11)
    assert result["id"] == 11
    assert result["name"] == "percent"


@responses.activate
def test_get_measures_metadata(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures/metadata?lang=en"
    payload = {"version": "1.0"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = measures_api.get_measures_metadata()
    assert result["version"] == "1.0"
