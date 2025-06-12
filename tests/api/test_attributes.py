from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.attributes import AttributesAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def attributes_api(dummy_config: LDBConfig) -> AttributesAPI:
    return AttributesAPI(dummy_config)


@responses.activate
def test_list_attributes(attributes_api: AttributesAPI, api_url: str) -> None:
    url = f"{api_url}/attributes"
    paginated_mock(url, [{"id": 1, "name": "Attr1"}])
    result = attributes_api.list_attributes()
    assert isinstance(result, list)
    assert result[0]["name"] == "Attr1"


@responses.activate
def test_list_attributes_with_variable_id(attributes_api: AttributesAPI, api_url: str) -> None:
    base_url = f"{api_url}/attributes"
    query = urlencode({"variable-id": "5", "lang": "en", "page-size": "100"})
    url = f"{base_url}?{query}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    attributes_api.list_attributes(variable_id="5")
    # responses stores requests in responses.calls
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "variable-id=5" in called_url
    assert "lang=en" in called_url
    assert "page-size=100" in called_url


@responses.activate
def test_get_attribute_info(attributes_api: AttributesAPI, api_url: str) -> None:
    url = f"{api_url}/attributes/7"
    expected = {"id": 7, "name": "Attr7"}
    responses.add(responses.GET, url, json=expected, status=200)
    result = attributes_api.get_attribute_info(attribute_id="7")
    assert result["id"] == 7


@responses.activate
def test_get_attributes_metadata(attributes_api: AttributesAPI, api_url: str) -> None:
    url = f"{api_url}/attributes/metadata"
    expected = {"info": "Metadata"}
    responses.add(responses.GET, url, json=expected, status=200)
    result = attributes_api.get_attributes_metadata()
    assert result["info"] == "Metadata"
