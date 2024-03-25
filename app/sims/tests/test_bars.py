# -*- coding: utf-8 -*-
"""This file deals with testing the menubar, navbar, and sidebar functions and logic.
No callbacks or online scripting is tested within this file.
For web-based tests see ####.py.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pytest

from ..menubar import className
from ..menubar import create_submenu
from ..menubar import file_menu
from ..menubar import help_menu
from ..menubar import icon_text
from ..menubar import layout
from ..menubar import menu_item
from ..menubar import method_menu
from ..menubar import spin_system_menu
from ..menubar import ui
from ..navbar import brand
from ..navbar import navbar_bottom_ui
from ..navbar import navbar_top_ui
from ..sidebar import advanced_settings_modal
from ..sidebar import fit  # TODO rename features
from ..sidebar import fit_report
from ..sidebar import home
from ..sidebar import method
from ..sidebar import settings
from ..sidebar import SIDEBAR_TAB_NAME
from ..sidebar import sidebar_tabs
from ..sidebar import spectrum
from ..sidebar import spin_system
from ..sidebar import ui
from ..sidebar import utility_tabs


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


# ================================== menubar.py tests ==================================
def test_icon_text():
    pass


def test_menu_item():
    pass


def test_create_submenu():
    pass


def test_file_menu():
    pass


def test_spin_system():
    pass


def test_method_menu():
    pass


def test_help_menu():
    pass


def test_layout():
    pass


def test_ui():
    pass


# ================================== navbar.py tests ===================================
def test_brand():
    pass


def test_navbar_top_ui():
    pass


def test_navbar_bottom_ui():
    pass


# ================================== sidebar.py tests ==================================
def test_icons():
    pass


def test_sidebar_tabs():
    pass


def test_advanced_settings_modal():
    pass


def test_utility_tabs():
    pass


def test_ui():
    pass
