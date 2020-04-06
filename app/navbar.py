# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from .app import app
from .app import year


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


def place_icon_and_label(icon, label):
    return html.Div(
        [html.I(className=icon), html.Div(label, className="pl-2")],
        className="icon-label",
    )


# documentation link
documentation = html.A(
    place_icon_and_label("fas fa-book-open", "Documentation"),
    href="https://mrsimulator.readthedocs.io/en/stable/",
    className="nav-link",
    target="_blank",
)

# github project link
github_link = html.A(
    place_icon_and_label("fab fa-github", "Github"),
    href="https://github.com/DeepanshS/mrsimulator",
    className="nav-link",
    target="_blank",
)

# about us page-link
about_us = html.Div(
    dbc.Button(
        place_icon_and_label("fas fa-user-cog", "About"),
        id="about_button",
        style={"backgroundColor": "transparent", "border": "none"},
        className="nav-link icon-label",
    ),
    className="nav-link",
)


# secondary navbar ================================================================== #
# The load isotopomer button activates the isotopomer collapsible menu.
import_isotopomer_button = html.Button(
    html.Div(
        [
            html.I(className="fac fa-isotopomers fa-lg"),
            html.Div("Isotopomers", className="hide-label-sm pl-3"),
        ],
        className="secondary-nav-link",
    ),
    id="import-isotopomer-toggler",
    className="flex-fill",
)

# The load spectrum button activates the spectrum collapsible menu.
import_spectrum_button = html.Button(
    html.Div(
        [
            html.I(className="fac fa-spectrum fa-lg"),
            html.Div("Spectrum", className="hide-label-sm pl-3"),
        ],
        className="secondary-nav-link",
    ),
    id="import-spectrum-toggler",
    style=None,
    className="flex-fill",
)

# pack the buttons from secondary navbar in a div
import_options = html.Div(
    [import_isotopomer_button, import_spectrum_button],
    id="import-navbar",
    className="d-flex top-navbar",
)


# The navgation bar displayed on the top of the web app.
navbar = dbc.Navbar(
    [
        html.Div(
            [
                dbc.NavbarBrand(
                    html.Img(
                        src="/assets/mrsimulator-logo-dark.svg",
                        height="80px",
                        alt="Mrsimulator",
                    )
                ),
                html.Div(
                    id="burger",
                    className="burger",
                    children=[
                        html.Div(className="line1"),
                        html.Div(className="line2"),
                        html.Div(className="line3"),
                    ],
                ),
            ],
            className="nav-burger",
        ),
        html.Div(
            [
                dbc.Collapse(
                    [documentation, github_link, about_us],
                    id="navbar-collapse",
                    navbar=True,
                ),
                import_options,
            ],
            className="nav-composite",
        ),
    ],
    color=None,
    # sticky="top",
    # fixed="top",
    dark=None,
    expand="sm",
    # className="flex-fill align-item-right",
)

navbar_group = html.Div(
    [navbar, html.Div(className="color-gradient")], id="navbar-group"
)


@app.callback(
    [Output("navbar-collapse", "is_open"), Output("burger", "className")],
    [Input("burger", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n is None:
        raise PreventUpdate
    if is_open:
        return [not is_open, "burger"]
    return [not is_open, "burger toggle"]


# The navgation bar displayed at the bottom of the web app.
navbar_bottom = dbc.Navbar(
    html.Div([dbc.Label(f"@mrsimulator, 2018-{year}", color="light")]),
    color=None,
    # fixed="bottom",
    # sticky="bottom",
    dark=None,
    className="bottom-navbar",
    id="mrsimulator-bottom",
)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="initialize"),
    Output("temp1", "children"),
    [Input("mrsimulator-bottom", "children")],
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
