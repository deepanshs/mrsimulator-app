# -*- coding: utf-8 -*-
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


def display_spin_system_info_table(json_data: dict):
    sys_row = []
    sys_items = ["", "Name", "%", "# Sites", "Isotopes", ""]
    sys_row.append(html.Tr([html.Td(html.B(item)) for item in sys_items]))

    if "spin_systems" in json_data:
        icon = html.Span(html.I(className="fas fa-pencil-alt"), **{"data-edit-sys": ""})
        for i, spin_system in enumerate(json_data["spin_systems"]):
            name = "" if "name" not in spin_system.keys() else spin_system["name"]
            abd = spin_system["abundance"]
            n_site = len(spin_system["sites"])
            isotopes = "-".join(set([item["isotope"] for item in spin_system["sites"]]))
            pack = [i, name, abd, n_site, isotopes, icon]
            sys_row.append(html.Tr([html.Td(item) for item in pack]))

    method_row = []
    mth_items = ["", "Name", "Channels", "B0 / T", "vr / kHz", ""]
    method_row.append(html.Tr([html.Td(html.B(item)) for item in mth_items]))

    if "methods" in json_data:
        icon = html.Span(html.I(className="fas fa-pencil-alt"), **{"data-edit-mth": ""})
        for i, method in enumerate(json_data["methods"]):
            name = "" if "name" not in method.keys() else method["name"]
            channels = "-".join(method["channels"])
            Bo = method["spectral_dimensions"][0]["events"][0]["magnetic_flux_density"]
            vr = method["spectral_dimensions"][0]["events"][0]["rotor_frequency"] / 1e3
            method_row.append(
                html.Tr([html.Td(item) for item in [i, name, channels, Bo, vr, icon]])
            )

    return [method_row, sys_row]


def display_sample_info(json_data):
    title = json_data["name"]
    title = "Sample" if title == "" else title
    description = json_data["description"]
    data = [
        html.H4(
            [title, button, modal],
            style={"display": "flex", "justify-content": "space-between"},
        ),
        dbc.Card(dbc.CardBody(description)),
    ]
    tables = display_spin_system_info_table(json_data)
    icons = html.Ul(
        [
            html.Li(html.Span(html.I(className="fas fa-plus-circle fa-lg"))),
            html.Li(html.Span(html.I(className="fas fa-clone fa-lg"))),
            html.Li(html.Span(html.I(className="fas fa-minus-circle fa-lg"))),
        ],
        **{"data-edit-tools": ""},
    )

    method_table = [
        html.Div([html.H5("Method Overview"), icons], **{"data-table-header-mth": ""}),
        html.Table(tables[0], id="method-table", **{"data-table-mth": ""}),
    ]
    system_table = [
        html.Div(
            [html.H5("Spin system Overview"), icons], **{"data-table-header-sys": ""}
        ),
        html.Table(tables[1], id="system-table", **{"data-table-sys": ""}),
    ]

    return html.Div([*data, *method_table, *system_table], **{"data-info-table": ""})


sample_info = html.Div(
    className="left-card active",
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
