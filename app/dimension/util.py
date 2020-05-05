# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


def print_methods_info(methods):
    """Return a html for rendering the display in the read-only method section."""
    output = []

    for i, method in enumerate(methods):
        local = []
        local.append(html.B(method["name"], className=""))
        channels = ", ".join(method["channels"])
        local.append(html.Div(["Channel: ", channels], className="pl-2"))

        # local.append(html.Br())

        output.append(
            html.Li(
                [
                    html.H6(i),
                    html.Div(
                        [
                            html.A(local),
                            # dbc.Button(
                            #     "X",
                            #     color="danger",
                            #     block=True,
                            #     id={"type": "initiate-remove-isotopomer", "index": i},
                            # ),
                        ]
                    ),
                ],
                className="list-group-item",
            )
        )

    return html.Div(html.Ul(output, className="list-group"), className="display-form")


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_methods_load"),
    Output("temp4", "children"),
    [Input("method-read-only", "children")],
    [State("config", "data")],
)
