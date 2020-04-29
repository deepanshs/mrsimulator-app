# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from . import importer
from . import navbar
from .custom_widgets import custom_button
from .dimension import dimension_body
from .graph import spectrum_body
from .isotopomer import isotopomer_body
from .modal.about import about_modal
from .sidebar import master_toolbar
from .sidebar import sample_info

# from . import sidebar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# The dimension and isotopomer cards are place at the front and back of a master
# card
# card_flip = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dimension_body, className="card-face", sm=6, md=12, lg=12, xl=6
#                 ),
#                 dbc.Col(
#                     isotopomer_body,
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
#     id="interface-dimension-isotopomer",
# )


# @app.callback(
#     [
#         Output("card-flip", "className"),
#         Output("dimension-card-body", "className"),
#         Output("isotopomer-card-body", "className"),
#     ],
#     [
#         Input("dimension-card-title", "n_clicks"),
#         Input("isotopomer-card-title", "n_clicks"),
#     ],
# )
# def flip(n1, n2):
#     """Flips the card between the isotopomer and dimension cards."""
#     if n1 is None and n2 is None:
#         raise PreventUpdate
#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if trigger_id == "isotopomer-card-title":
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
#     [dbc.Col(isotopomer_body), dbc.Col(dimension_body)], className="col-left",
# )
# slide3 = html.Section([help_line, spectrum_body], className="col-right")

# storage data
storage_div = html.Div(
    [
        # memory for holding the isotopomers data
        dcc.Store(id="local-isotopomers-data", storage_type="session"),
        dcc.Store(id="local-simulator-data", storage_type="session"),
        # memory for holding the exp data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for holding the computationally expensive computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the dimension data
        dcc.Store(id="local-method-data", storage_type="memory"),
        # a mapping of isotopomer index to local isotopomer index
        dcc.Store(id="local-isotopomer-index-map", storage_type="memory"),
        # dcc.Store(id="local-dimension-max-index", storage_type="memory"),
        dcc.Store(id="new-json", storage_type="memory"),
        dcc.Store(id="temp-json", storage_type="memory"),
        dcc.Store(id="new-method-json", storage_type="memory"),
        # store a bool indicating if the data is from an external file
        dcc.Store(id="config", storage_type="memory"),
    ]
)

nav_group = html.Div(
    [
        navbar.navbar_group,
        about_modal,
        # navbar.side_panel,
        html.Div(
            [importer.isotopomer_import_layout, importer.spectrum_import_layout],
            id="drawers-import",
        ),
        dbc.Alert(
            id="alert-message-isotopomer",
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
        master_toolbar,
        sample_info,
    ],
    # className="fixed-top",
)

sidebar = html.Div(
    [
        custom_button(
            icon_classname="fac fa-isotopomers",
            id="view-isotopomers",
            tooltip="View isotopomers",
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

app_1 = html.Div(
    [
        html.Div(id="temp1"),
        html.Div(id="temp2"),
        html.Div(id="temp3"),
        html.Div(id="temp4"),
        dbc.Row(
            [
                dbc.Col([isotopomer_body, dimension_body], md=12, lg=6),
                dbc.Col(spectrum_body, md=12, lg=6),
            ]
        ),
        storage_div,
        navbar.navbar_bottom,
    ],
    className="app-1",
)
