# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import ALL
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from lmfit import Parameters
from mrsimulator import Simulator
from mrsimulator.utils.spectral_fitting import make_LMFIT_params

from app import app


def fitting_interface_table(params_dict):
    """Creates list of components to pass into a html.Table for user input"""
    fit_header = ["", "Name", "Value", "Min", "Max", ""]
    fit_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in fit_header]))]

    for key, vals in params_dict.items():
        vary_id = {"name": f"{key}-vary", "kind": "vary"}
        name_id = {"name": f"{key}-label", "kind": "name"}
        val_id = {"name": f"{key}-value", "kind": "value"}
        min_id = {"name": f"{key}-min", "kind": "min"}
        max_id = {"name": f"{key}-max", "kind": "max"}

        # Name with tooltip on hover and pattern matching id
        name = html.Div(id=name_id, children=key)
        name_wrapper = html.Div(name, id=f"{key}-tooltip-div-wrapper")
        tooltip = dbc.Tooltip(key, target=f"{key}-tooltip-div-wrapper")
        name_div = html.Div([name_wrapper, tooltip])

        vary = dbc.Checkbox(id=vary_id, checked=vals["vary"])
        val = dbc.Input(id=val_id, type="number", value=vals["value"])
        min = dbc.Input(id=min_id, type="number", value=vals["min"])
        max = dbc.Input(id=max_id, type="number", value=vals["max"])
        ic = html.Span(  # Way to add shadow when hovered?
            html.I(className="fas fa-times", title="Remove Parameter"),
            id={"name": f"delete-{key}-row", "kind": "delete"},
            **{"data-edit-mth": ""},
        )
        pack = [vary, name_div, val, min, max, ic]
        fit_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return fit_row


def fields_body():
    return html.Div(id="params-input-div", children=[])


def ui():
    """Intputs fields with names and delete buttons"""
    reset_button = html.Button(id="reset-button", children="Reset")
    simulate_button = html.Button(id="simulate-button", children="Simulate Spectrum")
    run_fitting_button = html.Button(id="run-fitting-button", children="Run Fitting")
    return html.Div(
        children=[fields_body(), reset_button, simulate_button, run_fitting_button],
        id="input-fields",
    )


fields = ui()


def lmfit_jston_to_dict(lmfit_json):
    """Makes dictonary representation of params object from json string
    Params:
        lmfit_json: JSON string of lmtit Parameters object

    Return:
        params_dict: dictonary of lmfit parameters
    """
    KEY_LIST = ["vary", "value", "min", "max"]
    params_obj = Parameters().loads(lmfit_json)
    params_dict = {}

    for name, param in params_obj.items():
        params_dict[name] = {key: getattr(param, key) for key in KEY_LIST}

    return params_dict


# Callbacks ===================================================================
@app.callback(
    Output("params-input-div", "children"),
    Input("params-data", "data"),
    State("do-fit-div-update", "data"),
)
def update_fields_div(data, do_update):
    """Updated visible fields when visible data is changed"""
    if not do_update:
        raise PreventUpdate

    if data is None:
        return html.Table(id="fields-table", children=fitting_interface_table({}))

    params_dict = lmfit_jston_to_dict(data)
    rows = fitting_interface_table(params_dict)
    return html.Table(id="fields-table", children=rows)


@app.callback(
    Output("params-data", "data"),
    Output("do-fit-div-update", "data"),  # Latch to prevent 'update_fields_div'
    Input("simulate-button", "n_clicks"),
    Input("run-fitting-button", "n_clicks"),
    Input("reset-button", "n_clicks"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    Input("local-mrsim-data", "data"),
    State("params-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),  # Requires states to be generated
    State({"kind": "value", "name": ALL}, "value"),  # to be made in the order which
    State({"kind": "vary", "name": ALL}, "checked"),  # they appear on the page.
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
)
def update_params_data(n1, n2, n3, n4, mrsim_data, visible_data, *vals):
    """Sets visible data from either fields inputs or stored data"""
    if not ctx.triggered:
        return None, True
        # raise PreventUpdate
    trigger_id = trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "simulate-button" or trigger_id == "run-fitting-button":
        zip_vals = list(zip(*vals))
        new_obj = Parameters()

        for row in zip_vals:
            new_obj.add(*row)

        return new_obj.dumps(), False

    if trigger_id == "reset-button" or trigger_id == "local-mrsim-data":
        if len(mrsim_data["spin_systems"]) == 0:
            raise PreventUpdate
        sim = Simulator.parse_dict_with_units(mrsim_data)
        params_obj = make_LMFIT_params(sim)
        return params_obj.dumps(), True

    # Comprehension triggers
    if trigger_id[0] == "{":
        trigger_id = json.loads(trigger_id)  # Cast to dict
        if "name" in trigger_id and trigger_id["name"][:6] == "delete":
            params_obj = Parameters().loads(visible_data)
            del params_obj[trigger_id["name"].split("-")[1]]
            return params_obj.dumps(), True
        # Start other context calls here
