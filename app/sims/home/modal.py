# -*- coding: utf-8 -*-
"""Modal window for updating simulator title and description"""
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app
from app.custom_widgets import custom_button


def title():
    """Sample Title"""
    label = dbc.FormText("Title")
    field = dbc.Input(type="text", placeholder="Add title", id="info-name-edit")
    return [label, field]


def description():
    """Sample Description"""
    label = dbc.FormText("Description")
    field = dbc.Textarea(
        value="",
        placeholder="Add description",
        id="info-description-edit",
        style={"height": "12rem"},
    )
    return [label, field]


def body():
    return html.Div([*title(), *description()])


def footer():
    save_button = dbc.Button(
        "Save",
        id="save_info_modal",
        color="dark",
        className="ml-auto",
        outline=True,
    )
    return dbc.ModalFooter(save_button)


def ui():
    """Modal body with form  and close button"""
    close_button = custom_button(
        icon_classname="fas fa-times 2x",
        tooltip="Close",
        id="close-info-modal",
        className="icon-button",
        module="html",
    )

    content = dbc.ModalBody([close_button, body()])
    return dbc.Modal(
        [content, footer()],
        id="info-modal-editor",
        is_open=False,
        role="document",
        className="modal-dialogue",
        backdrop="static",
    )


modal = ui()


app.clientside_callback(
    """function openModal(n1, n2, data) {
        let _id = dash_clientside.callback_context.triggered.map((t) => t.prop_id);
        let trigger_id = _id[0].split(".")[0]
        let no_update = window.dash_clientside.no_update;
        if (trigger_id == "close-info-modal") { return [false, no_update, no_update]; }

        let name = "Title", description = "Sample description";
        if (data != null) {
            name = data["name"];
            description = data["description"];
        }
        return [true, name, description];
    }""",
    Output("info-modal-editor", "is_open"),
    Output("info-name-edit", "value"),
    Output("info-description-edit", "value"),
    Input("title-home-button", "n_clicks"),
    Input("close-info-modal", "n_clicks"),
    State("local-mrsim-data", "data"),
    prevent_initial_call=True,
)
