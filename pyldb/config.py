import os
from dataclasses import dataclass, field

# API Constants
LDB_API_BASE_URL = "https://bdl.stat.gov.pl/api/v1"
DEFAULT_LANGUAGE = "pl"
DEFAULT_CACHE_EXPIRY = 3600  # 1 hour in seconds


@dataclass
class LDBConfig:
    """Configuration for LDB API client.

    The configuration can be set in three ways (in order of precedence):
    1. Direct parameter passing
    2. Environment variables
    3. Default values
    """

    api_key: str | None = field(default=None)
    language: str = field(default=DEFAULT_LANGUAGE)
    use_cache: bool = field(default=True)
    cache_expire_after: int = field(default=DEFAULT_CACHE_EXPIRY)

    def __post_init__(self) -> None:
        """Initialize configuration values from environment variables if not set directly."""
        # Get API key from environment if not provided directly
        if self.api_key is None:
            self.api_key = os.getenv("LDB_API_KEY")
            if not self.api_key:
                raise ValueError("API key must be provided either directly or through LDB_API_KEY environment variable")

        # Get language from environment if not provided directly
        env_language = os.getenv("LDB_LANGUAGE")
        if env_language:
            self.language = env_language

        # Get cache settings from environment if not provided directly
        env_use_cache = os.getenv("LDB_USE_CACHE")
        if env_use_cache is not None:
            self.use_cache = env_use_cache.lower() in ("true", "1", "yes")

        env_cache_expiry = os.getenv("LDB_CACHE_EXPIRY")
        if env_cache_expiry is not None:
            try:
                self.cache_expire_after = int(env_cache_expiry)
            except ValueError as e:
                raise ValueError("LDB_CACHE_EXPIRY must be an integer") from e
