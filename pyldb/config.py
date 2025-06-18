import enum
import os
from dataclasses import dataclass, field

# API Constants
LDB_API_BASE_URL = "https://bdl.stat.gov.pl/api/v1"


class Language(enum.Enum):
    PL = "pl"
    EN = "en"


DEFAULT_LANGUAGE = Language.EN
DEFAULT_CACHE_EXPIRY = 3600  # 1 hour in seconds


@dataclass
class LDBConfig:
    """Configuration for LDB API client.

    The configuration can be set in three ways (in order of precedence):

    1. Direct parameter passing
    2. Environment variables
    3. Default values


    Attributes:
        api_key: API key for authentication
        language: Language code for API responses (default: "pl")
        use_cache: Whether to use request caching (default: True)
        cache_expire_after: Cache expiration time in seconds (default: 3600)
        proxy_url: Optional URL of the proxy server
        proxy_username: Optional username for proxy authentication
        proxy_password: Optional password for proxy authentication
    """

    api_key: str | None = field(default=None)
    language: Language = field(default=DEFAULT_LANGUAGE)
    use_cache: bool = field(default=True)
    cache_expire_after: int = field(default=DEFAULT_CACHE_EXPIRY)
    proxy_url: str | None = field(default=None)
    proxy_username: str | None = field(default=None)
    proxy_password: str | None = field(default=None)

    def __post_init__(self) -> None:
        """Initialize configuration values from environment variables if not set directly."""
        # Get API key from environment if not provided directly
        if self.api_key is None:
            self.api_key = os.getenv("LDB_API_KEY")
            if not self.api_key:
                raise ValueError("API key must be provided either directly or through LDB_API_KEY environment variable")

        # Get language from environment if not provided directly
        # Convert provided language string to Language enum if necessary
        if isinstance(self.language, str):
            try:
                self.language = Language(self.language.lower())
            except ValueError as e:
                raise ValueError(f"language must be one of: {[lang.value for lang in Language]}") from e

        env_language = os.getenv("LDB_LANGUAGE")
        if env_language:
            try:
                self.language = Language(env_language.lower())
            except ValueError as e:
                raise ValueError(f"LDB_LANGUAGE must be one of: {[lang.value for lang in Language]}") from e

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

        # Get proxy settings from environment if not provided directly
        if self.proxy_url is None:
            self.proxy_url = os.getenv("LDB_PROXY_URL")

        if self.proxy_username is None:
            self.proxy_username = os.getenv("LDB_PROXY_USERNAME")

        if self.proxy_password is None:
            self.proxy_password = os.getenv("LDB_PROXY_PASSWORD")
