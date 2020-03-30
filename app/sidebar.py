# -*- coding: utf-8 -*-
import json

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_button
from app.modal.file_info import file_info

# from dash.dependencies import ClientsideFunction

colors = {"background": "#e2e2e2", "text": "#585858"}

# Info ------------------------------------------------------------------------------ #
isotopomers_info_button = custom_button(
    icon_classname="fas fa-info-circle",
    id="indicator_status",
    tooltip="Isotopomers info",
    outline=True,
    color="dark",
)

filename_datetime = html.Div(
    [
        html.H5("Add a title", id="filename_dataset"),
        file_info,
        html.P(
            "Add a description ... ",
            id="data_description",
            style={"textAlign": "left", "color": colors["text"]},
        ),
    ]
)


@app.callback(
    Output("isotopomer-dropdown", "value"),
    [
        Input("nmr_spectrum", "clickData"),
        Input("local-processed-data", "modified_timestamp"),
    ],
    [
        State("isotopomer-dropdown", "options"),
        State("decompose", "active"),
        State("isotopomer-dropdown", "value"),
        State("local-isotopomer-index-map", "data"),
        State("config", "data"),
    ],
)
def update_isotopomer_dropdown_index(
    clickData, t1, options, decompose, dropdown_index, index_map, config
):
    """Update the current value of the isotopomer dropdown value when the trace
       (line plot) is selected, or
        Args:
            clickData: (trigger) the click data when a trace is clicked.
            options: (trigger) the list of new options for the isotopomers dropdown.
            decompose: (state) the state of the decompose option.
            old_dropdown_value: (state) the old drop-down index value. Return 0, if
                old value is greater than the length of new options, else return the
                old value
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    if config is None:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "local-processed-data" and config["is_new_data"]:
        dropdown_index = 0 if dropdown_index is None else dropdown_index
        dropdown_index = 0 if dropdown_index >= len(options) else dropdown_index
        return dropdown_index
    if trigger_id == "local-processed-data":
        return no_update

    if clickData is None:
        return no_update

    index = clickData["points"][0]["curveNumber"] if decompose else 0
    return index_map[index]


@app.callback(
    Output("json-file-editor", "value"),
    [Input("isotopomer-dropdown", "value"), Input("json-file-editor-button", "active")],
    [State("local-isotopomers-data", "data")],
)
def update_json_file_editor_from_isotopomer_dropdown(
    index, is_advanced_editor_open, local_isotopomer_data
):
    """Return an isotopomer as a JSON value corresponding to dropdown selection index.
    Args:
        index: (trigger) The index of isotopomer dropdown selection.
        local_isotopomer_data: (state) Local isotopomers data as the state.
    """
    print("active", is_advanced_editor_open)

    if not is_advanced_editor_open:
        raise PreventUpdate
    if local_isotopomer_data is None:
        return PreventUpdate
    if index is None:
        return ""

    isotopomer_list = local_isotopomer_data["isotopomers"]
    print("dropdown index", index)
    if index >= len(isotopomer_list):
        index = 0

    return json.dumps(isotopomer_list[index], indent=2, ensure_ascii=True)


# app.clientside_callback(
#     # Update isotopomer dropdown options base on local isotopomers data.
#     #     Args:
#     #         isotope_id_value: (trigger) a filter and update of the isotopomer
#     #             dropdown options based on the value of the isotope.
#     #         local_isotopomer_data: (state) Local isotopomers data as the state.
#     #
#     ClientsideFunction(
#         namespace="clientside", function_name="update_isotopomer_dropdown_options"
#     ),
#     Output("isotopomer-dropdown", "options"),
#     [Input("local-isotopomers-data", "data")],
# )


sidebar = dbc.Card(
    dbc.CardBody(filename_datetime),
    className="my-card-sidebar",
    inverse=False,
    id="sidebar",
)
