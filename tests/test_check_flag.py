
import pytest
import os
from pathlib import Path
from pyinitgen.cli import create_inits

def test_check_flag_fail(fs):
    """
    Test that --check returns 1 if __init__.py is missing
    """
    # Create directory structure without __init__.py
    fs.create_dir("test_dir")

    # Run create_inits with check=True
    # Since I haven't modified create_inits signature yet, this test expects
    # to call it with check=True. However, to fail first, I will call it with
    # a new argument that doesn't exist yet, which will raise TypeError.
    # But to follow TDD properly, I should write the test as I want the API to look.

    # The existing signature is:
    # create_inits(base_dir, dry_run=False, verbose=False, use_emoji=True, init_content="")

    # I want to add check=True.

    # Assert return code is 1 and file is NOT created.
    exit_code, created, scanned = create_inits(Path("."), check=True)

    assert exit_code == 1
    assert created == 0
    assert not os.path.exists("test_dir/__init__.py")

def test_check_flag_pass(fs):
    """
    Test that --check returns 0 if all __init__.py exist
    """
    # Create directory structure WITH __init__.py
    fs.create_dir("test_dir")
    fs.create_file("test_dir/__init__.py")
    fs.create_file("__init__.py")

    # Run create_inits with check=True
    exit_code, created, scanned = create_inits(Path("."), check=True)

    assert exit_code == 0
    assert created == 0
