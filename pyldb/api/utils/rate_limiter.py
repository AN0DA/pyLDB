import asyncio
import json
import threading
import time
from collections import deque
from typing import Any

from platformdirs import user_cache_dir as _user_cache_dir

from pyldb.utils.cache import get_cache_file_path

user_cache_dir: Any | None = _user_cache_dir


class PersistentQuotaCache:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self.cache_file = get_cache_file_path("quota_cache.json")
        self._lock = threading.Lock()
        self._data: dict[str, Any] = {}
        if self.enabled:
            self._load()

    def _load(self) -> None:
        try:
            with open(self.cache_file) as f:
                self._data = json.load(f)
        except Exception:
            self._data = {}

    def _save(self) -> None:
        if not self.enabled:
            return
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self._data, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save quota cache to {self.cache_file}") from e

    def get(self, key: str) -> Any:
        if not self.enabled:
            return []
        with self._lock:
            return self._data.get(key, [])

    def set(self, key: str, value: Any) -> None:
        if not self.enabled:
            return
        with self._lock:
            self._data[key] = value
            self._save()


class RateLimiter:
    def __init__(
        self, quotas: dict[int, int | tuple], is_registered: bool, cache: PersistentQuotaCache | None = None
    ) -> None:
        self.quotas = quotas
        self.is_registered = is_registered
        self.lock = threading.Lock()
        self.calls: dict[int, deque[float]] = {period: deque() for period in quotas}
        self.cache = cache
        self.cache_key = f"sync_{'reg' if is_registered else 'anon'}"
        if self.cache and self.cache.enabled:
            self._load_from_cache()

    def _get_limit(self, period: int) -> int:
        # quotas: {period: tuple of (anonymous_limit, registered_limit) or int}
        limit_value = self.quotas[period]
        if isinstance(limit_value, tuple):
            return limit_value[1] if self.is_registered else limit_value[0]
        return limit_value

    def _load_from_cache(self) -> None:
        if self.cache is not None:
            for period in self.quotas:
                cached = self.cache.get(f"{self.cache_key}_{period}")
                self.calls[period] = deque(cached)

    def _save_to_cache(self) -> None:
        if not self.cache or not self.cache.enabled:
            return
        for period in self.quotas:
            self.cache.set(f"{self.cache_key}_{period}", list(self.calls[period]))

    def acquire(self) -> None:
        now = time.time()
        with self.lock:
            for period in self.quotas:
                q = self.calls[period]
                limit = self._get_limit(period)
                # Remove old calls
                while q and q[0] <= now - period:
                    q.popleft()
                if len(q) >= limit:
                    wait = period - (now - q[0])
                    self._save_to_cache()
                    raise RuntimeError(
                        f"Rate limit exceeded: {limit} requests per {period}s. Try again in {wait:.1f}s."
                    )
            # Record this call
            for period in self.quotas:
                self.calls[period].append(now)
            self._save_to_cache()


class AsyncRateLimiter:
    def __init__(
        self, quotas: dict[int, int | tuple], is_registered: bool, cache: PersistentQuotaCache | None = None
    ) -> None:
        self.quotas = quotas
        self.is_registered = is_registered
        self.locks = {period: asyncio.Lock() for period in quotas}
        self.calls: dict[int, deque[float]] = {period: deque() for period in quotas}
        self.cache = cache
        self.cache_key = f"async_{'reg' if is_registered else 'anon'}"
        if self.cache and self.cache.enabled:
            self._load_from_cache()

    def _get_limit(self, period: int) -> int:
        # quotas: {period: tuple of (anonymous_limit, registered_limit) or int}
        limit_value = self.quotas[period]
        if isinstance(limit_value, tuple):
            return limit_value[1] if self.is_registered else limit_value[0]
        return limit_value

    def _load_from_cache(self) -> None:
        if self.cache is not None:
            for period in self.quotas:
                cached = self.cache.get(f"{self.cache_key}_{period}")
                self.calls[period] = deque(cached)

    def _save_to_cache(self) -> None:
        if not self.cache or not self.cache.enabled:
            return
        for period in self.quotas:
            self.cache.set(f"{self.cache_key}_{period}", list(self.calls[period]))

    async def acquire(self) -> None:
        now = time.time()
        # Check all periods and raise immediately if any limit is exceeded
        for period in self.quotas:
            async with self.locks[period]:
                q = self.calls[period]
                limit = self._get_limit(period)
                while q and q[0] <= now - period:
                    q.popleft()
                if len(q) >= limit:
                    wait = period - (now - q[0])
                    self._save_to_cache()
                    raise RuntimeError(
                        f"Rate limit exceeded: {limit} requests per {period}s. Try again in {wait:.1f}s."
                    )
        # Record this call for all periods
        for period in self.quotas:
            self.calls[period].append(now)
        self._save_to_cache()
