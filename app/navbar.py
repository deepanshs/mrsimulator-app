# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from .app import year
from .menubar import master_menubar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# secondary navbar ================================================================== #
# The load isotopomer button activates the isotopomer collapsible menu.
# import_isotopomer_button = html.Button(
#     html.Div(
#         [
#             html.I(className="fac fa-isotopomers fa-lg"),
#             html.Div("Isotopomers", className="hide-label-sm pl-3"),
#         ],
#         className="secondary-nav-link",
#     ),
#     id="import-isotopomer-toggler",
#     className="flex-fill",
# )

# # The load spectrum button activates the spectrum collapsible menu.
# import_spectrum_button = html.Button(
#     html.Div(
#         [
#             html.I(className="fac fa-spectrum fa-lg"),
#             html.Div("Spectrum", className="hide-label-sm pl-3"),
#         ],
#         className="secondary-nav-link",
#     ),
#     id="import-spectrum-toggler",
#     style=None,
#     className="flex-fill",
# )

# # pack the buttons from secondary navbar in a div
# import_options = html.Div(
#     [import_isotopomer_button, import_spectrum_button],
#     id="import-navbar",
#     className="d-flex top-navbar",
# )


# The navgation bar displayed on the top of the web app.
navbar = dbc.Navbar(
    [
        html.Div(
            [
                dbc.NavbarBrand(
                    html.Img(
                        src="/assets/mrsimulator-logo-dark.svg",
                        height="50rem",
                        alt="Mrsimulator",
                    )
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
