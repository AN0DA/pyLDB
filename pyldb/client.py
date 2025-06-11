from types import SimpleNamespace

from pyldb.api.data import DataAPI
from pyldb.config import LDBConfig


class LDB:
    """Main interface for interacting with LDB API."""

    def __init__(self, config: LDBConfig | None = None):
        """Initialize LDB client.

        Args:
            config: Configuration object. If not provided, a new instance will be created
                   using environment variables and defaults.

        Note:
            Configuration can be set through:
            1. Direct parameter passing to LDBConfig
            2. Environment variables (LDB_API_KEY, LDB_LANGUAGE, etc.)
            3. Default values
        """
        self.config = config or LDBConfig()

        self.api = SimpleNamespace()
        self.api.data = DataAPI(self.config)
