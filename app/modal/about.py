# -*- coding: utf-8 -*-
"""
    Model page with tabs containing
    - App description
    - How to report issues
    - About contributors.
"""
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.exceptions import PreventUpdate

from app.app import app
from app.app import year


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


PATH = "config/"

# Get info from JSON file.
with open(PATH + "about.json", "r") as f:
    content = json.load(f)

about_ = content["about"]

div = []


def get_contents(content):
    div = []
    if isinstance(content, list):
        lst1 = []
        for list_item in content:
            lst1.append(html.Li(list_item))
        div.append(html.Ul(lst1))
    elif isinstance(content, dict):
        sub_div = []
        for item in content.keys():
            div_ = []
            div_.append(html.H6(item))
            div_.append(html.Div(get_contents(content[item])))
            sub_div.append(dbc.Col(div_, xs=12, sm=12, md=12, lg=6, xl=6))
        div.append(dbc.Row(sub_div))
    else:
        div.append(dcc.Markdown(content))
    return div


def create_tab(title, content):
    return dbc.Tab(dbc.Card(dbc.CardBody(get_contents(content))), label=title)


tabs_list = []
for item in about_.keys():
    tabs_list.append(create_tab(item, about_[item]))

tabs = dbc.Tabs(tabs_list)

# Layout ----------------------------------------------------------------------
about_modal = dbc.Modal(
    [dbc.ModalHeader(f"Mrsimulator-app 2018-{year}"), dbc.ModalBody(tabs)],
    size="lg",
    id="modal_about",
    role="document",
    className="modal-dialog",
)


@app.callback(Output("modal_about", "is_open"), [Input("about_button", "n_clicks")])
def toggle_modal_about(n):
    """Model window for advance input."""
    if n is None:
        raise PreventUpdate
    return True
