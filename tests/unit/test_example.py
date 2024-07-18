# System imports
from __future__ import annotations

# Library imports
import numpy as np

# Local imports
import example

# Typing only imports


def test__gen_damped_data() -> None:
    """Unit test for the gen_damped_data function."""
    x_vals, y_vals = example.gen_damped_data()
    assert len(x_vals) == len(y_vals) == 50

    for x, y in zip(x_vals, y_vals, strict=True):
        assert isinstance(x, float)
        assert isinstance(y, float)
        expected_y = np.cos(2 * np.pi * x) * np.exp(-x)
        assert np.isclose(y, expected_y, atol=1e-8)

    max_x = max(x_vals)
    assert np.isclose(max_x, 5.0, atol=1e-8)

    assert max(y_vals) == y_vals[0]
    assert max(y_vals) <= 1.0
    assert min(y_vals) >= -1.0


def test__gen_undamped_data() -> None:
    """Unit test for the gen_undamped_data function."""
    x_vals, y_vals = example.gen_undamped_data()
    assert len(x_vals) == len(y_vals) == 50

    for x, y in zip(x_vals, y_vals, strict=True):
        assert isinstance(x, float)
        assert isinstance(y, float)
        expected_y = np.cos(2 * np.pi * x)
        assert np.isclose(y, expected_y, atol=1e-8)

    max_x = max(x_vals)
    assert np.isclose(max_x, 5.0, atol=1e-8)

    assert max(y_vals) <= 1.0
    assert min(y_vals) >= -1.0


def test__gen_underdamped_data() -> None:
    """Unit test for the gen_undamped_data function."""
    x_vals, y_vals = example.gen_underdamped_data()
    assert len(x_vals) == len(y_vals) == 50

    for x, y in zip(x_vals, y_vals, strict=True):
        assert isinstance(x, float)
        assert isinstance(y, float)
        expected_y = np.cos(2 * np.pi * x) * np.exp(0.2 * x)
        assert np.isclose(y, expected_y, atol=1e-8)

    max_x = max(x_vals)
    assert np.isclose(max_x, 5.0, atol=1e-8)

    assert max(y_vals) >= 1.0
    assert min(y_vals) <= -1.0
