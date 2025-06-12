from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.years import YearsAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def years_api(dummy_config: LDBConfig) -> YearsAPI:
    return YearsAPI(dummy_config)


@responses.activate
def test_list_years(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years"
    paginated_mock(url, [{"id": 2020, "name": "2020"}, {"id": 2021, "name": "2021"}])
    result = years_api.list_years()
    assert isinstance(result, list)
    assert result[0]["id"] == 2020


@responses.activate
def test_list_years_with_sort(years_api: YearsAPI, api_url: str) -> None:
    params = {"sort": "Id", "lang": "en", "page-size": "100"}
    url = f"{api_url}/years?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also add page 1 for pagination completeness
    params["page"] = "1"
    url1 = f"{api_url}/years?{urlencode(params)}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    years_api.list_years(sort="Id")
    called_url = responses.calls[0].request.url
    assert called_url is not None and "sort=Id" in called_url


@responses.activate
def test_get_year_info(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years/2021?lang=en"
    payload = {"id": 2021, "name": "2021"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = years_api.get_year_info(year_id=2021)
    assert result["id"] == 2021


@responses.activate
def test_get_years_metadata(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years/metadata?lang=en"
    payload = {"info": "Years API"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = years_api.get_years_metadata()
    assert result["info"] == "Years API"
