# -*- coding: utf-8 -*-
"""This file deals with testing the home module functions and logic.
No callbacks or online scripting is tested within this file.
For web-based tests see test_home_selenium.py.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pytest

from .. import overview_page
from .. import ui

__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


@pytest.fixture
def mrsim():
    return


# Need to import .mrsim file and use as dict


def test_ui():
    home_body = ui()

    assert isinstance(home_body, html.Div)
    assert home_body.className == "left-card active"
    assert home_body.id == "info-body"


def test_refresh():
    pass


# def test_overview_page():
#     mrsim = None  # Load some data

#     page = overview_page()
#     assert isinstance(page, html.Div)
