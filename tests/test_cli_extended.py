
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import logging
from pyinitgen.cli import main, create_inits, load_ignore_patterns

@pytest.fixture
def temp_dir(tmp_path):
    (tmp_path / "root").mkdir()
    return tmp_path / "root"

def test_load_ignore_patterns_no_file(temp_dir):
    assert load_ignore_patterns(temp_dir) == set()

def test_load_ignore_patterns_empty_file(temp_dir):
    (temp_dir / ".pyinitgenignore").touch()
    assert load_ignore_patterns(temp_dir) == set()

def test_load_ignore_patterns_complex(temp_dir):
    content = """
# comment
dir1

dir2/subdir
    """
    (temp_dir / ".pyinitgenignore").write_text(content)
    patterns = load_ignore_patterns(temp_dir)
    assert "dir1" in patterns
    assert "dir2/subdir" in patterns
    assert "# comment" not in patterns
    assert "" not in patterns

def test_main_arguments(temp_dir):
    with patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "--dry-run", "--quiet", "--no-emoji"]):
        with patch("pyinitgen.cli.create_inits") as mock_create:
            mock_create.return_value = (0, 0, 0)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0

            mock_create.assert_called_with(
                temp_dir.resolve(),
                dry_run=True,
                verbose=False,
                use_emoji=False,
                init_content=""
            )

def test_main_verbose(temp_dir):
    with patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "-v"]):
        with patch("pyinitgen.cli.create_inits") as mock_create:
            mock_create.return_value = (0, 0, 0)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0
            mock_create.assert_called_with(
                temp_dir.resolve(),
                dry_run=False,
                verbose=True,
                use_emoji=True,
                init_content=""
            )

def test_main_custom_content(temp_dir):
    content = "a=1"
    with patch("sys.argv", ["pyinitgen", "--base-dir", str(temp_dir), "--init-content", content]):
        with patch("pyinitgen.cli.create_inits") as mock_create:
            mock_create.return_value = (0, 0, 0)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0
            mock_create.assert_called_with(
                temp_dir.resolve(),
                dry_run=False,
                verbose=False,
                use_emoji=True,
                init_content=content
            )

def test_create_inits_error_handling(temp_dir, caplog):
    # Simulate an error when writing a file
    (temp_dir / "subdir").mkdir()

    with patch("builtins.open", side_effect=PermissionError("Boom")):
        exit_code, created, scanned = create_inits(temp_dir)
        assert exit_code == 1
        assert "Failed to create" in caplog.text
        assert "Boom" in caplog.text

def test_create_inits_logging(temp_dir, caplog):
    caplog.set_level(logging.DEBUG)
    (temp_dir / "subdir").mkdir()

    exit_code, created, scanned = create_inits(temp_dir, verbose=True)
    assert "Scanning:" in caplog.text
    assert (temp_dir / "subdir" / "__init__.py").exists()

def test_create_inits_dry_run_logging(temp_dir, caplog):
    caplog.set_level(logging.INFO)
    (temp_dir / "subdir").mkdir()

    exit_code, created, scanned = create_inits(temp_dir, dry_run=True)
    assert "[DRY-RUN] Would create" in caplog.text
    assert "Dry-run complete" in caplog.text
    assert not (temp_dir / "subdir" / "__init__.py").exists()

def test_main_version():
    with patch("sys.argv", ["pyinitgen", "--version"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
