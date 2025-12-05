# tests/test_cli.py

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from pyinitgen.cli import create_inits
from pyinitgen.config import EXCLUDE_DIRS


@pytest.fixture
def temp_dir(tmp_path):
    """
    Creates a temporary directory structure for testing.
    """
    # Create a basic structure
    (tmp_path / "project_root").mkdir()
    (tmp_path / "project_root" / "package_a").mkdir()
    (tmp_path / "project_root" / "package_a" / "subpackage_a").mkdir()
    (tmp_path / "project_root" / "package_b").mkdir()
    (tmp_path / "project_root" / "package_b" / "subpackage_b").mkdir()
    
    # Create some excluded directories
    (tmp_path / "project_root" / ".git").mkdir()
    (tmp_path / "project_root" / "__pycache__").mkdir()
    (tmp_path / "project_root" / "node_modules").mkdir()
    (tmp_path / "project_root" / "docs").mkdir()
    (tmp_path / "project_root" / "venv").mkdir()
    (tmp_path / "project_root" / "data").mkdir()
    (tmp_path / "project_root" / "assets").mkdir()
    
    # Create a file to ensure it doesn't interfere
    (tmp_path / "project_root" / "package_a" / "module.py").touch()
    
    return tmp_path / "project_root"


def test_create_inits_dry_run(temp_dir):
    """
    Test that __init__.py files are not created in dry-run mode.
    """
    exit_code, created_count, scanned_dirs = create_inits(temp_dir, dry_run=True)

    assert exit_code == 0
    assert created_count == 0
    assert not (temp_dir / "package_a" / "__init__.py").exists()
    assert not (temp_dir / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert not (temp_dir / "package_b" / "__init__.py").exists()
    assert not (temp_dir / "package_b" / "subpackage_b" / "__init__.py").exists()


def test_create_inits_actual_run(temp_dir):
    """
    Test that __init__.py files are created correctly in actual run mode,
    and excluded directories are ignored.
    """
    exit_code, created_count, scanned_dirs = create_inits(temp_dir, dry_run=False)

    assert exit_code == 0
    # Expecting __init__.py in:
    # project_root (base_dir itself)
    # package_a
    # package_a/subpackage_a
    # package_b
    # package_b/subpackage_b
    assert created_count == 5 
    
    assert (temp_dir / "__init__.py").exists()
    assert (temp_dir / "package_a" / "__init__.py").exists()
    assert (temp_dir / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert (temp_dir / "package_b" / "__init__.py").exists()
    assert (temp_dir / "package_b" / "subpackage_b" / "__init__.py").exists()

    # Assert that __init__.py are NOT created in excluded directories
    assert not (temp_dir / ".git" / "__init__.py").exists()
    assert not (temp_dir / "__pycache__" / "__init__.py").exists()
    assert not (temp_dir / "node_modules" / "__init__.py").exists()
    assert not (temp_dir / "docs" / "__init__.py").exists()
    assert not (temp_dir / "venv" / "__init__.py").exists()
    assert not (temp_dir / "data" / "__init__.py").exists()
    assert not (temp_dir / "assets" / "__init__.py").exists()


def test_create_inits_existing_init_file(temp_dir):
    """
    Test that create_inits does not overwrite existing __init__.py files.
    """
    # Create an existing __init__.py file
    (temp_dir / "package_a" / "__init__.py").touch()
    
    exit_code, created_count, scanned_dirs = create_inits(temp_dir, dry_run=False)
    
    assert exit_code == 0
    # Only 4 new files should be created (project_root, subpackage_a, package_b, subpackage_b)
    assert created_count == 4 
    assert (temp_dir / "package_a" / "__init__.py").exists() # Should still exist
    assert (temp_dir / "package_a" / "subpackage_a" / "__init__.py").exists()
    assert (temp_dir / "package_b" / "__init__.py").exists()
    assert (temp_dir / "package_b" / "subpackage_b" / "__init__.py").exists()


def test_exclude_dirs_content():
    """
    Test that EXCLUDE_DIRS contains expected entries.
    This test is more for ensuring the constant itself is as expected.
    """
    expected_excludes = {
        ".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "env",
        ".mypy_cache", ".pytest_cache", ".ruff_cache", "node_modules",
        ".vscode", ".idea", ".DS_Store", "build", "dist", "eggs", ".egg-info",
        "docs", "site", ".github", "htmlcov", ".tox", ".nox",
        "pip-wheel-metadata", "tmp", "temp", "data", "assets", "static", "media"
    }
    assert EXCLUDE_DIRS == expected_excludes


def test_create_inits_with_ignore_file(tmp_path):
    """
    Test that __init__.py files are not created in directories specified
    in a .pyinitgenignore file.
    """
    project_root = tmp_path / "project_root_with_ignore"
    project_root.mkdir()

    # Create some directories, some of which will be ignored by the file
    (project_root / "package_x").mkdir()
    (project_root / "package_x" / "subpackage_x").mkdir()
    (project_root / "ignored_by_file").mkdir()
    (project_root / "another_ignored").mkdir()
    (project_root / "another_ignored" / "sub_ignored").mkdir()
    (project_root / "not_ignored").mkdir()

    # Create a .pyinitgenignore file
    ignore_file_content = """
# This is a comment
ignored_by_file
another_ignored
    """
    (project_root / ".pyinitgenignore").write_text(ignore_file_content)

    exit_code, created_count, scanned_dirs = create_inits(project_root, dry_run=False)

    assert exit_code == 0
    # Expected: project_root, package_x, subpackage_x, not_ignored
    assert created_count == 4

    assert (project_root / "__init__.py").exists()
    assert (project_root / "package_x" / "__init__.py").exists()
    assert (project_root / "package_x" / "subpackage_x" / "__init__.py").exists()
    assert (project_root / "not_ignored" / "__init__.py").exists()

    # Assert that __init__.py are NOT created in directories ignored by the file
    assert not (project_root / "ignored_by_file" / "__init__.py").exists()
    assert not (project_root / "another_ignored" / "__init__.py").exists()
    assert not (project_root / "another_ignored" / "sub_ignored" / "__init__.py").exists()


def test_create_inits_with_custom_content(temp_dir):
    """
    Test that __init__.py files are created with the specified custom content.
    """
    custom_content = "# This is a custom init file\n__version__ = '0.1.0'\n"
    exit_code, created_count, scanned_dirs = create_inits(
        temp_dir, dry_run=False, init_content=custom_content
    )

    assert exit_code == 0
    assert created_count == 5 # Same as actual run, but with content

    # Verify content of created __init__.py files
    assert (temp_dir / "__init__.py").read_text() == custom_content
    assert (temp_dir / "package_a" / "__init__.py").read_text() == custom_content
    assert (temp_dir / "package_a" / "subpackage_a" / "__init__.py").read_text() == custom_content
    assert (temp_dir / "package_b" / "__init__.py").read_text() == custom_content
    assert (temp_dir / "package_b" / "subpackage_b" / "__init__.py").read_text() == custom_content

    # Ensure existing __init__.py files are not overwritten with custom content
    # For this, we need to create an existing __init__.py with different content
    # and then run create_inits again.
    (temp_dir / "package_a" / "subpackage_a" / "__init__.py").write_text("existing content")
    exit_code, created_count, scanned_dirs = create_inits(
        temp_dir, dry_run=False, init_content="new content"
    )
    assert (temp_dir / "package_a" / "subpackage_a" / "__init__.py").read_text() == "existing content"


