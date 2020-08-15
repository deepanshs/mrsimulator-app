# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import ALL
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


def update_method_info(methods):
    """Return a html for rendering the display in the read-only method section."""
    output = []

    for i, method in enumerate(methods):
        local = []
        local.append(html.B(f"Method-{i}", className=""))

        # method name
        name = method["name"]
        name = f"{name[:18]}..." if len(name) > 18 else name
        local.append(html.Div(name, className=""))

        # method channel(s)
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
                            #     id={"type": "initiate-remove-spin-system",
                            #       "index": i},
                            # ),
                        ]
                    ),
                ],
                id={"type": "select-method-index", "index": i},
                className="list-group-item",
            )
        )

    return html.Div(html.Ul(output, className="list-group"), className="display-form")


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_methods_load"),
    Output("temp4", "children"),
    [Input("method-read-only", "children")],
    [State("config", "data")],
    prevent_initial_call=True,
)

app.clientside_callback(
    """
        function(n){
            set_method_index(n)
            return null;
        }
    """,
    Output("temp6", "children"),
    [Input("select-method", "value")],
    prevent_initial_call=True,
)

app.clientside_callback(
    """
        function(n, value){
            let index = get_method_index();
            if (index == value){
                throw window.dash_clientside.PreventUpdate;
            }
            return index;
        }
    """,
    Output("select-method", "value"),
    [Input({"type": "select-method-index", "index": ALL}, "n_clicks")],
    [State("select-method", "value")],
    prevent_initial_call=True,
)
