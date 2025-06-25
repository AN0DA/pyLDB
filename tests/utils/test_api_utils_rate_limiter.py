import asyncio
import threading
import time
from collections.abc import Generator
from typing import Any

import pytest

from pyldb.api.utils import rate_limiter


@pytest.fixture(autouse=True)
def _enable_real_rate_limiting(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    # Undo the global patching from conftest.py for this test module
    monkeypatch.undo()
    yield


class DummyCache(rate_limiter.PersistentQuotaCache):
    def __init__(self) -> None:
        super().__init__(enabled=True)  # Set enabled=True so _save is called
        self._data = {}
        self._lock = threading.Lock()
        self.saved = False

    def _save(self) -> None:
        self.saved = True


def test_persistent_quota_cache_get_set(tmp_path: Any) -> None:
    cache_file = tmp_path / "quota_cache.json"
    cache = rate_limiter.PersistentQuotaCache(enabled=True)
    cache.cache_file = str(cache_file)
    cache.set("foo", [1, 2, 3])
    assert cache.get("foo") == [1, 2, 3]
    # Test persistence
    cache2 = rate_limiter.PersistentQuotaCache(enabled=True)
    cache2.cache_file = str(cache_file)
    cache2._load()
    assert cache2.get("foo") == [1, 2, 3]


def test_persistent_quota_cache_disabled() -> None:
    cache = rate_limiter.PersistentQuotaCache(enabled=False)
    cache.set("foo", [1, 2, 3])
    assert cache.get("foo") == []


def test_rate_limiter_basic() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 2, 5: 3}
    rl = rate_limiter.RateLimiter(quotas, is_registered=False)
    rl.acquire()
    rl.acquire()
    # Should raise on third call within 1s
    with pytest.raises(RuntimeError) as e:
        rl.acquire()
    assert "Rate limit exceeded" in str(e.value)


def test_rate_limiter_respects_period() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 2}
    rl = rate_limiter.RateLimiter(quotas, is_registered=False)
    rl.acquire()
    rl.acquire()
    with pytest.raises(RuntimeError):
        rl.acquire()
    time.sleep(1.1)
    rl.acquire()  # Should not raise


def test_rate_limiter_tuple_quota() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: (1, 2)}
    rl_anon = rate_limiter.RateLimiter(quotas, is_registered=False)
    rl_reg = rate_limiter.RateLimiter(quotas, is_registered=True)
    rl_anon.acquire()
    with pytest.raises(RuntimeError):
        rl_anon.acquire()
    rl_reg.acquire()
    rl_reg.acquire()
    with pytest.raises(RuntimeError):
        rl_reg.acquire()


def test_rate_limiter_cache() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 2}
    cache = DummyCache()
    rl = rate_limiter.RateLimiter(quotas, is_registered=False, cache=cache)
    rl.acquire()
    rl.acquire()
    with pytest.raises(RuntimeError):
        rl.acquire()
    assert cache.saved


def test_async_rate_limiter_basic() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 2}
    arl = rate_limiter.AsyncRateLimiter(quotas, is_registered=False)

    async def run() -> None:
        await arl.acquire()
        await arl.acquire()
        with pytest.raises(RuntimeError):
            await arl.acquire()

    asyncio.run(run())


def test_async_rate_limiter_tuple_quota() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: (1, 2)}
    arl_anon = rate_limiter.AsyncRateLimiter(quotas, is_registered=False)
    arl_reg = rate_limiter.AsyncRateLimiter(quotas, is_registered=True)

    async def run() -> None:
        await arl_anon.acquire()
        with pytest.raises(RuntimeError):
            await arl_anon.acquire()
        await arl_reg.acquire()
        await arl_reg.acquire()
        with pytest.raises(RuntimeError):
            await arl_reg.acquire()

    asyncio.run(run())


def test_async_rate_limiter_cache() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 2}
    cache = DummyCache()
    arl = rate_limiter.AsyncRateLimiter(quotas, is_registered=False, cache=cache)

    async def run() -> None:
        await arl.acquire()
        await arl.acquire()
        with pytest.raises(RuntimeError):
            await arl.acquire()
        assert cache.saved

    asyncio.run(run())


def test_rate_limiter_thread_safety() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 5}
    rl = rate_limiter.RateLimiter(quotas, is_registered=False)
    errors = []

    def worker() -> None:
        try:
            rl.acquire()
        except RuntimeError:
            errors.append(1)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(errors) >= 5


def test_async_rate_limiter_concurrent() -> None:
    quotas: dict[int, int | tuple[Any, ...]] = {1: 5}
    arl = rate_limiter.AsyncRateLimiter(quotas, is_registered=False)
    errors = []

    async def worker() -> None:
        try:
            await arl.acquire()
        except RuntimeError:
            errors.append(1)

    async def run() -> None:
        await asyncio.gather(*(worker() for _ in range(10)))
        assert sum(errors) >= 5

    asyncio.run(run())
