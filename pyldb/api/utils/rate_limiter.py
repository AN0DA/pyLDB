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
    """
    Persistent cache for API quota usage, stored on disk.

    This class provides thread-safe, persistent storage for quota usage data,
    allowing rate limiters to survive process restarts and share state between sessions.
    """

    def __init__(self, enabled: bool = True) -> None:
        """
        Initialize the persistent quota cache.

        Args:
            enabled: Whether to enable persistent caching.
        """
        self.enabled = enabled
        self.cache_file = get_cache_file_path("quota_cache.json")
        self._lock = threading.Lock()
        self._data: dict[str, Any] = {}
        if self.enabled:
            self._load()

    def _load(self) -> None:
        """
        Load quota data from the cache file.
        """
        try:
            with open(self.cache_file) as f:
                self._data = json.load(f)
        except Exception:
            self._data = {}

    def _save(self) -> None:
        """
        Save quota data to the cache file.
        """
        if not self.enabled:
            return
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self._data, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save quota cache to {self.cache_file}") from e

    def get(self, key: str) -> Any:
        """
        Retrieve a cached value by key.

        Args:
            key: Cache key.
        Returns:
            Cached value, or [] if not found or disabled.
        """
        if not self.enabled:
            return []
        with self._lock:
            return self._data.get(key, [])

    def set(self, key: str, value: Any) -> None:
        """
        Set a cached value by key and persist it.

        Args:
            key: Cache key.
            value: Value to store.
        """
        if not self.enabled:
            return
        with self._lock:
            self._data[key] = value
            self._save()


class RateLimiter:
    """
    Thread-safe synchronous rate limiter for API requests.

    Enforces multiple quota periods (e.g., per second, per minute) and persists usage if a cache is provided.
    """

    def __init__(
        self, quotas: dict[int, int | tuple], is_registered: bool, cache: PersistentQuotaCache | None = None
    ) -> None:
        """
        Initialize the rate limiter.

        Args:
            quotas: Dictionary of {period_seconds: limit or (anon_limit, reg_limit)}.
            is_registered: Whether the user is registered (affects quota).
            cache: Optional persistent cache for quota usage.
        """
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
        """
        Acquire a slot for an API request, blocking if over quota.

        Raises:
            RuntimeError: If the rate limit is exceeded for any period.
        """
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
    """
    Asyncio-compatible rate limiter for API requests.

    Enforces multiple quota periods and persists usage if a cache is provided.
    """

    def __init__(
        self, quotas: dict[int, int | tuple], is_registered: bool, cache: PersistentQuotaCache | None = None
    ) -> None:
        """
        Initialize the async rate limiter.

        Args:
            quotas: Dictionary of {period_seconds: limit or (anon_limit, reg_limit)}.
            is_registered: Whether the user is registered (affects quota).
            cache: Optional persistent cache for quota usage.
        """
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
        """
        Acquire a slot for an API request asynchronously, raising if over quota.

        Raises:
            RuntimeError: If the rate limit is exceeded for any period.
        """
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
