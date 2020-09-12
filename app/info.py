# -*- coding: utf-8 -*-
import math

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_button
from app.spin_system.utils import default_unit
from app.spin_system.utils import label_dictionary

colors = {"background": "#e2e2e2", "text": "#585858"}

default_sample = {"name": "Title", "description": "Sample description"}
# Info ------------------------------------------------------------------------------ #

# button = dbc.Button(id="edit-info-button")
button = custom_button(
    icon_classname="fas fa-pencil-alt",
    tooltip="Edit",
    id="edit-info-button",
    className="icon-button",
    module="html",
)
sample_title = [
    dbc.FormText("Title"),
    dbc.Input(type="text", placeholder="Add title", id="info-name-edit"),
]
sample_description = [
    dbc.FormText("Description"),
    dbc.Textarea(
        value="",
        placeholder="Add description",
        id="info-description-edit",
        style={"height": "12rem"},
    ),
]
modal = dbc.Modal(
    [
        dbc.ModalBody(
            [
                custom_button(
                    icon_classname="fas fa-times 2x",
                    tooltip="Close",
                    id="close_info_modal",
                    className="icon-button",
                    module="html",
                ),
                dbc.FormGroup([*sample_title, *sample_description]),
            ],
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Save",
                id="save_info_modal",
                color="dark",
                className="ml-auto",
                outline=True,
            )
        ),
    ],
    id="info_modal_editor",
    is_open=False,
    role="document",
    className="modal-dialog",
    backdrop="static",
)


@app.callback(
    [
        Output("info_modal_editor", "is_open"),
        Output("info-name-edit", "value"),
        Output("info-description-edit", "value"),
    ],
    [Input("edit-info-button", "n_clicks"), Input("close_info_modal", "n_clicks")],
    [State("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
def open_modal(n1, n2, data):
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "close_info_modal":
        return False, no_update, no_update

    name = default_sample["name"]
    description = default_sample["description"]
    if data is not None:
        name, description = data["name"], data["description"]
    return True, name, description


def attribute_value_pair_(key, value):
    if not isinstance(value, str):
        value = round(value, 10)
    return f"{label_dictionary[key]}={value} {default_unit[key]}, "


def display_spin_system_info_(json_data: dict):
    output = []
    for i, spin_system in enumerate(json_data):
        local = []
        # spin system title and abundance in the first row
        title = html.H6(f"Spin system {i}")
        if "name" in spin_system.keys():
            if spin_system["name"] not in ["", None]:
                title = html.H6(spin_system["name"], className="")

        abundance = (
            "100" if "abundance" not in spin_system else spin_system["abundance"]
        )
        abundance = html.Div(f"Abundance: {abundance} %", className="")
        head = html.Div(
            [title, abundance],
            style={"display": "flex", "justify-content": "space-between"},
            className="card-header",
        )
        # local.append(head)

        # add description to the following lines, if present
        if "description" in spin_system.keys():
            description = spin_system["description"]
            if description not in ["", None] and len(description) > 22:
                description = f"{description[:22]}..."
            local.append(html.Div(description, className=""))

        # per site info
        if "sites" not in spin_system:
            return

        for j, site in enumerate(spin_system["sites"]):
            site_local = []
            site_local.append(html.B(f"Site {j}"))

            for site_attribute, val in site.items():
                if isinstance(val, dict):
                    line = f"{label_dictionary[site_attribute]}: "

                    for key, value in val.items():
                        if value is not None:
                            value = (
                                math.degrees(value)
                                if key in ["alpha", "beta", "gamma"]
                                else value
                            )
                            value = value * 1e-6 if key == "Cq" else value
                            line += attribute_value_pair_(key, value)
                    site_local.append(html.Div(line[:-2], className="sm"))
                else:
                    site_local.append(
                        html.Div(
                            attribute_value_pair_(site_attribute, val)[:-2],
                            className="sm",
                        )
                    )
            local.append(html.Div(site_local))

        output.append(dbc.Card([head, dbc.CardBody(local)], className="my-4"))
    return output


def display_sample_info(json_data):
    title = json_data["name"]
    title = "Sample" if title == "" else title
    description = json_data["description"]
    data = dbc.CardBody(
        [
            html.H5(
                [title, button, modal],
                style={"display": "flex", "justify-content": "space-between"},
            ),
            html.P(description, style={"textAlign": "left", "color": colors["text"]}),
        ],
        className="sample-info-cards",
    )

    spin_sys_cards = []
    if "spin_systems" in json_data:
        spin_sys_cards = display_spin_system_info_(json_data["spin_systems"])

    return html.Div([dbc.Card(data), *spin_sys_cards])


sample_info = html.Div(
    className="my-card",
    children=dcc.Upload(
        html.Div(display_sample_info(default_sample), id="info-read-only"),
        id="upload-spin-system-local",
        disable_click=True,
        multiple=False,
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
        },
    ),
    id="info-body",
)
