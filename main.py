# -*- coding: utf-8 -*-
import sys

import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app
from app.inv import mrinv
from app.root import root_app
from app.sims import mrsimulator_app

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

server = app.server


@app.callback(
    [Output("page-content", "children"), Output("url-search", "href")],
    [Input("url", "pathname")],
    [State("url", "search")],
)
def display_page(pathname, search):
    print("pathname", pathname, search)
    if pathname == "/simulator":
        return [mrsimulator_app, search]
    if pathname == "/inversion":
        return [mrinv, search]
    return [root_app, ""]


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
