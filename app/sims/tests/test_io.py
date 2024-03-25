# -*- coding: utf-8 -*-
"""This file deals with testing the io module functions and logic.
No callbacks or online scripting is tested within this file.
For web-based tests see test_io_selenium.py.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pytest

from ..io import fix_missing_keys
from ..io import import_file_from_url
from ..io import import_mrsim_file
from ..io import load_file_from_url
from ..io import load_local_file
from ..io import parse_data
from ..io import parse_file_contents


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


@pytest.fixture
def mrsim():
    """dict representation of a .mrsim file"""
    pass


def test_load_file_from_url():
    # TODO: find url of .mrsim file
    # url = ""
    # load_file = load_file_from_url(url)

    # assert load_file == mrsim
    pass


def test_load_local_file():
    # TODO: create local file
    # file_path = ""
    # load_file = load_local_file()
    pass


def test_import_file_from_url():
    pass


def test_import_mrsim_file():
    pass


def test_parse_file_contents():
    pass


def test_fix_missing_keys():
    pass


def test_parse_data(mrsim):
    # sim = parse_data(mrsim)

    # # TODO: write actual checks

    # assert sim["name"] == "Test file"
    # assert sim["description"] == "This is a test description"
    # assert sim["spin_systems"] == None
    # assert sim["methods"] == None
    # assert sim["config"] == None
    # assert sim["version"] == None
    # assert sim["signal_processors"] == None
    # assert sim["params"] == None

    pass
