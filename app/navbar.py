# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# side panel with documentation and github information.
# side_panel = html.Div(
#     [
#         html.Div(
#             id="info-sidepanel",
#             style={},
#             className="sidepanel",
#             children=[
#                 dbc.Button(
#                     html.I(className="fas fa-times"),
#                     id="toggle-sidepanel-hide",
#                     className="close-btn",
#                 ),
#                 html.A(
#                     [html.I(className="fas fa-book"), " Documentation"],
#                     href="https://mrsimulator.readthedocs.io/en/stable/",
#                 ),
#                 html.A(
#                     [html.I(className="fab fa-github"), " Github"],
#                     href="https://github.com/DeepanshS/mrsimulator",
#                 ),
#             ],
#         )
#     ]
# )


# @app.callback(
#     Output("info-sidepanel", "style"),
#     [
#         Input("toggle-sidepanel-show", "n_clicks"),
#         Input("toggle-sidepanel-hide", "n_clicks"),
#     ],
#     [State("info-sidepanel", "style")],
# )
# def callback_sidepanel(n1, n2, style):
#     """Show hide the side-panel"""
#     if n1 == n2 is None:
#         style["width"] = "0px"
#         return style
#     max_ = max(i for i in [n1, n2] if i is not None)
#     if max_ == n1:
#         style["width"] = "250px"
#     if max_ == n2:
#         style = {"width": "0px"}
#     return style


documentation = dbc.NavLink(
    [html.I(className="fas fa-book"), " ", "Documentation"],
    href="https://mrsimulator.readthedocs.io/en/stable/",
    external_link=True,
    className="navbar-dark",
)

github_link = dbc.NavLink(
    [html.I(className="fab fa-github"), " Github"],
    href="https://github.com/DeepanshS/mrsimulator",
    external_link=True,
    className="navbar-dark",
)

about_us = dbc.Button(
    "About", color="link", id="about_button", className="navbar-dark nav-link"
)


# The navgation bar displayed on the top of the web app.
navbar_top = dbc.Navbar(
    [
        dbc.NavbarBrand(
            html.Img(
                src="/assets/mrsimulator-dark-featured.png",
                height="50px",
                alt="Mrsimulator",
            )
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            [documentation, github_link, about_us], id="navbar-collapse", navbar=True
        ),
    ],
    color="dark",
    sticky="top",
    fixed="top",
    dark=True,
    expand="sm",
    id="top-navbar",
    className="drawer-card",
)


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# The navgation bar displayed at the bottom of the web app.
navbar_bottom = dbc.Navbar(
    html.Div(
        [dbc.Label("mrsimulator 2018-2019", color="light")], id="bottom-navbar-content"
    ),
    color="dark",
    sticky="bottom",
    dark=True,
    id="bottom-navbar",
)


# secondary navbar ================================================================== #
# The load isotopomer button activates the isotopomer collapsible menu.
import_isotopomer_button = dbc.Button(
    "Isotopomers",
    color="link",
    id="import-isotopomer-toggler",
    className="flex-fill secondary-nav-link",
)

# The load spectrum button activates the spectrum collapsible menu.
import_spectrum_button = dbc.Button(
    "Spectrum",
    color="link",
    id="import-spectrum-toggler",
    className="flex-fill secondary-nav-link",
)

# The show example button activates the collapsible example menu.
show_example_button = dbc.Button(
    "Examples",
    color="link",
    id="example-file-toggler",
    className="flex-fill secondary-nav-link",
)


@app.callback(
    [
        Output("upload-isotopomer-master-collapse", "is_open"),
        Output("upload-spectrum-master-collapse", "is_open"),
        Output("example-drawer-collapse", "is_open"),
    ],
    [
        Input("import-isotopomer-toggler", "n_clicks_timestamp"),
        Input("import-spectrum-toggler", "n_clicks_timestamp"),
        Input("example-file-toggler", "n_clicks_timestamp"),
        Input("upload-isotopomer-panel-hide-button", "n_clicks_timestamp"),
        Input("upload-spectrum-panel-hide-button", "n_clicks_timestamp"),
        Input("example-panel-hide-button", "n_clicks_timestamp"),
    ],
    [
        State("upload-isotopomer-master-collapse", "is_open"),
        State("upload-spectrum-master-collapse", "is_open"),
        State("example-drawer-collapse", "is_open"),
    ],
)
def toggle_import_file_collapse(n1, n2, n3, n4, n5, n6, c1, c2, c3):
    """callback to toggle collapse import and example widgets with their
    respective buttons."""
    if n1 == n2 == n3 == n4 == n5 == n6 is None:
        raise PreventUpdate
    max_ = max(i for i in [n1, n2, n3, n4, n5, n6] if i is not None)
    if max_ == n1 or max_ == n4:
        return [not c1, False, False]
    if max_ == n2 or max_ == n5:
        return [False, not c2, False]
    if max_ == n3 or max_ == n6:
        return [False, False, not c3]
    return [False, False, False]


import_options = html.Div(
    [import_isotopomer_button, import_spectrum_button, show_example_button],
    id="import-navbar",
    className="d-flex drawer-card",
)
