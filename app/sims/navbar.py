# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

from .menubar import master_menubar
from app import year

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# The navgation bar displayed on the top of the web app.
def brand():
    icon = dcc.Link(
        html.Img(
            src="/assets/mrsimulator-logo-dark.svg",
            height="40px",
            alt="Mrsimulator",
        ),
        href="/",
    )
    return dbc.NavbarBrand(icon, class_name="logo")


def navbar_top_ui():
    bar = [
        brand(),
        master_menubar,
    ]
    return dbc.Navbar(dbc.Container(bar), color=None, dark=None, expand="md")


def navbar_bottom_ui():
    content = html.Div([dbc.Label(f"@mrsimulator, 2019-{year}", color="light")])
    return dbc.Navbar(
        dbc.Container([content]), color=None, dark=None, class_name="bottom-navbar"
    )


navbar_top = navbar_top_ui()
navbar_bottom = navbar_bottom_ui()
