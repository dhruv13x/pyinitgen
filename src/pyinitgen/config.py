# src/pyinitgen/config.py

EXCLUDE_DIRS = {
    # VCS
    ".git",
    ".hg",
    ".svn",

    # Python Caches/Tools
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",

    # JS/Node
    "node_modules",

    # IDE / OS
    ".vscode",
    ".idea",
    ".DS_Store",

    # Build / Dist
    "build",
    "dist",
    "eggs",
    ".egg-info",

    # Docs
    "docs",
    "site",

    # Other tools
    ".github",

    # Python test/build artifacts
    "htmlcov",
    ".tox",
    ".nox",
    "pip-wheel-metadata",

    # Temporary/data directories
    "tmp",
    "temp",
    "data",
    "assets",
    "static",
    "media",
}

IGNORE_FILE_NAME = ".pyinitgenignore"
