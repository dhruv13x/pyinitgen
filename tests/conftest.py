
import pytest
import os
import shutil
from pathlib import Path

# Common mocks are handled via pytest-mock, so no need for extensive custom fixture
# unless we have complex object creation.

# The 'fs' fixture comes from pyfakefs and is automatically available if pyfakefs is installed
# and configured. pyinitgen has it in dev dependencies.

@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    """
    Ensure environment variables are clean before each test.
    """
    # Prevent tests from being affected by or affecting the real environment variables
    # especially for banner tests.
    monkeypatch.delenv("CREATE_DUMP_PALETTE", raising=False)
