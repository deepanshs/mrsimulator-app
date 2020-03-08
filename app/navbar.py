# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.app import year


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


def place_icon_and_label(icon, label):
    return html.Div(
        [html.I(className=icon), html.Div(label, className="pl-2")],  # hide-label-sm
        className="d-flex align-items-center",
    )


documentation = html.A(
    place_icon_and_label("fas fa-book-open", "Documentation"),
    href="https://mrsimulator.readthedocs.io/en/stable/",
    className="navbar-dark nav-link",
    target="_blank",
)

github_link = html.A(
    place_icon_and_label("fab fa-github", "Github"),
    href="https://github.com/DeepanshS/mrsimulator",
    className="navbar-dark nav-link",
    target="_blank",
)

about_us = dbc.Button(
    place_icon_and_label("fas fa-user-cog", "About"),
    color="link",
    id="about_button",
    className="navbar-dark nav-link",
)


# The navgation bar displayed on the top of the web app.
navbar_top = dbc.Navbar(
    [
        dbc.NavbarBrand(
            html.Img(
                src="/assets/mrsimulator-logo-dark.svg",
                height="50px",
                alt="Mrsimulator",
                id="mrsimulator-logo",
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
    className="top-navbar",
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
        [dbc.Label(f"@mrsimulator, 2018-{year}", color="light")],
        id="bottom-navbar-content",
    ),
    color="dark",
    sticky="bottom",
    dark=True,
    id="bottom-navbar",
)


# secondary navbar ================================================================== #
# The load isotopomer button activates the isotopomer collapsible menu.
import_isotopomer_button = dbc.Button(
    html.Div(
        [
            html.I(className="fac fa-isotopomers fa-lg"),
            html.Div("Isotopomers", className="hide-label-xs pl-3"),
        ],
        className="d-flex align-items-center justify-content-center",
    ),
    color="link",
    id="import-isotopomer-toggler",
    className="flex-fill secondary-nav-link",
)

# The load spectrum button activates the spectrum collapsible menu.
import_spectrum_button = dbc.Button(
    html.Div(
        [
            html.I(className="fac fa-spectrum"),
            html.Div("Spectrum", className="hide-label-xs pl-3"),
        ],
        className="d-flex align-items-center justify-content-center",
    ),
    color="link",
    id="import-spectrum-toggler",
    className="flex-fill secondary-nav-link",
)

# pack the buttons from secondary navbar in a div
import_options = html.Div(
    [import_isotopomer_button, import_spectrum_button],
    id="import-navbar",
    className="d-flex top-navbar",
)


@app.callback(
    [
        Output("upload-isotopomer-master-collapse", "is_open"),
        Output("upload-spectrum-master-collapse", "is_open"),
    ],
    [
        Input("import-isotopomer-toggler", "n_clicks"),
        Input("import-spectrum-toggler", "n_clicks"),
        Input("upload-isotopomer-panel-hide-button", "n_clicks"),
        Input("upload-spectrum-panel-hide-button", "n_clicks"),
    ],
    [
        State("upload-isotopomer-master-collapse", "is_open"),
        State("upload-spectrum-master-collapse", "is_open"),
    ],
)
def toggle_import_file_collapse(n1, n2, n4, n5, c1, c2):
    """callback to toggle collapse import and example widgets with their
    respective buttons."""
    if n1 is n2 is n4 is n5 is None:
        raise PreventUpdate

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id in [
        "import-isotopomer-toggler",
        "upload-isotopomer-panel-hide-button",
    ]:
        return [not c1, False]
    if button_id in ["import-spectrum-toggler", "upload-spectrum-panel-hide-button"]:
        return [False, not c2]
    return [False, False]
