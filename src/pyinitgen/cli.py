#!/usr/bin/env python3
# src/pyinitgen/cli.py

import argparse
import logging
import os
from pathlib import Path
from .banner import print_logo

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


def load_ignore_patterns(base_dir: Path) -> set[str]:
    """
    Loads ignore patterns from a .pyinitgenignore file in the base_dir.
    """
    ignore_file_path = base_dir / IGNORE_FILE_NAME
    if not ignore_file_path.is_file():
        return set()

    patterns = set()
    with open(ignore_file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.add(line)
    return patterns


def create_inits(
    base_dir: Path,
    dry_run: bool = False,
    verbose: bool = False,
    use_emoji: bool = True,
    init_content: str = "",
):
    created_count = 0
    scanned_dirs = 0
    
    user_excludes = load_ignore_patterns(base_dir)
    all_excludes = EXCLUDE_DIRS.union(user_excludes)

    for root, dirs, files in os.walk(base_dir):
        # Filter out unwanted dirs
        dirs[:] = [d for d in dirs if d not in all_excludes]
        scanned_dirs += 1

        if verbose:
            logging.debug(f"Scanning: {root}")

        if "__init__.py" not in files:
            init_file = Path(root) / "__init__.py"
            if dry_run:
                logging.info(f"[DRY-RUN] Would create {init_file}")
            else:
                try:
                    with open(init_file, "w") as f:
                        f.write(init_content)
                    init_file.chmod(0o644) # Set permissions after writing
                    logging.info(f"Created {init_file}")
                    created_count += 1
                except Exception as e:
                    logging.error(f"Failed to create {init_file}: {e}")
                    return 1, created_count, scanned_dirs

    if dry_run:
        logging.info("Dry-run complete. No files created.")
    else:
        checkmark = "✅ " if use_emoji else ""
        logging.info(
            f"{checkmark}Operation complete. "
            f"Scanned {scanned_dirs} dirs, created {created_count} new __init__.py files."
        )

    return 0, created_count, scanned_dirs


def main():
    print_logo()
    parser = argparse.ArgumentParser(
        description="Ensure all directories have __init__.py files."
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        type=Path,
        help="Base directory to scan (default: current dir)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-error logs"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show scanned directories"
    )
    parser.add_argument(
        "--no-emoji", action="store_true", help="Disable emoji in output"
    )
    parser.add_argument(
        "--init-content",
        type=str,
        default="",
        help="Content to write to new __init__.py files (default: empty file)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s 1.0.0", help="Show program's version number and exit"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.ERROR
        if args.quiet
        else logging.DEBUG
        if args.verbose
        else logging.INFO,
        format="%(message)s",
    )

    exit_code, _, _ = create_inits(
        args.base_dir.resolve(),
        dry_run=args.dry_run,
        verbose=args.verbose,
        use_emoji=not args.no_emoji,
        init_content=args.init_content,
    )
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
