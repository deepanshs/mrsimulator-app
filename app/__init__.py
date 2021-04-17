# -*- coding: utf-8 -*-
import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash

from .head import head_config

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
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

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # html.Div(id="placeholder"),
        html.A(id="url-search", href=""),
    ],
    className="main",
)
