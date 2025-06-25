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


@responses.activate
def test_list_years_extra_query(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years?foo=bar&lang=en&page-size=100"
    responses.add(responses.GET, url, json={"results": [{"id": 2020}]}, status=200)
    result = years_api.list_years(extra_query={"foo": "bar"})
    assert result[0]["id"] == 2020


@responses.activate
def test_get_year_extra_query(years_api: YearsAPI, api_url: str) -> None:
    url = f"{api_url}/years/2022?foo=bar&lang=en"
    responses.add(responses.GET, url, json={"id": 2022}, status=200)
    result = years_api.get_year(year_id=2022, extra_query={"foo": "bar"})
    assert result["id"] == 2022


class DummyException(Exception):
    pass


@responses.activate
def test_list_years_error(years_api: YearsAPI) -> None:
    def raise_exc(*a: object, **k: object) -> None:
        raise DummyException("fail")

    years_api.fetch_all_results = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        years_api.list_years()


@responses.activate
def test_get_year_error(years_api: YearsAPI) -> None:
    def raise_exc(*a: object, **k: object) -> None:
        raise DummyException("fail")

    years_api.fetch_single_result = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        years_api.get_year(2021)


@responses.activate
def test_get_years_metadata_error(years_api: YearsAPI) -> None:
    def raise_exc(*a: object, **k: object) -> None:
        raise DummyException("fail")

    years_api.fetch_single_result = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        years_api.get_years_metadata()
