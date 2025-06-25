import pytest
from pytest import MonkeyPatch

from pyldb.config import DEFAULT_CACHE_EXPIRY, DEFAULT_LANGUAGE, Language, LDBConfig


def test_config_direct_init() -> None:
    config = LDBConfig(api_key="abc123", language=Language.EN, use_cache=False, cache_expire_after=123)
    assert config.api_key == "abc123"
    assert config.language == Language.EN
    assert config.use_cache is False
    assert config.cache_expire_after == 123


def test_config_env(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("LDB_API_KEY", raising=False)
    monkeypatch.setenv("LDB_API_KEY", "envkey")
    monkeypatch.setenv("LDB_LANGUAGE", "pl")
    monkeypatch.setenv("LDB_USE_CACHE", "true")
    monkeypatch.setenv("LDB_CACHE_EXPIRY", "888")
    config = LDBConfig(api_key=None)
    assert config.api_key == "envkey"
    assert config.language == Language.PL
    assert config.use_cache is True
    assert config.cache_expire_after == 888


def test_config_env_false_cache(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "key2")
    monkeypatch.setenv("LDB_USE_CACHE", "false")
    config = LDBConfig(api_key=None)
    assert config.use_cache is False


def test_config_env_invalid_expiry(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "key3")
    monkeypatch.setenv("LDB_CACHE_EXPIRY", "badint")
    with pytest.raises(ValueError):
        LDBConfig(api_key=None)


def test_config_env_missing_key(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("LDB_API_KEY", raising=False)
    with pytest.raises(ValueError):
        LDBConfig(api_key=None)


def test_config_defaults(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("LDB_API_KEY", raising=False)
    # Provide api_key directly, others use defaults
    config = LDBConfig(api_key="directkey")
    assert config.language == DEFAULT_LANGUAGE
    assert config.use_cache is True
    assert config.cache_expire_after == DEFAULT_CACHE_EXPIRY
    assert config.proxy_url is None
    assert config.proxy_username is None
    assert config.proxy_password is None


def test_config_proxy_direct_init() -> None:
    config = LDBConfig(
        api_key="abc123", proxy_url="http://proxy.example.com:8080", proxy_username="user", proxy_password="pass"
    )
    assert config.proxy_url == "http://proxy.example.com:8080"
    assert config.proxy_username == "user"
    assert config.proxy_password == "pass"


def test_config_proxy_env(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "envkey")
    monkeypatch.setenv("LDB_PROXY_URL", "http://proxy.example.com:8080")
    monkeypatch.setenv("LDB_PROXY_USERNAME", "envuser")
    monkeypatch.setenv("LDB_PROXY_PASSWORD", "envpass")

    config = LDBConfig(api_key=None)
    assert config.proxy_url == "http://proxy.example.com:8080"
    assert config.proxy_username == "envuser"
    assert config.proxy_password == "envpass"


def test_config_quota_cache_env(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "key4")
    monkeypatch.setenv("LDB_QUOTA_CACHE_ENABLED", "false")
    monkeypatch.setenv("LDB_QUOTA_CACHE", "/tmp/quota.json")
    monkeypatch.setenv("LDB_USE_GLOBAL_CACHE", "true")
    config = LDBConfig(api_key=None)
    assert config.quota_cache_enabled is False
    assert config.quota_cache_file == "/tmp/quota.json"
    assert config.use_global_cache is True


def test_config_custom_quotas_env(monkeypatch: MonkeyPatch) -> None:
    import json

    monkeypatch.setenv("LDB_API_KEY", "key5")
    quotas = {1: 42, 900: 99, 43200: 123, 604800: 456}
    monkeypatch.setenv("LDB_QUOTAS", json.dumps(quotas))
    config = LDBConfig(api_key=None)
    for k, v in quotas.items():
        assert config.custom_quotas is not None
        assert config.custom_quotas[k] == v


def test_config_custom_quotas_invalid_json(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("LDB_API_KEY", "key6")
    monkeypatch.setenv("LDB_QUOTAS", "not-a-json")
    with pytest.raises(ValueError):
        LDBConfig(api_key=None)


def test_config_custom_quotas_not_dict(monkeypatch: MonkeyPatch) -> None:
    import json

    monkeypatch.setenv("LDB_API_KEY", "key7")
    monkeypatch.setenv("LDB_QUOTAS", json.dumps([1, 2, 3]))
    with pytest.raises(ValueError):
        LDBConfig(api_key=None)


def test_config_custom_quotas_invalid_keys(monkeypatch: MonkeyPatch) -> None:
    import json

    monkeypatch.setenv("LDB_API_KEY", "key8")
    # key is not a valid period, value is negative
    monkeypatch.setenv("LDB_QUOTAS", json.dumps({123: -1}))
    with pytest.raises(ValueError):
        LDBConfig(api_key=None)
