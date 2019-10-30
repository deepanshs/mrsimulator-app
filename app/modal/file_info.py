# -*- coding: utf-8 -*-
"""Model page layout and callbacks for isotopomer file content."""
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# Layout ----------------------------------------------------------------------
# model user-interface
file_info = dbc.Modal(
    [dbc.ModalHeader(), dbc.ModalBody(html.P())],
    id="file_info_modal",
    role="document",
    # modalClassName="modal-dialog",
    # className="modal-dialog",
)


@app.callback(
    Output("file_info_modal", "is_open"),
    [Input("file_info_button", "n_clicks")],
    [State("file_info_modal", "is_open")],
)
def toggle_modal_setting(n1, is_open):
    """Model window for info input."""
    if n1 is None:
        raise PreventUpdate
    if n1:
        return not is_open
    return is_open
