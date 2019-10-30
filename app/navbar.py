# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from .app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

import_isotopomer_button = dbc.DropdownMenuItem(
    "Isotopomers",
    id="import-isotopomer-toggler",
    # className="nav-dropdownmen-item"
)

import_spectrum_button = dbc.DropdownMenuItem(
    "Spectrum",
    id="import-spectrum-toggler",
    # className="nav-dropdownmen-item"
)


import_menu = dbc.DropdownMenu(
    [import_isotopomer_button, import_spectrum_button],
    label="Import",
    # in_navbar=True,
    nav=True,
    # className="navbar-dark",
)

# The import button activates the collapsible import menu.
# import_button = dbc.Button(
#     "Import", color="link", id="import-file-toggler", className="navbar-dark nav-link"
# )

# The show example button activates the collapsible example menu.
show_example_button = dbc.NavItem(
    dbc.Button(
        "Examples",
        color="link",
        id="example-file-toggler",
        className="navbar-dark nav-link",
    ),
    key="ul",
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


# side panel with documentation and github information.
side_panel = html.Div(
    [
        html.Div(
            id="info-sidepanel",
            style={},
            className="sidepanel",
            children=[
                dbc.Button(
                    html.I(className="fas fa-times"),
                    id="toggle-sidepanel-hide",
                    className="close-btn",
                ),
                html.A(
                    [html.I(className="fas fa-book"), " Documentation"],
                    href="https://mrsimulator.readthedocs.io/en/stable/",
                ),
                html.A(
                    [html.I(className="fab fa-github"), " Github"],
                    href="https://github.com/DeepanshS/mrsimulator",
                ),
            ],
        )
    ]
)


@app.callback(
    Output("info-sidepanel", "style"),
    [
        Input("toggle-sidepanel-show", "n_clicks"),
        Input("toggle-sidepanel-hide", "n_clicks"),
    ],
    [State("info-sidepanel", "style")],
)
def callback_sidepanel(n1, n2, style):
    """Show hide the side-panel"""
    if n1 == n2 is None:
        style["width"] = "0px"
        return style
    max_ = max(i for i in [n1, n2] if i is not None)
    if max_ == n1:
        style["width"] = "250px"
    if max_ == n2:
        style = {"width": "0px"}
    return style


# layout for side-panel togglee and brand logo
toggler_and_brand_logo_layout = dbc.Nav(
    [
        dbc.NavbarBrand(
            [
                dbc.Button(
                    html.I(className="fas fa-bars"),
                    id="toggle-sidepanel-show",
                    className="open-btn",
                ),
                html.Img(
                    src="/assets/mrsimulator-dark-featured.png",
                    height="50px",
                    alt="Mrsimulator",
                ),
                # html.H5(
                #     "A plotly-dash app",
                #     style={"color": "white", "float": "center", "font-size": 10},
                # ),
            ]
        ),
        # import_menu,
        dbc.Row([dbc.Col(import_menu), dbc.Col(show_example_button)]),
    ],
    navbar=True,
)

# The navgation bar displayed on the top of the web app.
navbar_top = dbc.Navbar(
    toggler_and_brand_logo_layout,
    color="dark",
    sticky="top",
    fixed="top",
    dark=True,
    className="navbar justify-content-start",
    expand="sm",
)

# The navgation bar displayed at the bottom of the web app.
navbar_bottom = dbc.Navbar(
    [dbc.Label("mrsimulator 2018-2019", color="light")],
    color="dark",
    sticky="bottom",
    dark=True,
    className="justify-content-start",
    expand="sm",
)


# @app.callback(
#     Output("navbar-collapse", "is_open"),
#     [Input("navbar-toggler", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     """Callback for toggling the collapse of nav menu items on small screens."""
#     if n:
#         return not is_open
#     return is_open
