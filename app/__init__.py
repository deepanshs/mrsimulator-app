# -*- coding: utf-8 -*-
import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash

from .head import head_config

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__version__ = "v0.3.0"

now = datetime.datetime.now()
year = now.year

# Initialize dash app
app = Dash(
    __name__,
    title="Mrsimulator",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    **head_config,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # html.Div(id="placeholder"),
        html.A(id="url-search", href=""),
    ],
    className="main",
)


# root = html.Div(
#     [
#         dcc.Link("Simulator", href="/simulator", id="simulator-app"),
#         dcc.Link("Inversion", href="/inversion", id="inversion-app"),
#         # dcc.Link("Home", href="/home", id="home-app"),
#     ],
#     className="home-page",
#     # **{"data-app-link": ""},
# )


# # counter = 0


# @app.callback(
#     [Output("page-content", "children"), Output("url-search", "href")],
#     [Input("url", "pathname")],
#     [State("url", "search")],
# )
# def display_page(pathname, search):
#     print("pathname", pathname, search)
#     # global counter
#     # print("counter", counter)
#     # if search == "" and counter != 0:
#     # counter = 1
#     # return [no_update, search]
#     if pathname == "/simulator":
#         return [mrsimulator_app, search]
#     if pathname == "/inversion":
#         return [mrinv, search]
#     return [root, ""]


# # app.clientside_callback(
# #     ClientsideFunction(namespace="clientside", function_name="initialize"),
# #     Output("placeholder", "children"),
# #     [Input("simulator-app", "n_clicks")],
# #     prevent_initial_call=True,
# # )
