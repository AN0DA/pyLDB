from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.variables import VariablesAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def variables_api(dummy_config: LDBConfig) -> VariablesAPI:
    return VariablesAPI(dummy_config)


@responses.activate
def test_list_variables(variables_api: VariablesAPI, api_url: str) -> None:
    url = f"{api_url}/variables"
    paginated_mock(url, [{"id": "1", "name": "Population"}])
    result = variables_api.list_variables()
    assert isinstance(result, list)
    assert result[0]["name"] == "Population"


@responses.activate
def test_list_variables_with_filters(variables_api: VariablesAPI, api_url: str) -> None:
    params = {
        "category-id": "cat",
        "aggregate-id": "agg",
        "name": "pop",
        "sort": "name",
        "lang": "en",
        "page-size": "100",
    }
    url = f"{api_url}/variables?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also add page 1 for completeness
    params["page"] = "1"
    url1 = f"{api_url}/variables?{urlencode(params)}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    variables_api.list_variables(category_id="cat", aggregate_id="agg", name="pop", sort="name")
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "category-id=cat" in called_url
    assert "aggregate-id=agg" in called_url
    assert "name=pop" in called_url
    assert "sort=name" in called_url


@responses.activate
def test_get_variable_info(variables_api: VariablesAPI, api_url: str) -> None:
    url = f"{api_url}/variables/1?lang=en"
    payload = {"id": "1", "name": "Population"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = variables_api.get_variable_info(variable_id="1")
    assert result["id"] == "1"
    assert result["name"] == "Population"


@responses.activate
def test_get_variables_metadata(variables_api: VariablesAPI, api_url: str) -> None:
    url = f"{api_url}/variables/metadata?lang=en"
    payload = {"info": "Variables API"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = variables_api.get_variables_metadata()
    assert result["info"] == "Variables API"
