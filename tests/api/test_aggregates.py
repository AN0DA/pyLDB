import pytest
import responses

from pyldb.api.aggregates import AggregatesAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def aggregates_api(dummy_config: LDBConfig) -> AggregatesAPI:
    return AggregatesAPI(dummy_config)


@responses.activate
def test_list_aggregates(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates"
    paginated_mock(url, [{"id": 1, "name": "Agg1"}])
    result = aggregates_api.list_aggregates()
    assert isinstance(result, list)
    assert result[0]["name"] == "Agg1"


@responses.activate
def test_list_aggregates_with_sort(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates?sort=Name&lang=en&page=0&page-size=100"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    aggregates_api.list_aggregates(sort="Name")
    # With responses, you can inspect the call arguments:
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "sort=Name" in called_url
    assert "lang=en" in called_url
    assert "page=0" in called_url
    assert "page-size=100" in called_url


@responses.activate
def test_get_aggregate_info(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates/42"
    expected = {"id": 42, "name": "Agg42"}
    responses.add(responses.GET, url, json=expected, status=200)
    result = aggregates_api.get_aggregate_info(aggregate_id="42")
    assert result["id"] == 42


@responses.activate
def test_list_aggregates_metadata(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates/metadata"
    paginated_mock(url, [{"id": "4", "name": "AggMeta"}])
    result = aggregates_api.list_aggregates_metadata()
    assert isinstance(result, list)
    assert result[0]["name"] == "AggMeta"


@responses.activate
def test_get_aggregate_metadata_info(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates/metadata/4"
    expected = {"id": "4", "name": "AggMeta"}
    responses.add(responses.GET, url, json=expected, status=200)
    result = aggregates_api.get_aggregate_metadata_info(aggregate_id="4")
    assert result["id"] == "4"


@responses.activate
def test_get_aggregates_metadata(aggregates_api: AggregatesAPI, api_url: str) -> None:
    url = f"{api_url}/aggregates/metadata"
    expected = {"info": "Metadata"}
    responses.add(responses.GET, url, json=expected, status=200)
    result = aggregates_api.get_aggregates_metadata()
    assert result["info"] == "Metadata"
