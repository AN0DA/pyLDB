import os
from pathlib import Path

try:
    from platformdirs import user_cache_dir
except ImportError:
    user_cache_dir = None


def get_default_cache_path(use_global_cache: bool = False, custom_path: str = None):
    if custom_path:
        return custom_path
    if use_global_cache:
        # Use platformdirs if available, else fallback
        if user_cache_dir:
            return os.path.join(user_cache_dir("pyldb", "pyldb"))
        # Fallback to ~/.cache/pyldb/
        return os.path.expanduser("~/.cache/pyldb")
    # Project-scoped: ./my_project/.cache/pyldb/
    cwd = Path.cwd()
    cache_dir = cwd / ".cache" / "pyldb"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return str(cache_dir)
