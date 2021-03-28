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

from app import app


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


list_ = []
for item in about_.keys():
    print(item)
    list_.append(
        dbc.Modal(
            [dbc.ModalHeader(item), dbc.ModalBody(get_contents(about_[item]))],
            size="lg",
            id=f"modal-{item}",
            role="document",
            className="modal-dialog",
        )
    )

    app.clientside_callback(
        """
        function (value) {
            if (value == null) {
                throw window.dash_clientside.PreventUpdate;
            }
            return 'true';
        }
        """,
        Output(f"modal-{item}", "is_open"),
        [Input(f"modal-{item}-button", "n_clicks")],
        prevent_initial_call=True,
    )

about_modals = html.Div(list_)
