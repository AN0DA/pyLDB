from urllib.parse import urlencode

import pandas as pd
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
    df = data_api.get_data_by_variable(variable_id="3643", all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "A"


@responses.activate
def test_get_data_by_variable_filters(data_api: DataAPI, api_url: str) -> None:
    params = {"year": "2021", "unit-level": "2", "parent-id": "PL", "lang": "en"}
    url = f"{api_url}/data/by-variable/111?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    with pytest.raises(ValueError, match="No data found for the specified criteria"):
        data_api.get_data_by_variable(variable_id="111", year=2021, unit_level=2, parent_id="PL", all_pages=False)
    req_url = responses.calls[0].request.url
    assert req_url is not None
    for k, v in params.items():
        assert f"{k}={v}" in req_url


@responses.activate
def test_get_data_by_unit(data_api: DataAPI, api_url: str) -> None:
    params = {"var-id": "3643", "lang": "en"}
    url = f"{api_url}/data/by-unit/999?{urlencode(params)}"
    payload = {"results": [{"id": "B", "value": 555}]}
    responses.add(responses.GET, url, json=payload, status=200)
    df = data_api.get_data_by_unit(unit_id="999", variables=["3643"], all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "B"
    request_url = responses.calls[0].request.url
    assert request_url is not None and "var-id=3643" in request_url


@responses.activate
def test_get_data_by_variable_locality(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-variable/7/locality/2?lang=en"
    payload = {"results": [{"id": "C", "value": 42}]}
    responses.add(responses.GET, url, json=payload, status=200)
    df = data_api.get_data_by_variable_locality(variable_id="7", locality_id="2", all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "C"


@responses.activate
def test_get_data_locality_by_unit(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/localities/by-unit/44?lang=en"
    payload = {"results": [{"id": "D", "value": 10}]}
    responses.add(responses.GET, url, json=payload, status=200)
    df = data_api.get_data_locality_by_unit(unit_id="44", all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "D"


@responses.activate
def test_get_data_by_attribute(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-attribute/5?lang=en"
    payload = {"results": [{"id": "E", "value": 9}]}
    responses.add(responses.GET, url, json=payload, status=200)
    df = data_api.get_data_by_attribute(attribute_id="5", all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "E"


@responses.activate
def test_get_data_by_attribute_locality(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-attribute/6/locality/3?lang=en"
    payload = {"results": [{"id": "F", "value": 8}]}
    responses.add(responses.GET, url, json=payload, status=200)
    df = data_api.get_data_by_attribute_locality(attribute_id="6", locality_id="3", all_pages=False)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["id"] == "F"


@responses.activate
def test_get_data_availability_by_variable(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/availability/by-variable/7?lang=en"
    payload = {"availability": True}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_availability_by_variable(variable_id="7")
    assert result["availability"] is True


@responses.activate
def test_get_data_availability_by_unit(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/availability/by-unit/8?lang=en"
    payload = {"availability": False}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_availability_by_unit(unit_id="8")
    assert result["availability"] is False


@responses.activate
def test_get_data_availability_by_attribute(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/availability/by-attribute/9?lang=en"
    payload = {"availability": True}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_availability_by_attribute(attribute_id="9")
    assert result["availability"] is True


@responses.activate
def test_get_data_availability_by_variable_locality(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/availability/by-variable/7/locality/2?lang=en"
    payload = {"availability": True}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_availability_by_variable_locality(variable_id="7", locality_id="2")
    assert result["availability"] is True


@responses.activate
def test_get_data_availability_by_attribute_locality(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/availability/by-attribute/9/locality/3?lang=en"
    payload = {"availability": False}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_availability_by_attribute_locality(attribute_id="9", locality_id="3")
    assert result["availability"] is False


@responses.activate
def test_get_data_metadata(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/metadata?lang=en"
    payload = {"info": "data metadata"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = data_api.get_data_metadata()
    assert result["info"] == "data metadata"


@responses.activate
def test_no_data_found_raises(data_api: DataAPI, api_url: str) -> None:
    url = f"{api_url}/data/by-variable/0?lang=en"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    with pytest.raises(ValueError):
        data_api.get_data_by_variable(variable_id="0", all_pages=False)
