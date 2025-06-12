from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.measures import MeasuresAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def measures_api(dummy_config: LDBConfig) -> MeasuresAPI:
    return MeasuresAPI(dummy_config)


@responses.activate
def test_list_measures(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures"
    paginated_mock(url, [{"id": 1, "name": "kg"}])
    result = measures_api.list_measures()
    assert isinstance(result, list)
    assert result[0]["name"] == "kg"


@responses.activate
def test_list_measures_with_sort(measures_api: MeasuresAPI, api_url: str) -> None:
    params = {"sort": "Name", "lang": "en", "page": "0", "page-size": "100"}
    url = f"{api_url}/measures?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also add page 1 for pagination completeness (even if not needed for empty result)
    params["page"] = "1"
    url1 = f"{api_url}/measures?{urlencode(params)}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    measures_api.list_measures(sort="Name")
    request_url = responses.calls[0].request.url
    assert request_url is not None and "sort=Name" in request_url


@responses.activate
def test_get_measure_info(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures/11?lang=en"
    payload = {"id": 11, "name": "percent"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = measures_api.get_measure_info(measure_id=11)
    assert result["id"] == 11
    assert result["name"] == "percent"


@responses.activate
def test_get_measures_metadata(measures_api: MeasuresAPI, api_url: str) -> None:
    url = f"{api_url}/measures/metadata?lang=en"
    payload = {"version": "1.0"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = measures_api.get_measures_metadata()
    assert result["version"] == "1.0"
