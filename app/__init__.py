# -*- coding: utf-8 -*-
import datetime

import dash_bootstrap_components as dbc
from dash import Dash

from .head import head_config

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]
__version__ = "v0.3.0"

now = datetime.datetime.now()
year = now.year

# Initialize dash app
app = Dash(
    __name__,
    title="Mrsimulator",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    **head_config,
)
