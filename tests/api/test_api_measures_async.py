from unittest.mock import AsyncMock, patch

import pytest

from pyldb.api.measures import MeasuresAPI
from pyldb.config import LDBConfig


@pytest.fixture
def measures_api(dummy_config: LDBConfig) -> MeasuresAPI:
    return MeasuresAPI(dummy_config)


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_alist_measures_all_branches(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    # No params
    afetch_single_result.return_value = [{"id": 1}]
    result = await measures_api.alist_measures()
    assert result == [{"id": 1}]
    # With sort
    afetch_single_result.return_value = [{"id": 2}]
    result = await measures_api.alist_measures(sort="Name")
    assert result == [{"id": 2}]
    # With extra_query
    afetch_single_result.return_value = [{"id": 3}]
    result = await measures_api.alist_measures(extra_query={"foo": "bar"})
    assert result == [{"id": 3}]


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_measure_all_branches(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    afetch_single_result.return_value = {"id": 11}
    result = await measures_api.aget_measure(11)
    assert result["id"] == 11
    afetch_single_result.return_value = {"id": 12}
    result = await measures_api.aget_measure(12, extra_query={"foo": "bar"})
    assert result["id"] == 12


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_measures_metadata(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    afetch_single_result.return_value = {"version": "1.0"}
    result = await measures_api.aget_measures_metadata()
    assert result["version"] == "1.0"


class DummyException(Exception):
    pass


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_alist_measures_error(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    afetch_single_result.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await measures_api.alist_measures()


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_measure_error(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    afetch_single_result.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await measures_api.aget_measure(3)


@pytest.mark.asyncio
@patch.object(MeasuresAPI, "afetch_single_result", new_callable=AsyncMock)
async def test_aget_measures_metadata_error(afetch_single_result: AsyncMock, measures_api: MeasuresAPI) -> None:
    afetch_single_result.side_effect = DummyException("fail")
    with pytest.raises(DummyException):
        await measures_api.aget_measures_metadata()
