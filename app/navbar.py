# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from . import __version__
from .app import year
from .menubar import master_menubar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# The navgation bar displayed on the top of the web app.
navbar = dbc.Navbar(
    [
        html.Div(
            [
                dbc.NavbarBrand(
                    [
                        dcc.Link(
                            html.Img(
                                src="/assets/mrsimulator-logo-dark.svg",
                                height="50px",
                                alt="Mrsimulator",
                            ),
                            href="/",
                        ),
                        html.Div(f"{__version__}", className="logo-version"),
                    ]
                ),
                # html.Div(
                #     id="burger",
                #     className="burger",
                #     children=[
                #         html.Div(className="line1"),
                #         html.Div(className="line2"),
                #         html.Div(className="line3"),
                #     ],
                # ),
            ],
            className="nav-burger",
        ),
        html.Div(master_menubar, className="nav-composite"),
    ],
    color=None,
    # sticky="top",
    # fixed="top",
    dark=None,
    expand="md",
)

navbar_group = html.Div(navbar)


# @app.callback(
#     [Output("navbar-collapse", "is_open"), Output("burger", "className")],
#     [Input("burger", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n is None:
#         raise PreventUpdate
#     if is_open:
#         return [not is_open, "burger"]
#     return [not is_open, "burger toggle"]


# The navgation bar displayed at the bottom of the web app.
navbar_bottom = dbc.Navbar(
    html.Div([dbc.Label(f"@mrsimulator, 2019-{year}", color="light")]),
    color=None,
    # fixed="bottom",
    # sticky="bottom",
    dark=None,
    className="bottom-navbar",
)
