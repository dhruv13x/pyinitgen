# tests/test_banner.py

import os
import pytest
from unittest.mock import MagicMock, patch
from rich.text import Text
from pyinitgen.banner import lerp, blend, print_logo

def test_lerp():
    assert lerp(0, 10, 0.5) == 5.0
    assert lerp(10, 20, 0.5) == 15.0
    assert lerp(0, 100, 0.0) == 0.0
    assert lerp(0, 100, 1.0) == 100.0

def test_blend():
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)

    # Test t=0 (should be close to c1)
    result = blend(c1, c2, 0)
    # Note: blend modifies t with gamma/wave, so t=0 might not result in exactly c1 if the formula shifts it.
    # Let's check the formula: t = t ** 1.47; t = 0.82*t + 0.08*sin(3.2*t)
    # if t=0, t**1.47 = 0. 0.82*0 + 0.08*sin(0) = 0.
    # So it should be exactly c1.
    assert result == "#000000"

    # Test t=1
    # 1**1.47 = 1.
    # 0.82*1 + 0.08*sin(3.2)
    # sin(3.2) is approx -0.058
    # 0.82 - 0.08*0.058... = approx 0.815
    # So it won't be pure white.
    result = blend(c1, c2, 1)
    assert result.startswith("#")
    assert len(result) == 7

def test_print_logo():
    with patch("pyinitgen.banner.console") as mock_console:
        print_logo()
        assert mock_console.print.called
        # Check that it printed multiple times (lines of logo + footer)
        assert mock_console.print.call_count > 1

        # Verify the footer by checking the last call
        last_call_args, last_call_kwargs = mock_console.print.call_args_list[-1]
        expected_footer = "[dim]🐍 Automatically generate __init__.py files for Python packages.[/dim]\\n"
        assert last_call_args[0] == expected_footer

def test_print_logo_procedural_palette():
    """
    Test that print_logo can generate a procedural palette
    when no fixed palette is specified.
    """
    with patch("pyinitgen.banner.console") as mock_console:
        # Unset the env var to ensure procedural generation
        if "CREATE_DUMP_PALETTE" in os.environ:
            del os.environ["CREATE_DUMP_PALETTE"]

        print_logo()
        assert mock_console.print.called
        assert mock_console.print.call_count > 1

def test_print_logo_with_fixed_palette():
    """
    Test that print_logo uses a fixed palette when the env var is set.
    """
    with patch("pyinitgen.banner.console") as mock_console:
        os.environ["CREATE_DUMP_PALETTE"] = "0"
        print_logo()
        assert mock_console.print.called
        assert mock_console.print.call_count > 1

def test_print_logo_with_invalid_palette_fallback():
    """
    Test that print_logo falls back to procedural generation
    if an invalid palette index is provided.
    """
    with patch("pyinitgen.banner.console") as mock_console:
        os.environ["CREATE_DUMP_PALETTE"] = "invalid"
        print_logo()
        assert mock_console.print.called
        assert mock_console.print.call_count > 1

def test_blend_edge_cases():
    """
    Test the blend function with edge-case t values.
    """
    c1 = (0, 0, 0)
    c2 = (255, 255, 255)
    assert blend(c1, c2, 0.0) == "#000000"
    # A t-value of 1.0 doesn't produce pure white due to the wave shaping function.
    # We'll check that it's a valid hex color, but not pure white.
    result = blend(c1, c2, 1.0)
    assert result.startswith("#")
    assert result != "#ffffff"

def test_print_logo_with_large_invalid_palette_fallback():
    """
    Test fallback for an out-of-range integer palette index.
    """
    with patch("pyinitgen.banner.console") as mock_console:
        os.environ["CREATE_DUMP_PALETTE"] = "9999"
        print_logo()
        assert mock_console.print.called
        assert mock_console.print.call_count > 1
