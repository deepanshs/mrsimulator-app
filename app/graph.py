# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .toolbar import toolbar

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]


spectrum_body = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Row(
                        [dbc.Col(html.H4("Spectrum", className="card-title")), toolbar]
                    )
                ),
                dbc.CardBody(dcc.Graph(id="nmr_spectrum", figure={"data": []})),
            ],
            className="v-100",
        )
    ]
)
