# type: ignore

from unittest.mock import AsyncMock, patch

import pytest

from pyldb.api.data import DataAPI
from pyldb.config import LDBConfig


@pytest.fixture
def data_api(dummy_config: LDBConfig) -> DataAPI:
    return DataAPI(dummy_config)


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_variable_all_branches(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, data_api: DataAPI
) -> None:
    # all_pages=True, return_metadata=True
    afetch_all_results.return_value = ([{"id": 1}], {"meta": 1})
    result = await data_api.aget_data_by_variable("v", all_pages=True, return_metadata=True)
    assert result == ([{"id": 1}], {"meta": 1})
    # all_pages=True, return_metadata=False
    afetch_all_results.return_value = [{"id": 2}]
    result = await data_api.aget_data_by_variable("v", all_pages=True, return_metadata=False)
    assert result == [{"id": 2}]
    # all_pages=False, return_metadata=True
    afetch_single_result.return_value = ([{"id": 3}], {"meta": 3})
    result = await data_api.aget_data_by_variable("v", all_pages=False, return_metadata=True)
    assert result == ([{"id": 3}], {"meta": 3})
    # all_pages=False, return_metadata=False
    afetch_single_result.return_value = [{"id": 4}]
    result = await data_api.aget_data_by_variable("v", all_pages=False, return_metadata=False)
    assert result == [{"id": 4}]


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_unit_all_branches(afetch_single_result: AsyncMock, data_api: DataAPI) -> None:
    afetch_single_result.return_value = ([{"id": 1}], {"meta": 1})
    result = await data_api.aget_data_by_unit("u", "var", return_metadata=True)
    assert result == ([{"id": 1}], {"meta": 1})
    afetch_single_result.return_value = [{"id": 2}]
    result = await data_api.aget_data_by_unit("u", "var", return_metadata=False)
    assert result == [{"id": 2}]


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_variable_locality_all_branches(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, data_api: DataAPI
) -> None:
    afetch_all_results.return_value = ([{"id": 1}], {"meta": 1})
    result = await data_api.aget_data_by_variable_locality("v", "l", all_pages=True, return_metadata=True)
    assert result == ([{"id": 1}], {"meta": 1})
    afetch_all_results.return_value = [{"id": 2}]
    result = await data_api.aget_data_by_variable_locality("v", "l", all_pages=True, return_metadata=False)
    assert result == [{"id": 2}]
    afetch_single_result.return_value = ([{"id": 3}], {"meta": 3})
    result = await data_api.aget_data_by_variable_locality("v", "l", all_pages=False, return_metadata=True)
    assert result == ([{"id": 3}], {"meta": 3})
    afetch_single_result.return_value = [{"id": 4}]
    result = await data_api.aget_data_by_variable_locality("v", "l", all_pages=False, return_metadata=False)
    assert result == [{"id": 4}]


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_unit_locality_all_branches(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, data_api: DataAPI
) -> None:
    afetch_all_results.return_value = ([{"id": 1}], {"meta": 1})
    result = await data_api.aget_data_by_unit_locality("u", all_pages=True, return_metadata=True)
    assert result == ([{"id": 1}], {"meta": 1})
    afetch_all_results.return_value = [{"id": 2}]
    result = await data_api.aget_data_by_unit_locality("u", all_pages=True, return_metadata=False)
    assert result == [{"id": 2}]
    afetch_single_result.return_value = ([{"id": 3}], {"meta": 3})
    result = await data_api.aget_data_by_unit_locality("u", all_pages=False, return_metadata=True)
    assert result == ([{"id": 3}], {"meta": 3})
    afetch_single_result.return_value = [{"id": 4}]
    result = await data_api.aget_data_by_unit_locality("u", all_pages=False, return_metadata=False)
    assert result == [{"id": 4}]


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_metadata(afetch_single_result: AsyncMock, data_api: DataAPI) -> None:
    afetch_single_result.return_value = {"meta": "data"}
    result = await data_api.aget_data_metadata()
    assert result == {"meta": "data"}


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_params(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.return_value = (
        {"year": 2020, "unit-level": 2, "parent-id": "pid", "format": "csv", "foo": "bar"},
        {"meta": 1},
    )
    result, meta = await data_api.aget_data_by_variable(
        variable_id="v",
        year=2020,
        unit_level=2,
        parent_id="pid",
        format="csv",
        extra_query={"foo": "bar"},
        all_pages=True,
        return_metadata=True,
    )
    assert result["year"] == 2020
    assert result["unit-level"] == 2
    assert result["parent-id"] == "pid"
    assert result["format"] == "csv"
    assert result["foo"] == "bar"


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_async_get_data_by_unit_params(afetch_single_result: AsyncMock, data_api: DataAPI) -> None:
    afetch_single_result.return_value = {"year": 2021, "format": "csv", "bar": "baz"}
    result = await data_api.aget_data_by_unit(
        unit_id="u",
        variable="v",
        year=2021,
        format="csv",
        extra_query={"bar": "baz"},
        return_metadata=True,
    )
    assert result["year"] == 2021
    assert result["format"] == "csv"
    assert result["bar"] == "baz"


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_locality_params(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.return_value = ({"year": 2022, "format": "csv", "baz": "qux"}, {"meta": 1})
    result, meta = await data_api.aget_data_by_variable_locality(
        variable_id="v",
        locality_id="l",
        year=2022,
        format="csv",
        extra_query={"baz": "qux"},
        all_pages=True,
        return_metadata=True,
    )
    assert result["year"] == 2022
    assert result["format"] == "csv"
    assert result["baz"] == "qux"


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_unit_locality_params(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    afetch_all_results.return_value = ({"year": 2023, "format": "csv", "qux": "quux"}, {"meta": 1})
    result, meta = await data_api.aget_data_by_unit_locality(
        unit_id="u",
        variable_id="v",
        year=2023,
        format="csv",
        extra_query={"qux": "quux"},
        all_pages=True,
        return_metadata=True,
    )
    assert result["year"] == 2023
    assert result["format"] == "csv"
    assert result["qux"] == "quux"


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_variable_edge_cases(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    # Empty results
    afetch_all_results.return_value = ([], {"meta": 1})
    result = await data_api.aget_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)
    assert result == ([], {"meta": 1})
    # Missing metadata
    afetch_all_results.return_value = ([{"id": 1}], None)
    result = await data_api.aget_data_by_variable(variable_id="v", all_pages=True, return_metadata=True)
    assert result == ([{"id": 1}], None)


@pytest.mark.asyncio
@patch.object(DataAPI, "afetch_all_results", new_callable=AsyncMock)
async def test_async_get_data_by_unit_locality_edge_cases(afetch_all_results: AsyncMock, data_api: DataAPI) -> None:
    # Empty results
    afetch_all_results.return_value = ([], {"meta": 1})
    result = await data_api.aget_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)
    assert result == ([], {"meta": 1})
    # Missing metadata
    afetch_all_results.return_value = ([{"id": 1}], None)
    result = await data_api.aget_data_by_unit_locality(unit_id="u", all_pages=True, return_metadata=True)
    assert result == ([{"id": 1}], None)
