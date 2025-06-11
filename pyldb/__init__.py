"""Python interface for Bank Danych Lokalnych (LDB) API."""

from pyldb.client import LDB
from pyldb.config import LDBConfig

__version__ = "0.0.1"
__all__ = ["LDB", "LDBConfig"]
