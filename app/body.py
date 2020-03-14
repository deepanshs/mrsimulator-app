# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import importer
from app import navbar
from app import sidebar
from app.dimension import dimension_body
from app.graph import spectrum_body
from app.isotopomer import isotopomer_body
from app.modal.about import about_modal

# import dash

# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.exceptions import PreventUpdate

# from app.app import app

# from app.isotopomer import isotopomer_body_card
# from app.dimension import dimension_body_card

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# The dimension and isotopomer cards are place at the front and back of a master
# card
# card_flip = html.Div(
#     dbc.Row(
#         [
#             dbc.Col(isotopomer_body_card, className="card-face card-face-back", xl=6),
#             dbc.Col(dimension_body_card, className="card-face", xl=6),
#         ],
#         id="card-flip",
#         className="card-3D",
#     ),
#     className="scene",
# )


# @app.callback(
#     [
#         Output("card-flip", "className"),
#         Output("dimension-body-card", "className"),
#         Output("isotopomer-body-card", "className"),
#     ],
#     [Input("dimension-card", "n_clicks"), Input("isotopomer-card", "n_clicks")],
# )
# def flip(n1, n2):
#     """Flips the card between the isotopomer and dimension cards."""
#     if n1 is None and n2 is None:
#         raise PreventUpdate
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if trigger_id == "dimension-card":
#         return [
#             "card-3D card-3D-is-flipped",
#             "card-flip-hide",
#             "card-flip-show",
#         ]

#     if trigger_id == "isotopomer-card":
#         return ["card-3D", "card-flip-show", "card-flip-hide"]


sub_body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.Br(), isotopomer_body], xs=12, sm=12, md=12, lg=3, xl=3),
                dbc.Col([html.Br(), spectrum_body], xs=12, sm=12, md=12, lg=6, xl=6),
                dbc.Col([html.Br(), dimension_body], xs=12, sm=12, md=12, lg=3, xl=3),
                # dbc.Col([html.Br(), spectrum_body], xs=12, sm=12, md=12, lg=7, xl=5),
                # dbc.Col([html.Br(), card_flip], xs=12, sm=12, md=12, lg=5, xl=7),
            ]
        ),
        # memory for holding the isotopomers data
        dcc.Store(id="local-isotopomers-data", storage_type="memory"),
        # memory for old local isotopomers data
        dcc.Store(id="old-local-isotopomers-data", storage_type="memory"),
        # memory for holding the exp data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for holding the computationally expensive computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the dimension data
        dcc.Store(id="local-dimension-data", storage_type="memory"),
        # a mapping of isotopomer index to local isotopomer index
        dcc.Store(id="local-isotopomer-index-map", storage_type="memory"),
        # dcc.Store(id="local-dimension-max-index", storage_type="memory"),
        dcc.Store(id="new-json", storage_type="memory"),
    ]
)

body = dbc.Row(
    [
        dbc.Col(sidebar.sidebar, xs=12, sm=12, md=12, lg=12, xl=12),
        dbc.Col(
            [html.Div(sub_body), html.Div(id="isotopomer_computed_log")],
            xs=12,
            sm=12,
            md=12,
            lg=12,
            xl=12,
        ),
    ]
)

app_1 = dbc.Container(
    [
        navbar.navbar_top,
        navbar.import_options,
        html.Div(id="buffer", className="buffer"),
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
        html.Div(body),
        about_modal,
        # dcc.Location(id="download-csdm-file", refresh=True),
        # dcc.Location(id="download-csv-file", refresh=True),
        # test,
        # dbc.Jumbotron(),
        navbar.navbar_bottom,
    ],
    fluid=True,
    className="master-padding",
)
