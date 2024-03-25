# -*- coding: utf-8 -*-
"""This file deals with testing the site.py functions and logic.
No callbacks or online scripting is tested within this file.
For web-based tests see ####.py.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pytest

from ..site import collapsable_card_ui
from ..site import isotope_and_shift_ui
from ..site import quadrupolar_ui
from ..site import shielding_symmetric_ui
from ..site import ui


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"
