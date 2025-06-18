from urllib.parse import urlencode

import pytest
import responses

from pyldb.api.subjects import SubjectsAPI
from pyldb.config import LDBConfig
from tests.conftest import paginated_mock


@pytest.fixture
def subjects_api(dummy_config: LDBConfig) -> SubjectsAPI:
    return SubjectsAPI(dummy_config)


@responses.activate
def test_list_subjects(subjects_api: SubjectsAPI, api_url: str) -> None:
    url = f"{api_url}/subjects"
    paginated_mock(url, [{"id": "A", "name": "Demography"}])
    result = subjects_api.list_subjects()
    assert isinstance(result, list)
    assert result[0]["name"] == "Demography"


@responses.activate
def test_list_subjects_with_parent_and_sort(subjects_api: SubjectsAPI, api_url: str) -> None:
    params = {"parent-id": "A", "sort": "name", "lang": "en", "page-size": "100"}
    url = f"{api_url}/subjects?{urlencode(params)}"
    responses.add(responses.GET, url, json={"results": []}, status=200)
    # Also add page 1 for completeness
    params["page"] = "1"
    url1 = f"{api_url}/subjects?{urlencode(params)}"
    responses.add(responses.GET, url1, json={"results": []}, status=200)
    subjects_api.list_subjects(parent_id="A", sort="name")
    called_url = responses.calls[0].request.url
    assert called_url is not None
    assert "parent-id=A" in called_url
    assert "sort=name" in called_url


@responses.activate
def test_get_subject(subjects_api: SubjectsAPI, api_url: str) -> None:
    url = f"{api_url}/subjects/B?lang=en"
    payload = {"id": "B", "name": "Labour market"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = subjects_api.get_subject(subject_id="B")
    assert result["id"] == "B"
    assert result["name"] == "Labour market"


@responses.activate
def test_get_subjects_metadata(subjects_api: SubjectsAPI, api_url: str) -> None:
    url = f"{api_url}/subjects/metadata?lang=en"
    payload = {"info": "Subjects API"}
    responses.add(responses.GET, url, json=payload, status=200)
    result = subjects_api.get_subjects_metadata()
    assert result["info"] == "Subjects API"
