# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.dimension import dimension_body
from app.graph import spectrum_body

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


colors = {"background": "#e2e2e2", "text": "#585858"}

main_body = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.Br(), spectrum_body], xs=12, sm=12, md=12, lg=7, xl=7),
                dbc.Col([html.Br(), dimension_body], xs=12, sm=12, md=12, lg=5, xl=5),
            ]
        ),
        dcc.Store(id="local-metadata", storage_type="memory"),
        dcc.Store(id="local-csdm-data", storage_type="memory"),
        dcc.Store(id="local-computed-data", storage_type="memory"),
    ]
)
