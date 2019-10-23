# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(dbc.Button("Search", color="primary", className="ml-2"), width="auto"),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


nav_items = dbc.Row(
    [
        dbc.NavLink(
            "Documentation",
            href="https://mrsimulator.readthedocs.io/en/stable/",
            # className="navbar-light expand-lg",
        ),
        dbc.NavLink(
            children=[html.I(className="fab fa-github-square"), "Github"],
            href="https://github.com/DeepanshS/mrsimulator",
            # className="navbar-light expand-lg",
        ),
    ],
    className="ml-auto",  # mt-3 mt-md-0 flex-nowrap
)

navbar_top = dbc.Navbar(
    [
        html.Div(
            [
                html.Img(src="/assets/mrsimulator-dark-featured.png", height="70px"),
                html.H5(
                    "A plotly-dash app",
                    style={"color": "white", "float": "center", "font-size": 16},
                ),
            ]
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([nav_items], id="navbar-collapse", navbar=True),
    ],
    color="dark",
    sticky="top",
    fixed="top",
    dark=True,
    # className="navbar navbar-expand-lg navbar-dark bg-dark",
)

navbar_bottom = dbc.Navbar(
    [
        dbc.Label("mrsimulator 2018-2019", style={"color": "white"}),
        html.I(className="fab fa-apple"),
    ],
    color="dark",
    sticky="bottom",
    # fixed="bottom",
    dark=True,
    # className="navbar navbar-expand-lg navbar-dark bg-dark",
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
