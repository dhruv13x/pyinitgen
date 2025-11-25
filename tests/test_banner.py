# tests/test_banner.py


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

        # Verify the footer
        args, kwargs = mock_console.print.call_args
        assert "[dim]📂 Automated __init__.py generator for Python packages.[/dim]" in args[0]
