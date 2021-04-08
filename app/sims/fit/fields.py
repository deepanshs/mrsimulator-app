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


KEY_LIST = ["vary", "value", "min", "max"]
# LEN_KEY_LIST = len(KEY_LIST)
WIDTHS = {
    "name": 3,
    "value": 2,
    "vary": 1,
    "min": 2,
    "max": 2,
    # "expr": 0,
    # "brute_step": 2,
}


def fields_header():
    """Header labels for fitting parameters"""
    cols = [dbc.Col(html.Div("Name"), width=WIDTHS["name"])]
    cols += [
        dbc.Col(html.Div(" ".join(key.split("_")).capitalize()))
        for key in KEY_LIST  # Needs width arguments
    ]
    return html.Div(dbc.Row(cols))


def fields_body():
    return html.Div(id="params-input-div", children=[])


def delete_row_button(name):
    """Makes delete button for spesicied row name"""
    return html.Button(
        id={"name": f"delete-{name}-row", "kind": "delete"}, children="x"
    )


def make_input_row(name, vals):
    """Constructs list of dbc.Col components for user input

    Params:
        str name: Name of parameter
        dict vals: Dictonary of parameter values

    Returns:
        dbc.Row object
    """
    name_div = html.Div(id={"name": f"{name}-label", "kind": "name"}, children=[name])
    vary_div = dbc.Checkbox(
        id={"name": f"{name}-vary", "kind": "vary"},
        checked=vals["vary"],
    )
    # value_div = None

    return dbc.Row(
        id=f"{name}-row",
        # May need additional formatting to fit within bounds
        children=[
            dbc.Col([name_div, vary_div]),
            dbc.Col(
                dbc.Input(
                    id={"name": f"{name}-value", "kind": "value"},
                    type="number",
                    value=vals["value"],
                )
            ),
            dbc.Col(
                dbc.Input(
                    id={"name": f"{name}-min", "kind": "min"},
                    type="number",
                    value=vals["min"],
                )
            ),
            dbc.Col(
                dbc.Input(
                    id={"name": f"{name}-max", "kind": "max"},
                    type="number",
                    value=vals["max"],
                )
            ),
            dbc.Col(delete_row_button(name)),
        ],
    )


def ui():
    """Intputs fields with names and delete buttons"""
    update_button = html.Button(id="update-button", children="Simulate", n_clicks=0)
    reset_button = html.Button(id="reset-button", children="Reset", n_clicks=0)
    run_fitting_button = html.Button(
        id="run-fitting-button", children="Run Fitting", n_clicks=0
    )
    return html.Div(
        children=[
            fields_header(),
            fields_body(),
            update_button,
            reset_button,
            run_fitting_button,
        ],
        id="input-fields",
        # additional fields needed for formatting?
    )


fields = ui()


def lmfit_jston_to_dict(lmfit_json):
    """Makes dictonary representation of params object from json string
    Params:
        lmfit_json: JSON string of lmtit Parameters object

    Return:
        params_dict: dictonary of lmfit parameters
    """
    params_obj = Parameters().loads(lmfit_json)
    params_dict = {}

    for name, param in params_obj.items():
        params_dict[name] = {key: getattr(param, key) for key in KEY_LIST}

    return params_dict


# Callbacks ===================================================================
@app.callback(
    Output("params-input-div", "children"),
    Input("params-data", "data"),
)
def update_fields_div(data):
    """Updated visible fields when visible data is changed"""

    # Should output be moved to another place ex. 'importer.py'
    # # Currently being triggered by reset-button on new data upload fom
    # 'update_params_data'
    # ISSUE : being updated by 'update_params_data' 'when update-button'
    # is pressed
    # Maybe 'update_params_data' can be triggered by local-mrsim-data

    print("div", ctx.triggered)
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "update-button":
        print("update button")
        raise PreventUpdate

    if data is None:
        return

    params_dict = lmfit_jston_to_dict(data)
    rows = [make_input_row(k, v) for k, v in params_dict.items()]
    return rows


@app.callback(
    Output("params-data", "data"),
    Input("update-button", "n_clicks"),
    Input("run-fitting-button", "n_clicks"),
    Input("reset-button", "n_clicks"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    State("params-data", "data"),
    State("local-mrsim-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),
    State({"kind": "value", "name": ALL}, "value"),
    State({"kind": "vary", "name": ALL}, "checked"),
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    # State({"kind": "expr", "name": ALL}, "value"),
    # State({"kind": "brute-step", "name": ALL}, "value"),
)
def update_params_data(n1, n2, n3, n4, visible_data, local_data, *vals):
    """Sets visible data from either fields inputs or stored data"""
    if not ctx.triggered:
        # return test_str
        raise PreventUpdate
    print("dat", ctx.triggered)
    trigger_id = trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "update-button" or trigger_id == "run-fitting-button":
        zip_vals = list(zip(*vals))
        new_obj = Parameters()

        for row in zip_vals:
            new_obj.add(
                name=row[0],
                value=row[1],
                vary=row[2],
                min=row[3],
                max=row[4],
                # expr=,
                # brute_step=float(row[4]) if row[4] is not None else 0,
            )

        return new_obj.dumps()

    if trigger_id == "reset-button":
        if local_data is None:
            raise PreventUpdate
        sim = Simulator(**local_data)
        params_obj = make_LMFIT_params(sim)
        return params_obj.dumps()

    # Comprehension triggers
    if trigger_id[0] == "{":
        trigger_id = json.loads(trigger_id)  # Cast to dict
        if "name" in trigger_id and trigger_id["name"][:6] == "delete":
            params_obj = Parameters().loads(visible_data)
            del params_obj[trigger_id["name"].split("-")[1]]
            return params_obj.dumps()
        # Start other context calls here


# Validate input callback

# Disable checkbox if 'expr' is used
