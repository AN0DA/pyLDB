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
