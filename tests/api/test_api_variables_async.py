from unittest.mock import AsyncMock, patch

import pytest

from pyldb.api.variables import VariablesAPI
from pyldb.config import LDBConfig


@pytest.fixture
def variables_api(dummy_config: LDBConfig) -> VariablesAPI:
    return VariablesAPI(dummy_config)


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_alist_variables_all_branches(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, variables_api: VariablesAPI
) -> None:
    # all_pages True
    afetch_all_results.return_value = [{"id": "1"}]
    result = await variables_api.alist_variables(all_pages=True)
    assert result == [{"id": "1"}]
    # all_pages False
    afetch_single_result.return_value = [{"id": "2"}]
    result = await variables_api.alist_variables(all_pages=False)
    assert result == [{"id": "2"}]
    # With all filters
    afetch_all_results.return_value = [{"id": "3"}]
    result = await variables_api.alist_variables(
        category_id="cat",
        aggregate_id="agg",
        name="pop",
        sort="name",
        page_size=10,
        max_pages=2,
        extra_query={"foo": "bar"},
        all_pages=True,
    )
    assert result == [{"id": "3"}]


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_variable_all_branches(afetch_single_result: AsyncMock, variables_api: VariablesAPI) -> None:
    afetch_single_result.return_value = {"id": "1"}
    result = await variables_api.aget_variable("1")
    assert result["id"] == "1"
    afetch_single_result.return_value = {"id": "2"}
    result = await variables_api.aget_variable("2", extra_query={"foo": "bar"})
    assert result["id"] == "2"


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_asearch_variables_all_branches(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, variables_api: VariablesAPI
) -> None:
    # all_pages True
    afetch_all_results.return_value = [{"id": "1"}]
    result = await variables_api.asearch_variables(all_pages=True)
    assert result == [{"id": "1"}]
    # all_pages False
    afetch_single_result.return_value = [{"id": "2"}]
    result = await variables_api.asearch_variables(all_pages=False)
    assert result == [{"id": "2"}]
    # With all filters
    afetch_all_results.return_value = [{"id": "3"}]
    result = await variables_api.asearch_variables(
        name="pop",
        category_id="cat",
        aggregate_id="agg",
        sort="name",
        page_size=10,
        max_pages=2,
        extra_query={"foo": "bar"},
        all_pages=True,
    )
    assert result == [{"id": "3"}]


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_variables_metadata(afetch_single_result: AsyncMock, variables_api: VariablesAPI) -> None:
    afetch_single_result.return_value = {"info": "meta"}
    result = await variables_api.aget_variables_metadata()
    assert result["info"] == "meta"


class _DummyException(Exception):
    pass


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_alist_variables_error(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, variables_api: VariablesAPI
) -> None:
    afetch_all_results.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.alist_variables(all_pages=True)
    afetch_single_result.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.alist_variables(all_pages=False)


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_variable_error(afetch_single_result: AsyncMock, variables_api: VariablesAPI) -> None:
    afetch_single_result.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.aget_variable("1")


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_all_results", new_callable=AsyncMock)
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_asearch_variables_error(
    afetch_single_result: AsyncMock, afetch_all_results: AsyncMock, variables_api: VariablesAPI
) -> None:
    afetch_all_results.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.asearch_variables(all_pages=True)
    afetch_single_result.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.asearch_variables(all_pages=False)


@pytest.mark.asyncio
@patch.object(VariablesAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_variables_metadata_error(afetch_single_result: AsyncMock, variables_api: VariablesAPI) -> None:
    afetch_single_result.side_effect = _DummyException("fail")
    with pytest.raises(_DummyException):
        await variables_api.aget_variables_metadata()
