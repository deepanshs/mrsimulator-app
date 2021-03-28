# -*- coding: utf-8 -*-
"""Modal window for updating simulator title and description"""
import dash_bootstrap_components as dbc
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

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
    return dbc.FormGroup([*title(), *description()])


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
        className="modal-dialog",
        backdrop="static",
    )


modal = ui()


@app.callback(
    [
        Output("info-modal-editor", "is_open"),
        Output("info-name-edit", "value"),
        Output("info-description-edit", "value"),
    ],
    [
        Input("title-home-button", "n_clicks"),
        Input("close-info-modal", "n_clicks"),
    ],
    [State("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
def open_modal(n1, n2, data):
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "close-info-modal":
        return False, no_update, no_update

    name = "Title" if data is None else data["name"]
    description = "Sample description" if data is None else data["description"]
    return True, name, description
