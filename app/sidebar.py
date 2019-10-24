# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .app import app


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


colors = {"background": "#e2e2e2", "text": "#585858"}

filename_datetime = html.Div(
    [
        html.H5(id="filename_dataset"),
        html.H6(
            id="data_description", style={"textAlign": "left", "color": colors["text"]}
        ),
    ]
)

with open("example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)

dropdown_menu_items = [
    dbc.DropdownMenuItem("Examples", id="dropdown-example-item"),
    dbc.DropdownMenuItem("URL", id="dropdown-URL-item"),
]

input_box = [
    dbc.DropdownMenu(dropdown_menu_items, label="input_type", addon_type="prepend"),
    dbc.Input(id="input-group-dropdown-input", placeholder="name"),
]

examples_dropdown = dcc.Dropdown(
    id=f"mrsim-examples",
    options=mrsimulator_examples,
    value=None,
    searchable=False,
    clearable=False,
)

sample_url = dbc.InputGroup(
    [
        dbc.InputGroupAddon("URL", addon_type="prepend"),
        dbc.Input(id=f"sample-url", value=None, placeholder="Paste URL"),
        dbc.Button("Submit", id=f"sample-url-submit"),
    ]
)

# dbc.Col([html.Br(), spectrum_body], xs=12, sm=12, md=12, lg=7, xl=7),

upload_data = [
    dbc.Col(
        [
            dcc.Upload(
                id="upload_data",
                children=html.Div(
                    [
                        "Drag and drop, or ",
                        html.A(
                            [html.I(className="fas fa-upload"), " select"], href="#"
                        ),
                    ]
                ),
                style={
                    "lineHeight": "80px",
                    "borderWidth": "0.75px",
                    "borderStyle": "dashed",
                    "borderRadius": "7px",
                    "textAlign": "center",
                },
                # Allow multiple files to be uploaded
                multiple=False,
                className="control-upload",
            ),
            dbc.FormText(id="error_message"),
        ],
        xs=12,
        sm=12,
        md=6,
        lg=6,
        xl=12,
    ),
    dbc.Col([examples_dropdown, dbc.FormText("Or select an example")]),
]

upload_data_collapsible = dbc.Navbar(
    [
        dbc.NavbarToggler(id="upload-data-toggler"),
        dbc.Collapse(upload_data, id="upload-data-collapse", navbar=True),
    ],
    expand="md",
    light=True,
    # fixed="top",
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("upload-data-collapse", "is_open"),
    [Input("upload-data-toggler", "n_clicks")],
    [State("upload-data-collapse", "is_open")],
)
def upload_data_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


input_file = [upload_data_collapsible, html.Hr(), filename_datetime]

sidebar = dbc.Card(
    dbc.CardBody(html.Div(input_file)), className="h-100 my-card-sidebar", inverse=False
)
