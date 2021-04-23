# -*- coding: utf-8 -*-
import json
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import ALL
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from lmfit import Parameters
from mrsimulator import parse
from mrsimulator.utils.spectral_fitting import make_LMFIT_params

from app import app


CSS_STR = '*{font-family:"Helvetica",sans-serif;}td{padding: 0 8px}'


def inputs():
    """Parameters input html div"""
    return html.Div(id="params-input-div", children=[])


def report():
    """LMFIT report html div"""
    return html.Div(id="params-report-div", children=[])


def ui():
    """Main UI for fitting interface"""
    return html.Div(
        children=[inputs(), report()], id="input-fields", className="fit-scroll"
    )


fields = ui()


# Callbacks ============================================================================
@app.callback(
    Output("params-input-div", "children"),
    Output("params-report-div", "children"),
    Output("params-report-div", "hidden"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    Input("reset-button", "n_clicks"),
    Input("local-mrsim-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),  # Requires states to be generated
    State({"kind": "value", "name": ALL}, "value"),  # to be made in the order which
    State({"kind": "vary", "name": ALL}, "checked"),  # they appear on the page.
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    State({"kind": "expr", "name": ALL}, "value"),
    prevent_initial_call=True,
)
def update_fitting_elements(n1, n2, mr_data, *vals):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fitting elements", trigger_id)
    if trigger_id.startswith("{"):
        py_dict = json.loads(trigger_id)
        name, trigger_id = py_dict["name"], py_dict["kind"]
        return CALLBACKS[trigger_id](name, vals)

    return CALLBACKS[trigger_id](vals)


# Main data callback
@app.callback(
    Output("params-data", "data"),
    Output("trigger-sim", "data"),
    Output("trigger-fit", "data"),
    Input("simulate-button", "n_clicks"),
    Input("run-fitting-button", "n_clicks"),
    State("local-mrsim-data", "data"),
    State("params-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),  # Requires states to be generated
    State({"kind": "value", "name": ALL}, "value"),  # to be made in the order which
    State({"kind": "vary", "name": ALL}, "checked"),  # they appear on the page.
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    State({"kind": "expr", "name": ALL}, "value"),
    prevent_initial_call=True,
)
# def update_fitting_data(n1, n2, n3, n4, _, mr_data, p_data, *vals):
def update_fitting_data(n1, n2, mr_data, _, *vals):
    """Main callback for fitting parameters interface"""
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fitting data", trigger_id)

    return CALLBACKS[trigger_id](vals)


# Helper Methods =======================================================================
def update_params_and_simulate(vals):
    """Updates stored Parameters object JSON and triggers a simulation"""
    return get_new_params_json(vals), int(datetime.now().timestamp() * 1000), no_update


def update_params_and_fit(vals):
    """Updates stored Parameters object JSON and triggers fitting"""
    params_data = ctx.states["params-data.data"]

    print("FITTING")
    print(params_data)

    return get_new_params_json(vals), no_update, int(datetime.now().timestamp() * 1000)


def delete_param(name, vals):
    """Deletes specified param (row) from interface and updates stored JSON"""
    params_data = get_new_params_json(vals)
    params_obj = Parameters().loads(params_data)

    name = name.split("-")[1]
    del params_obj[name]

    params_dict = params_obj_to_dict(params_obj)
    table = fit_table(params_dict)

    return table, no_update, no_update


def construct_params_body(*args):
    data = ctx.inputs["local-mrsim-data.data"]
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if len(data["spin_systems"]) == 0:
        table = fit_table({})
        return table, no_update, True

    if trigger_id == "reset-button":
        sim, processor, _ = parse(data)
        params_obj = make_LMFIT_params(sim, processor)

    else:
        if "params" in data and data["params"] is not None:
            params_obj = Parameters().loads(data["params"])
        else:
            sim, processor, _ = parse(data)
            params_obj = make_LMFIT_params(sim, processor)

    params_dict = params_obj_to_dict(params_obj)
    table = fit_table(params_dict)
    report, hide = ("", True) if "report" not in data else (data["report"], False)
    report = html.Iframe(sandbox="", srcDoc=report, id="fit-report-iframe")

    return table, report, hide


# Add 'expression' field after code refactored
#   requires validation? or can take errors from 'lmfit' library
# Truncate decimal places (using css?)
def fit_table(params_dict):
    """Constructs html table of parameter inputs fields for user input

    Params:
        params_dict: dict representation of Parameters object

    Returns:
        html.Table with inputs
    """
    fit_header = ["", "Name", "Value", "Min", "Max", "expr", ""]
    fit_rows = [html.Thead(html.Tr([html.Th(html.B(item)) for item in fit_header]))]

    input_args = {"type": "number", "autoComplete": "off"}
    for key, vals in params_dict.items():
        vary_id = {"name": f"{key}-vary", "kind": "vary"}
        name_id = {"name": f"{key}-label", "kind": "name"}
        val_id = {"name": f"{key}-value", "kind": "value"}
        min_id = {"name": f"{key}-min", "kind": "min"}
        max_id = {"name": f"{key}-max", "kind": "max"}
        expr_id = {"name": f"{key}-expr", "kind": "expr"}

        # Name with tooltip on hover and pattern matching id
        name = html.Div(id=name_id, children=key)
        name_wrapper = html.Div(name, id=f"{key}-tooltip-div-wrapper")
        tooltip = dbc.Tooltip(key, target=f"{key}-tooltip-div-wrapper")
        name_div = html.Div([name_wrapper, tooltip])

        vary = dbc.Checkbox(id=vary_id, checked=vals["vary"])
        # Safari raises input invalid with type=number and a float value
        val = dcc.Input(id=val_id, value=vals["value"], **input_args)
        min_ = dcc.Input(id=min_id, value=vals["min"], **input_args)
        max_ = dcc.Input(id=max_id, value=vals["max"], **input_args)
        expr_ = dcc.Input(id=expr_id, value=vals["expr"])
        ic = html.Span(
            html.I(className="fas fa-times", title="Remove Parameter"),
            id={"name": f"delete-{key}-row", "kind": "delete"},
            **{"data-edit-mth": ""},
        )
        pack = [vary, name_div, val, min_, max_, expr_, ic]
        fit_rows += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return html.Table(id="fields-table", children=fit_rows)


def params_obj_to_dict(params_obj):
    """Makes dictionary representation of params object from json string
    Params:
        params_obj: Parameters object

    Return:
        params_dict: dictionary of lmfit parameters
    """
    KEY_LIST = ["vary", "value", "min", "max", "expr"]  # Add expr eventually
    # params_dict = {}

    # for name, param in params_obj.items():
    #     params_dict[name] = {key: getattr(param, key) for key in KEY_LIST}
    # return params_dict

    return {
        name: {key: getattr(param, key) for key in KEY_LIST}
        for name, param in params_obj.items()
    }


def get_new_params_json(vals):
    """Returns new Parameters JSON dump from input values"""
    zip_vals = list(zip(*vals))
    new_obj = Parameters()

    for row in zip_vals:
        print(row)
        new_obj.add(*row)

    return new_obj.dumps()


CALLBACKS = {
    "simulate-button": update_params_and_simulate,
    "run-fitting-button": update_params_and_fit,
    "reset-button": construct_params_body,
    "local-mrsim-data": construct_params_body,
    "delete": delete_param,
}


# def expand_output(out):
#     """Plotly callback outputs for `update_fitting` function"""
#     return [
#         *out["params"],
#         *out["body"],
#         *out["trigger"]
#     ]
