from types import SimpleNamespace

import pyldb.api as api
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
        self.api.aggregates = api.AggregatesAPI(self.config)
        self.api.attributes = api.AttributesAPI(self.config)
        self.api.data = api.DataAPI(self.config)
        self.api.levels = api.LevelsAPI(self.config)
        self.api.measures = api.MeasuresAPI(self.config)
        self.api.subjects = api.SubjectsAPI(self.config)
        self.api.units = api.UnitsAPI(self.config)
        self.api.variables = api.VariablesAPI(self.config)
        self.api.version = api.VersionAPI(self.config)
        self.api.years = api.YearsAPI(self.config)
