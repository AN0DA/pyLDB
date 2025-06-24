import os
from collections.abc import Callable
from pathlib import Path

from platformdirs import user_cache_dir as _user_cache_dir

user_cache_dir: Callable[[str, str], str] | None = _user_cache_dir


def get_default_cache_path(use_global_cache: bool = False, custom_path: str | None = None) -> str:
    """Get the default cache directory path.

    Args:
        use_global_cache: If True, use global cache directory (~/.cache/pyldb or system cache dir).
                         If False, use project-scoped cache (./.cache/pyldb).
        custom_path: Custom cache directory path to use instead of defaults.

    Returns:
        str: Path to the cache directory (not a specific file).
    """
    if custom_path:
        Path(custom_path).mkdir(parents=True, exist_ok=True)
        return custom_path
    if use_global_cache:
        # Use platformdirs if available, else fallback
        if user_cache_dir is not None:
            cache_dir = user_cache_dir("pyldb", "pyldb")
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
            return cache_dir
        # Fallback to ~/.cache/pyldb/
        fallback_cache_dir = os.path.expanduser("~/.cache/pyldb")
        os.makedirs(fallback_cache_dir, exist_ok=True)
        return fallback_cache_dir
    # Project-scoped: ./my_project/.cache/pyldb/
    cwd = Path.cwd()
    project_cache_dir: Path = cwd / ".cache" / "pyldb"
    project_cache_dir.mkdir(parents=True, exist_ok=True)
    return str(project_cache_dir)


def get_cache_file_path(filename: str, use_global_cache: bool = False, custom_path: str | None = None) -> str:
    """Get the path to a specific cache file.

    Args:
        filename: Name of the cache file (e.g., 'quota_cache.json').
        use_global_cache: If True, use global cache directory.
        custom_path: Custom cache directory path to use instead of defaults.

    Returns:
        str: Full path to the cache file.
    """
    cache_dir = get_default_cache_path(use_global_cache, custom_path)
    return os.path.join(cache_dir, filename)
