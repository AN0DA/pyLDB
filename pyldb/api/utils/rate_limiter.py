import asyncio
import json
import threading
import time
from collections import deque

from pyldb.utils.cache import get_default_cache_path

try:
    from platformdirs import user_cache_dir
except ImportError:
    user_cache_dir = None


class PersistentQuotaCache:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.cache_file = get_default_cache_path()
        self._lock = threading.Lock()
        self._data = None
        if self.enabled:
            self._load()

    def _load(self):
        try:
            with open(self.cache_file) as f:
                self._data = json.load(f)
        except Exception:
            self._data = {}

    def _save(self):
        if not self.enabled:
            return
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self._data, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save quota cache to {self.cache_file}") from e

    def get(self, key):
        if not self.enabled:
            return []
        with self._lock:
            return self._data.get(key, [])

    def set(self, key, value):
        if not self.enabled:
            return
        with self._lock:
            self._data[key] = value
            self._save()


class RateLimiter:
    def __init__(self, quotas, is_registered, cache: PersistentQuotaCache = None):
        self.quotas = quotas
        self.is_registered = is_registered
        self.lock = threading.Lock()
        self.calls = {period: deque() for period in quotas}
        self.cache = cache
        self.cache_key = f"sync_{'reg' if is_registered else 'anon'}"
        if self.cache and self.cache.enabled:
            self._load_from_cache()

    def _get_limit(self, period):
        # quotas: {period: int}
        return self.quotas[period]

    def _load_from_cache(self):
        for period in self.quotas:
            cached = self.cache.get(f"{self.cache_key}_{period}")
            self.calls[period] = deque(cached)

    def _save_to_cache(self):
        if not self.cache or not self.cache.enabled:
            return
        for period in self.quotas:
            self.cache.set(f"{self.cache_key}_{period}", list(self.calls[period]))

    def acquire(self):
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
    def __init__(self, quotas, is_registered, cache: PersistentQuotaCache = None):
        self.quotas = quotas
        self.is_registered = is_registered
        self.locks = {period: asyncio.Lock() for period in quotas}
        self.calls = {period: deque() for period in quotas}
        self.cache = cache
        self.cache_key = f"async_{'reg' if is_registered else 'anon'}"
        if self.cache and self.cache.enabled:
            self._load_from_cache()

    def _get_limit(self, period):
        # quotas: {period: int}
        return self.quotas[period]

    def _load_from_cache(self):
        for period in self.quotas:
            cached = self.cache.get(f"{self.cache_key}_{period}")
            self.calls[period] = deque(cached)

    def _save_to_cache(self):
        if not self.cache or not self.cache.enabled:
            return
        for period in self.quotas:
            self.cache.set(f"{self.cache_key}_{period}", list(self.calls[period]))

    async def acquire(self):
        now = time.time()
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
        for period in self.quotas:
            self.calls[period].append(now)
        self._save_to_cache()
