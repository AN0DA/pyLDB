
import pytest
import responses

from pyldb.api.years import YearsAPI
from pyldb.config import LDBConfig


@pytest.fixture
def years_api(dummy_config: LDBConfig) -> YearsAPI:
    return YearsAPI(dummy_config)


@responses.activate
def test_list_years(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years"
    payload = {"results": [{"id": 2020, "name": "2020"}, {"id": 2021, "name": "2021"}]}
    responses.add(responses.GET, url, json=payload, status=200)
    result = years_api.list_years()
    assert isinstance(result, list)
    assert result[0]["id"] == 2020


@responses.activate
def test_get_year(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years/2021?lang=en"
    payload = {"id": 2021, "name": "2021"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = years_api.get_year(year_id=2021)
    assert result["id"] == 2021


@responses.activate
def test_get_years_metadata(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years/metadata?lang=en"
    payload = {"info": "Years API"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = years_api.get_years_metadata()
    assert result["info"] == "Years API"
