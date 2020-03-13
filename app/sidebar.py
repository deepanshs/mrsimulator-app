# -*- coding: utf-8 -*-
import json

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_button
from app.isotopomer.draft import filter_isotopomer_list
from app.isotopomer.draft import get_isotopomer_dropdown_options
from app.modal.file_info import file_info

# from app.isotopomer.draft import isotopomer_set

# from app.isotopomer import display_isotopomers

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
        dbc.Row(
            [
                dbc.Col(
                    html.H5(
                        "Add a title", id="filename_dataset"  # contentEditable="True"
                    )
                ),
                # dbc.Col(
                #     isotopomers_info_button,
                #     width=3,
                #     className="d-flex justify-content-end",
                # )
                # dbc.Col(
                #     custom_button(
                #         text="",
                #         icon_classname="fas fa-edit",
                #         id="json-file-editor-toggler",
                #         tooltip="Edit the isotopomer file.",
                #         active=False,
                #         outline=True,
                #         style={"float": "right"},
                #     )
                # ),
            ],
            className="d-flex justify-content-between",
        ),
        file_info,
        html.P(
            "Add a description ... ",
            id="data_description",
            style={"textAlign": "left", "color": colors["text"]},
            # contentEditable="True",
        ),
        # isotopomer_set,
        # site_set,
        # html.H6(
        #     html.A(
        #         id="data_citation",
        #         href="https://pubs.acs.org/doi/abs/10.1021/ic020647f",
        #         target="_blank",
        #     ),
        #     style={"textAlign": "left", "color": colors["text"], "fontSize": 12},
        # ),
    ]
)

# def get_isotopomer_from_clicked_spectrum(clickData, local_computed_data):
#     if clickData is not None:
#         index = [clickData["points"][0]["curveNumber"]]
#     else:
#         length = len(local_computed_data["csdm"]["dependent_variables"])
#         index = [i for i in range(length)]

#     isotopomer = []
#     for i in index:
#         datum = local_computed_data["csdm"]["dependent_variables"][i]
#         isotopomer.append(
#             datum["application"]["com.github.DeepanshS.mrsimulator"]["isotopomers"][0]
#         )
#     return index, isotopomer


@app.callback(
    Output("isotopomer-dropdown", "value"),
    [Input("nmr_spectrum", "clickData"), Input("isotopomer-dropdown", "options")],
    [State("decompose", "active"), State("isotopomer-dropdown", "value")],
)
def update_isotopomer_dropdown_index(clickData, options, decompose, old_dropdown_value):
    """Update the current value of the isotopomer dropdown value when
        a) the trace (line plot) is selected, or
        b) the isotopomer dropdown options has changed.
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

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "isotopomer-dropdown":
        if old_dropdown_value > len(options):
            return 0
        return old_dropdown_value

    if clickData is None:
        raise PreventUpdate

    index = 0
    if decompose:
        index = clickData["points"][0]["curveNumber"]
    return index


@app.callback(
    Output("json-file-editor", "value"),
    [Input("isotopomer-dropdown", "value"), Input("new-json", "data")],
    [State("local-isotopomers-data", "data"), State("isotope_id-0", "value")],
)
def update_json_file_editor_from_isotopomer_dropdown(
    index, new_json_data, local_isotopomer_data, isotope_id_value
):
    """Return an isotopomer as a JSON value corresponding to dropdown selection index.
    Args:
        index: (trigger) The index of isotopomer dropdown selection.
        local_isotopomer_data: (state) Local isotopomers data as the state.
        isotope_id_value: (state) update of the isotopomer json list based on the value
            of the isotope.
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if local_isotopomer_data is None:
        raise PreventUpdate
    if index is None:
        raise PreventUpdate

    isotopomer_list = filter_isotopomer_list(
        local_isotopomer_data["isotopomers"], isotope_id_value
    )
    print("isotope_id_value", isotope_id_value, index)
    if index >= len(isotopomer_list):
        index = 0

    if trigger_id == "new-json":
        isotopomer_list[index] = new_json_data

    return json.dumps(isotopomer_list[index], indent=2, ensure_ascii=True)


@app.callback(
    Output("isotopomer-dropdown", "options"),
    [Input("isotope_id-0", "value")],
    [State("local-isotopomers-data", "data")],
)
def update_isotopomer_dropdown_options(isotope_id_value, local_isotopomer_data):
    """Update isotopomer dropdown options base on local isotopomers data.
        Args:
            isotope_id_value: (trigger) a filter and update of the isotopomer
                dropdown options based on the value of the isotope.
            local_isotopomer_data: (state) Local isotopomers data as the state.
    """
    if isotope_id_value is None:
        raise PreventUpdate
    if local_isotopomer_data is None:
        raise PreventUpdate

    isotopomer_dropdown_options = get_isotopomer_dropdown_options(
        local_isotopomer_data["isotopomers"], isotope_id_value
    )
    # print("option list", local_isotopomer_data, isotopomer_dropdown_options)
    return isotopomer_dropdown_options


sidebar = dbc.Card(
    dbc.CardBody(filename_datetime),
    className="h-100 my-card-sidebar",
    inverse=False,
    id="sidebar",
)
