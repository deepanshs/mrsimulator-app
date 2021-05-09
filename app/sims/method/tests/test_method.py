# -*- coding: utf-8 -*-
import math

import pytest
from dash.exceptions import PreventUpdate

from .. import sigma_helper


@pytest.fixture
def example_data():
    # NOTE: Only the keys-value pairs accessed by the tests are included
    return [
        -2.2,
        -0.8,
        2.3,
        1.4,
        1.9,
        -0.4,
        -1.6,
        1.9,
        -0.6,
        -1.3,
        1.0,
        -1.9,
        -1.3,
        -3.8,
        0.5,
        -1.9,
        1.6,
        1.2,
        -1.1,
        3.7,
        3.0,
        1.5,
        -0.7,
        1.7,
        1.5,
    ]


def test_sigma_helper_full_range(example_data):
    assert math.isclose(
        sigma_helper(x0=15, dx=-1, shape_x0=15, shape_x1=-10, y_values=example_data),
        1.831344861024269,
    ), "σ wrong (exact bounds; shape left to right)"

    assert math.isclose(
        sigma_helper(x0=15, dx=-1, shape_x0=-10, shape_x1=15, y_values=example_data),
        1.831344861024269,
    ), "σ wrong (exact bounds; shape right to left)"

    assert math.isclose(
        sigma_helper(x0=20, dx=-0.4, shape_x0=25, shape_x1=0, y_values=example_data),
        1.831344861024269,
    ), "σ wrong (extended bounds; shape left to right)"


def test_sigma_helper_extended_left_bounds(example_data):
    assert math.isclose(
        sigma_helper(x0=20, dx=-0.4, shape_x0=25, shape_x1=15.9, y_values=example_data),
        1.571114254279427,
    ), "σ wrong (extended left bound; first 10 elements; shape left to right)"

    assert math.isclose(
        sigma_helper(x0=20, dx=-0.4, shape_x0=15.9, shape_x1=25, y_values=example_data),
        1.571114254279427,
    ), "σ wrong (extended left bound; first 10 elements; shape right to left)"


def test_sigma_helper_extended_right_bounds(example_data):
    assert math.isclose(
        sigma_helper(x0=20, dx=-0.4, shape_x0=14.1, shape_x1=5, y_values=example_data),
        1.6841912005470163,
    ), "σ wrong (extended right bound; last 10 elements; shape left to right)"

    assert math.isclose(
        sigma_helper(x0=20, dx=-0.4, shape_x0=5, shape_x1=14.1, y_values=example_data),
        1.6841912005470163,
    ), "σ wrong (extended right bound; last 10 elements; shape right to left)"


def test_sigma_helper_middle_bounds(example_data):
    assert math.isclose(
        sigma_helper(
            x0=20, dx=-0.4, shape_x0=18.1, shape_x1=13.9, y_values=example_data
        ),
        1.5059660966627104,
    ), "σ wrong (elements 5 through 15; shape left to right)"

    assert math.isclose(
        sigma_helper(
            x0=20, dx=-0.4, shape_x0=13.9, shape_x1=18.1, y_values=example_data
        ),
        1.5059660966627104,
    ), "σ wrong (elements 5 through 15; shape left to right)"


def test_sigma_helper_exceptions(example_data):
    # Positive dx
    with pytest.raises(PreventUpdate):
        sigma_helper(x0=0, dx=1, shape_x0=0, shape_x1=25, y_values=example_data)

    # Out of bounds left
    with pytest.raises(PreventUpdate):
        sigma_helper(x0=0, dx=-1, shape_x0=10, shape_x1=5, y_values=example_data)

    # Out of bounds right
    with pytest.raises(PreventUpdate):
        sigma_helper(x0=0, dx=-1, shape_x0=-30, shape_x1=-35, y_values=example_data)

    # Empty y_values
    with pytest.raises(PreventUpdate):
        sigma_helper(x0=0, dx=-1, shape_x0=0, shape_x1=-10, y_values=[])
