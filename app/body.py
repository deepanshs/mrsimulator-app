# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import importer
from app import navbar
from app import sidebar
from app.dimension import dimension_body
from app.graph import spectrum_body
from app.modal.about import about_modal

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


sub_body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.Br(), spectrum_body], xs=12, sm=12, md=12, lg=7, xl=7),
                dbc.Col([html.Br(), dimension_body], xs=12, sm=12, md=12, lg=5, xl=5),
            ]
        ),
        # memory for holding the isotopomers data
        dcc.Store(id="local-isotopomers-data", storage_type="memory"),
        # memory for holding the exp data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for holding the computationally expensive computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the dimension data
        dcc.Store(id="local-dimension-data", storage_type="memory"),
        # dcc.Store(id="local-dimension-max-index", storage_type="memory"),
    ]
)

body = dbc.Row(
    [
        dbc.Col(sidebar.sidebar, xs=12, sm=12, md=12, lg=12, xl=3),
        dbc.Col(
            [html.Div(sub_body), html.Div(id="isotopomer_computed_log")],
            xs=12,
            sm=12,
            md=12,
            lg=12,
            xl=9,
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
