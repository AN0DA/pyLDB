from types import SimpleNamespace

from pytest import MonkeyPatch

from pyldb.client import LDB
from pyldb.config import LDBConfig, Language


def test_ldb_initializes_all_apis(monkeypatch: MonkeyPatch) -> None:
    # Use a dummy config and patch API classes to record instantiations
    class DummyAPI:
        def __init__(self, config: LDBConfig) -> None:
            self.config = config

    monkeypatch.setattr("pyldb.api.AggregatesAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.AttributesAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.DataAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.LevelsAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.MeasuresAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.SubjectsAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.UnitsAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.VariablesAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.VersionAPI", DummyAPI)
    monkeypatch.setattr("pyldb.api.YearsAPI", DummyAPI)

    config = LDBConfig(api_key="dummy")
    ldb = LDB(config=config)

    api = ldb.api
    assert isinstance(api, SimpleNamespace)
    # Check all endpoints exist and are DummyAPI instances
    assert isinstance(api.aggregates, DummyAPI)
    assert isinstance(api.attributes, DummyAPI)
    assert isinstance(api.data, DummyAPI)
    assert isinstance(api.levels, DummyAPI)
    assert isinstance(api.measures, DummyAPI)
    assert isinstance(api.subjects, DummyAPI)
    assert isinstance(api.units, DummyAPI)
    assert isinstance(api.variables, DummyAPI)
    assert isinstance(api.version, DummyAPI)
    assert isinstance(api.years, DummyAPI)
    # All configs passed through
    for attr in vars(api):
        assert getattr(api, attr).config is config


def test_ldb_config_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "envkey")
    monkeypatch.setenv("LDB_LANGUAGE", "en")
    monkeypatch.setenv("LDB_USE_CACHE", "0")
    monkeypatch.setenv("LDB_CACHE_EXPIRY", "42")
    ldb = LDB()
    assert ldb.config.api_key == "envkey"
    assert ldb.config.language == Language.EN
    assert ldb.config.use_cache is False
    assert ldb.config.cache_expire_after == 42
