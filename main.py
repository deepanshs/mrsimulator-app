# -*- coding: utf-8 -*-
import sys

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app
from app.inv import mrinv
from app.sims import mrsimulator_app

# from app_main import home_mrsims

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]


html_body = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # html.Div(id="placeholder"),
        html.A(id="url-search", href=""),
    ],
    className="main",
)

app.layout = html_body

server = app.server

home = html.Div(
    [
        dcc.Link("Simulator", href="/simulator", id="simulator-app"),
        dcc.Link("Inversion", href="/inversion", id="inversion-app"),
        # dcc.Link("Home", href="/home", id="home-app"),
    ],
    className="home-page",
    # **{"data-app-link": ""},
)

layout_2 = mrinv
# layout_3 = home_mrsims

counter = 0


@app.callback(
    [Output("page-content", "children"), Output("url-search", "href")],
    [Input("url", "pathname")],
    [State("url", "search")],
)
def display_page(pathname, search):
    print("pathname", pathname, search)
    global counter
    print("counter", counter)
    if search == "" and counter != 0:
        counter = 1
        return [no_update, search]
    if pathname == "/simulator":
        return [mrsimulator_app, search]
    if pathname == "/inversion":
        return [layout_2, search]
    # if pathname == "/home":
    #     return [layout_3, search]
    # else:
    return [home, ""]


# app.clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="initialize"),
#     Output("placeholder", "children"),
#     [Input("simulator-app", "n_clicks")],
#     prevent_initial_call=True,
# )


if __name__ == "__main__":
    host = "127.0.0.1"
    is_host = ["--host" in arg for arg in sys.argv]
    if any(is_host):
        host_index = np.where(np.asarray(is_host))[0][0]
        host = sys.argv[host_index].split("=")[1]

    port = 8050
    is_port = ["--port" in arg for arg in sys.argv]
    if any(is_port):
        port_index = np.where(np.asarray(is_port))[0][0]
        port = int(sys.argv[port_index].split("=")[1])

    debug = False
    is_debug = ["--debug" in arg for arg in sys.argv]
    if any(is_debug):
        debug_index = np.where(np.asarray(is_debug))[0][0]
        debug = True if sys.argv[debug_index].split("=")[1] == "True" else False

    app.run_server(host=host, port=port, debug=debug, use_reloader=False)
