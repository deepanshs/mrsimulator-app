# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .toolbar import toolbar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


spectrum_body = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(
                        html.H4(
                            "Spectrum", style={"padding-top": 12, "padding-left": 10}
                        )
                    ),
                    toolbar,
                ]
            )
        ),
        dbc.CardBody(dcc.Graph(id="nmr_spectrum", figure={"data": []})),
    ],
    className="v-100",
    id="spectrum_card",
)
