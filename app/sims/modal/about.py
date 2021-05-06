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
from mrsimulator import __version__ as mrsim_version

from app import __version__ as mrapp_version
from app import app

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


PATH = "config/"

# Get info from JSON file.
with open(PATH + "about.json", "r") as f:
    content = json.load(f)

about_ = content["about"]
ABOUT_CONTENT = (
    "Mrsimulator web-app is a plotly-dash user interface to the mrsimulator package "
    "designed for fast and easy solid-state NMR spectrum simulation. Both projects "
    "are open-source and maintained by the community. If you would like to contribute "
    "to the project, fork our Github repositories and start contributing."
)
LINK_MRSIMULATOR_LIB = "https://github.com/DeepanshS/mrsimulator"
LINK_MRSIMULATOR_APP = "https://github.com/DeepanshS/mrsimulator-app"


def about():
    title = dbc.ModalHeader("About")

    def make_row_element(name, link=None, version="", element="td"):
        link = html.A(name, href=link, target="blank_") if link is not None else name
        if element == "td":
            contents = [
                html.Td(item) if element == "td" else html.Th(item)
                for item in [link, version]
            ]

        return html.Thead(html.Tr(contents))

    table = html.Table(
        [
            make_row_element(html.B("Projects"), None, html.B("Version")),
            make_row_element("Mrsimulator", LINK_MRSIMULATOR_LIB, mrsim_version),
            make_row_element("Mrsimulator-App", LINK_MRSIMULATOR_APP, mrapp_version),
        ]
    )

    content = [ABOUT_CONTENT, table]
    modal = dbc.Modal(
        [title, dbc.ModalBody(content)],
        size="lg",
        id="modal-about",
        role="document",
        className="modal-dialog",
    )

    app.clientside_callback(
        """function (value) {
            if (value == null) throw window.dash_clientside.PreventUpdate;
            return 'true';
        }""",
        Output("modal-about", "is_open"),
        [Input("modal-about-button", "n_clicks")],
        prevent_initial_call=True,
    )
    return modal


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

about_modals = html.Div([*list_, about()])
