# type: ignore

from typing import Any
from unittest.mock import AsyncMock, patch
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


@responses.activate
def test_get_data_metadata_error(data_api: DataAPI) -> None:
    # Simulate error in fetch_single_result
    class DummyException(Exception):
        pass

    def raise_exc(*a: Any, **k: Any) -> None:
        raise DummyException("fail")

    data_api.fetch_single_result = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        data_api.get_data_metadata()


@responses.activate
def test_get_data_by_variable_all_branches(data_api: DataAPI, api_url: str) -> None:
    # all_pages True, return_metadata True
    url = f"{api_url}/data/by-variable/3643?lang=en"
    payload = {"results": [{"id": "A", "value": 123}]}
    responses.add(responses.GET, url, json=payload, status=200)

    def mock_fetch_all_results(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "A", "value": 123}], {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results  # type: ignore[assignment]
    result = data_api.get_data_by_variable(variable_id="3643", all_pages=True, return_metadata=True)
    assert result == ([{"id": "A", "value": 123}], {"meta": 1})

    # all_pages True, return_metadata False
    def mock_fetch_all_results_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "B"}]

    data_api.fetch_all_results = mock_fetch_all_results_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_variable(variable_id="3643", all_pages=True, return_metadata=False)
    assert result_no_meta == [{"id": "B"}]

    # all_pages False, return_metadata False
    def mock_fetch_single_result(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "C"}]

    data_api.fetch_single_result = mock_fetch_single_result  # type: ignore[assignment]
    result_single = data_api.get_data_by_variable(variable_id="3643", all_pages=False, return_metadata=False)
    assert result_single == [{"id": "C"}]


@responses.activate
def test_get_data_by_unit_all_branches(data_api: DataAPI, api_url: str) -> None:
    # return_metadata True
    def mock_fetch_single_result_with_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "A"}], {"meta": 1})

    data_api.fetch_single_result = mock_fetch_single_result_with_meta  # type: ignore[assignment]
    result = data_api.get_data_by_unit(unit_id="1", variable="v", return_metadata=True)
    assert result == ([{"id": "A"}], {"meta": 1})

    # return_metadata False
    def mock_fetch_single_result_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "B"}]

    data_api.fetch_single_result = mock_fetch_single_result_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_unit(unit_id="1", variable="v", return_metadata=False)
    assert result_no_meta == [{"id": "B"}]


@responses.activate
def test_get_data_by_variable_locality_all_branches(data_api: DataAPI, api_url: str) -> None:
    # all_pages True, return_metadata True
    def mock_fetch_all_results_with_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "A"}], {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results_with_meta  # type: ignore[assignment]
    result = data_api.get_data_by_variable_locality(
        variable_id="v", locality_id="l", all_pages=True, return_metadata=True
    )
    assert result == ([{"id": "A"}], {"meta": 1})

    # all_pages True, return_metadata False
    def mock_fetch_all_results_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "B"}]

    data_api.fetch_all_results = mock_fetch_all_results_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_variable_locality(
        variable_id="v", locality_id="l", all_pages=True, return_metadata=False
    )
    assert result_no_meta == [{"id": "B"}]

    # all_pages False, return_metadata True
    def mock_fetch_single_result_with_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "C"}], {"meta": 2})

    data_api.fetch_single_result = mock_fetch_single_result_with_meta  # type: ignore[assignment]
    result_single_meta = data_api.get_data_by_variable_locality(
        variable_id="v", locality_id="l", all_pages=False, return_metadata=True
    )
    assert result_single_meta == ([{"id": "C"}], {"meta": 2})

    # all_pages False, return_metadata False
    def mock_fetch_single_result_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "D"}]

    data_api.fetch_single_result = mock_fetch_single_result_no_meta  # type: ignore[assignment]
    result_single_no_meta = data_api.get_data_by_variable_locality(
        variable_id="v", locality_id="l", all_pages=False, return_metadata=False
    )
    assert result_single_no_meta == [{"id": "D"}]


@responses.activate
def test_get_data_by_unit_locality_all_branches(data_api: DataAPI, api_url: str) -> None:
    # all_pages True, return_metadata True
    def mock_fetch_all_results_with_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "A"}], {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results_with_meta  # type: ignore[assignment]
    result = data_api.get_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)
    assert result == ([{"id": "A"}], {"meta": 1})

    # all_pages True, return_metadata False
    def mock_fetch_all_results_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "B"}]

    data_api.fetch_all_results = mock_fetch_all_results_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=False)
    assert result_no_meta == [{"id": "B"}]

    # all_pages False, return_metadata True
    def mock_fetch_single_result_with_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        return ([{"id": "C"}], {"meta": 2})

    data_api.fetch_single_result = mock_fetch_single_result_with_meta  # type: ignore[assignment]
    result_single_meta = data_api.get_data_by_unit_locality(unit_id="u", all_pages=False, return_metadata=True)
    assert result_single_meta == ([{"id": "C"}], {"meta": 2})

    # all_pages False, return_metadata False
    def mock_fetch_single_result_no_meta(*a: Any, **k: Any) -> list[dict[str, Any]]:
        return [{"id": "D"}]

    data_api.fetch_single_result = mock_fetch_single_result_no_meta  # type: ignore[assignment]
    result_single_no_meta = data_api.get_data_by_unit_locality(unit_id="u", all_pages=False, return_metadata=False)
    assert result_single_no_meta == [{"id": "D"}]


@responses.activate
def test_get_data_by_variable_params(data_api: DataAPI, api_url: str) -> None:
    # Test all optional params: year, unit_level, parent_id, format, extra_query
    def mock_fetch_all_results(
        endpoint: str, params: dict[str, Any], **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (params, {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results  # type: ignore[assignment]
    result, meta = data_api.get_data_by_variable(
        variable_id="v",
        year=2020,
        unit_level=2,
        parent_id="pid",
        format="csv",
        extra_query={"foo": "bar"},
        all_pages=True,
        return_metadata=True,
    )
    # result is the params dictionary returned by the mock
    assert result["year"] == 2020
    assert result["unit-level"] == 2
    assert result["parent-id"] == "pid"
    assert result["format"] == "csv"
    assert result["foo"] == "bar"


@responses.activate
def test_get_data_by_unit_params(data_api: DataAPI, api_url: str) -> None:
    def mock_fetch_single_result(
        endpoint: str, results_key: str, params: dict[str, Any], **kwargs: Any
    ) -> dict[str, Any]:
        return params

    data_api.fetch_single_result = mock_fetch_single_result  # type: ignore[assignment]
    result = data_api.get_data_by_unit(
        unit_id="u",
        variable="v",
        year=2021,
        format="csv",
        extra_query={"bar": "baz"},
        return_metadata=True,
    )
    # result is the params dictionary returned by the mock
    assert result["year"] == 2021
    assert result["format"] == "csv"
    assert result["bar"] == "baz"


@responses.activate
def test_get_data_by_variable_locality_params(data_api: DataAPI, api_url: str) -> None:
    def mock_fetch_all_results(
        endpoint: str, params: dict[str, Any], **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (params, {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results  # type: ignore[assignment]
    result, meta = data_api.get_data_by_variable_locality(
        variable_id="v",
        locality_id="l",
        year=2022,
        format="csv",
        extra_query={"baz": "qux"},
        all_pages=True,
        return_metadata=True,
    )
    # result is the params dictionary returned by the mock
    assert result["year"] == 2022
    assert result["format"] == "csv"
    assert result["baz"] == "qux"


@responses.activate
def test_get_data_by_unit_locality_params(data_api: DataAPI, api_url: str) -> None:
    def mock_fetch_all_results(
        endpoint: str, params: dict[str, Any], **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (params, {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results  # type: ignore[assignment]
    result, meta = data_api.get_data_by_unit_locality(
        unit_id="u",
        variable_id="v",
        year=2023,
        format="csv",
        extra_query={"qux": "quux"},
        all_pages=True,
        return_metadata=True,
    )
    # result is the params dictionary returned by the mock
    assert result["year"] == 2023
    assert result["format"] == "csv"
    assert result["qux"] == "quux"


@responses.activate
def test_get_data_by_variable_edge_cases(data_api: DataAPI, api_url: str) -> None:
    # Empty results
    def mock_fetch_all_results_empty(*a: Any, **k: Any) -> tuple[list[Any], dict[str, Any]]:
        return ([], {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results_empty  # type: ignore[assignment]
    result = data_api.get_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)
    assert result == ([], {"meta": 1})

    # Missing metadata
    def mock_fetch_all_results_no_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], None]:
        return ([{"id": 1}], None)

    data_api.fetch_all_results = mock_fetch_all_results_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)
    # Check each element of the tuple separately to avoid type issues
    assert result_no_meta[0] == [{"id": 1}]
    assert result_no_meta[1] is None


@responses.activate
def test_get_data_by_unit_locality_edge_cases(data_api: DataAPI, api_url: str) -> None:
    # Empty results
    def mock_fetch_all_results_empty(*a: Any, **k: Any) -> tuple[list[Any], dict[str, Any]]:
        return ([], {"meta": 1})

    data_api.fetch_all_results = mock_fetch_all_results_empty  # type: ignore[assignment]
    result = data_api.get_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)
    assert result == ([], {"meta": 1})

    # Missing metadata
    def mock_fetch_all_results_no_meta(*a: Any, **k: Any) -> tuple[list[dict[str, Any]], None]:
        return ([{"id": 1}], None)

    data_api.fetch_all_results = mock_fetch_all_results_no_meta  # type: ignore[assignment]
    result_no_meta = data_api.get_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)
    # Check each element of the tuple separately to avoid type issues
    assert result_no_meta[0] == [{"id": 1}]
    assert result_no_meta[1] is None


class DummyException(Exception):
    pass


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_metadata_error(afetch_single_result: AsyncMock, data_api: DataAPI) -> None:
    afetch_single_result.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await data_api.aget_data_metadata()


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_error(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await data_api.aget_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_unit_error(afetch_single_result: AsyncMock, data_api: DataAPI) -> None:
    afetch_single_result.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await data_api.aget_data_by_unit(unit_id="u", variable="v", return_metadata=True)


@responses.activate
def test_get_data_by_variable_error(data_api: DataAPI) -> None:
    def raise_exc(*a: Any, **k: Any) -> None:
        raise DummyException("fail")

    data_api.fetch_all_results = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        data_api.get_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)


@responses.activate
def test_get_data_by_unit_error(data_api: DataAPI) -> None:
    def raise_exc(*a: Any, **k: Any) -> None:
        raise DummyException("fail")

    data_api.fetch_single_result = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        data_api.get_data_by_unit(unit_id="u", variable="v", return_metadata=True)


@responses.activate
def test_get_data_by_variable_locality_error(data_api: DataAPI) -> None:
    def raise_exc(*a: Any, **k: Any) -> None:
        raise DummyException("fail")

    data_api.fetch_all_results = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        data_api.get_data_by_variable_locality(variable_id="v", locality_id="l", all_pages=True, return_metadata=True)


@responses.activate
def test_get_data_by_unit_locality_error(data_api: DataAPI) -> None:
    def raise_exc(*a: Any, **k: Any) -> None:
        raise DummyException("fail")

    data_api.fetch_all_results = raise_exc  # type: ignore[assignment]
    with pytest.raises(DummyException):
        data_api.get_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_locality_error(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await data_api.aget_data_by_variable_locality(
            variable_id="v", locality_id="l", all_pages=True, return_metadata=True
        )


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_unit_locality_error(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await data_api.aget_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)


@responses.activate
def test_get_data_by_variable_pagination(data_api: DataAPI) -> None:
    # Test max_pages and page_size are passed through
    def fetch_all_results(
        endpoint: str, params: dict[str, Any], page_size: int, max_pages: int, **kwargs: Any
    ) -> tuple[int, int]:
        return page_size, max_pages

    data_api.fetch_all_results = fetch_all_results  # type: ignore[assignment]
    result = data_api.get_data_by_variable(variable_id="v", all_pages=True, page_size=55, max_pages=3)
    # result is a tuple (page_size, max_pages)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == 55  # page_size
    assert result[1] == 3  # max_pages


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_pagination(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.return_value = (55, 3)
    result = await data_api.aget_data_by_variable(variable_id="v", all_pages=True, page_size=55, max_pages=3)
    # result is a tuple (page_size, max_pages)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == 55  # page_size
    assert result[1] == 3  # max_pages
