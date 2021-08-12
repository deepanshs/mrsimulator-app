# -*- coding: utf-8 -*-
"""This file deals with testing the importer.py functions and logic.
No callbacks or online scripting is tested within this file.
For web-based tests see ####.py.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pytest

from ..importer import add_measurement_to_a_method
from ..importer import clear
from ..importer import clear_methods
from ..importer import clear_spin_systems
from ..importer import least_squares_fit
from ..importer import on_decompose_click
from ..importer import on_method_update
from ..importer import on_mrsim_config_change
from ..importer import on_spin_system_change
from ..importer import prep_valid_data_for_simulation
from ..importer import remove_measurement_from_a_method
from ..importer import save_info_modal
from ..importer import simulate_spectrum


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


# Most of these functions requrie ctx.states so cannot be tesed with pytest


def test_prep_valid_data_for_simulation():
    pass


def test_on_decompose_click():
    pass


def test_on_mrsim_config_change():
    pass


def test_clear():
    pass


def test_save_info_modal():
    pass


def test_on_method_update():
    pass


def test_on_spin_system_change():
    pass


def test_add_measurement_to_a_method():
    pass


def test_remove_measurement_from_a_method():
    pass


def test_simulate_spectrum():
    pass


def test_least_squares_fit():
    pass
