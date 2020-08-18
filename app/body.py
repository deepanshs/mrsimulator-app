# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from . import importer
from . import navbar
from .custom_widgets import custom_button
from .graph import spectrum_body
from .info import sample_info
from .nmr_method import dimension_body
from .nmr_method.toolbar import method_edit_tools
from .spin_system import spin_system_body
from .spin_system.toolbar import spin_system_edit_tools


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# The nmr_method and spin-system cards are place at the front and back of a master
# card
# card_flip = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dimension_body, className="card-face", sm=6, md=12, lg=12, xl=6
#                 ),
#                 dbc.Col(
#                     spin_system_body,
#                     className="card-face card-face-back",
#                     sm=6,
#                     md=12,
#                     lg=12,
#                     xl=6,
#                 ),
#             ],
#             id="card-flip",
#             className="card-3D",
#         ),
#         html.Div(className="buffer"),
#     ],
#     className="scene",
#     id="interface-dimension-spin-system",
# )


# @app.callback(
#     [
#         Output("card-flip", "className"),
#         Output("dimension-card-body", "className"),
#         Output("spin-system-card-body", "className"),
#     ],
#     [
#         Input("dimension-card-title", "n_clicks"),
#         Input("spin-system-card-title", "n_clicks"),
#     ],
# )
# def flip(n1, n2):
#     """Flips the card between the spin-system and dimension cards."""
#     if n1 is None and n2 is None:
#         raise PreventUpdate
#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if trigger_id == "spin-system-card-title":
#         return ["card-3D", "card-flip-show", "card-flip-hide"]

#     return ["card-3D card-3D-is-flipped", "card-flip-hide", "card-flip-show"]


# body = dbc.Row(
#     [
#         dbc.Col(spectrum_body, xs=12, sm=12, md=7, lg=7, xl=5, className="col-left"),
#         dbc.Col(card_flip, xs=12, sm=12, md=5, lg=5, xl=7, className="col-right"),
#     ],
#     className="col-grid",
# )

# help_line = html.Div("", id="help-line")
# slide2 = html.Section(
#     [dbc.Col(spin_system_body), dbc.Col(dimension_body)], className="col-left",
# )
# slide3 = html.Section([help_line, spectrum_body], className="col-right")

# storage data
storage_div = html.Div(
    [
        # memory for holding the spin systems data
        dcc.Store(id="local-mrsim-data", storage_type="session"),
        dcc.Store(id="local-simulator-data", storage_type="memory"),
        # memory for holding the exp data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for holding the computationally expensive computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the nmr_method data
        dcc.Store(id="local-method-data", storage_type="memory"),
        # a mapping of spin system index to local spin-system index
        dcc.Store(id="local-spin-system-index-map", storage_type="memory"),
        # dcc.Store(id="local-nmr_method-max-index", storage_type="memory"),
        dcc.Store(id="new-spin-system", storage_type="memory"),
        dcc.Store(id="new-method", storage_type="memory"),
        # store a bool indicating if the data is from an external file
        dcc.Store(id="config", storage_type="memory"),
        # method-template data
        dcc.Store(id="method-from-template", storage_type="memory"),
        dcc.Store(id="user-config", storage_type="local"),
    ]
)

nav_group = html.Div(
    [
        navbar.navbar_group,
        html.Div(
            [importer.spin_system_import_layout, importer.spectrum_import_layout],
            id="drawers-import",
        ),
        dbc.Alert(
            id="alert-message-simulation",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
        dbc.Alert(
            id="alert-message-import",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
        dbc.Alert(
            id="alert-message-spectrum",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
    ]
)

view_tools = html.Div(
    [
        custom_button(
            icon_classname="fas fa-info-circle",
            id="view-info",
            tooltip="Info",
            outline=True,
        ),
        custom_button(
            icon_classname="fac fa-spin-systems",
            id="view-spin-systems",
            tooltip="View spin-systems",
            outline=True,
        ),
        custom_button(
            icon_classname="fas fa-cube",
            id="view-methods",
            tooltip="View methods",
            outline=True,
        ),
    ],
    className="sidebar",
)

sidebar = html.Div(
    [view_tools, method_edit_tools, spin_system_edit_tools], className="sidebar-master"
)

app_1 = html.Div(
    [
        html.Div(id="temp1"),
        html.Div(id="temp2"),
        html.Div(id="temp3"),
        html.Div(id="temp4"),
        html.Div(id="temp5"),
        html.Div(id="temp6"),
        html.A(id="export-simulation-from-method-link", style={"display": "none"}),
        # html.Div(
        #     [
        #         html.Li(html.A("In", href="#info-body")),
        #         html.Li(html.A("Is", href="#spin-system-body")),
        #         html.Li(html.A("Me", href="#method-body")),
        #         html.Li(html.A("Sp", href="#spectrum-body")),
        #     ],
        #     className="nav-token",
        # ),
        html.Div(
            [sample_info, spin_system_body, dimension_body, spectrum_body],
            className="mobile-scroll",
        ),
        storage_div,
        navbar.navbar_bottom,
    ],
    className="app-1",
)
