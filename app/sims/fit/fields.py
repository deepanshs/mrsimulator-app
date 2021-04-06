# -*- coding: utf-8 -*-
import json
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.dependencies import ALL
from dash.dependencies import MATCH
from dash.exceptions import PreventUpdate

from app import app


KEY_LIST = ["value", "vary", "min", "max", "brute_step"]
LEN_KEY_LIST = len(KEY_LIST)
WIDTHS = {
    "name": 3,
    "value": 2,
    "vary": 1,
    "min": 2,
    "max": 2,
    # "expr": 0,
    "brute_step": 2,
}
testing_params_dict = {
    "param_name_1" : {"value": 0, "vary": True, "min": None, "max": 100, "brute_step": None},
    "param_name_2" : {"value": 200, "vary": False, "min": 0, "max": None, "brute_step": None},
    "param_name_3" : {"value": 17.3, "vary": True, "min": None, "max": 100, "brute_step": 0.5},
}

def fields_header():
    """Header labels for fitting parameters"""
    cols = [dbc.Col(html.Div("Name"), width=WIDTHS["name"])]
    cols += [
        dbc.Col(html.Div(" ".join(key.split("_")).capitalize())) 
        for key in KEY_LIST  # Needs width arguments
    ]
    cols += [dbc.Col(html.Div("Remove"))]
    return html.Div(dbc.Row(cols))


def fields_input():
    """List of input fields"""
    return html.Div(children=[], id="parameters-input-div") # Additional div formatting here


def delete_row_button(name):
    """Makes delete button for spesicied row name"""
    return html.Button(id={"name": f"delete-{name}-row", "kind": "delete"}, children="Delete")


def make_input_row(name, vals):
    """Constructs list of dbc.Col components for user input
    
    Params:
        str name: Name of parameter
        dict vals: Dictonary of parameter values

    Returns:
        dbc.Row object
    """
    return dbc.Row(
        id=f"{name}-row", 
        # May need additional formatting to fit within bounds
        children=[
            dbc.Col(html.Div(id={"name": f"{name}-label", "kind": "name"}, children=name), width=WIDTHS["name"]),
            dbc.Col(dbc.Input(id={"name": f"{name}-value", "kind": "value"}, type="number", value=vals["value"])),
            dbc.Col(dbc.Checkbox(id={"name": f"{name}-vary", "kind": "vary"}, checked=vals["vary"]), width=WIDTHS["vary"]),
            dbc.Col(dbc.Input(id={"name": f"{name}-min", "kind": "min"}, type="number", value=vals["min"])),
            dbc.Col(dbc.Input(id={"name": f"{name}-max", "kind": "max"}, type="number", value=vals["max"])),
            # dbc.Col(dbc.Input(id={"name": f"-{name}-expr", "kind": "expr"}, type="text", value=vals["expr"])),  # NOT IMPLEMENTED
            dbc.Col(dbc.Input(id={"name": f"{name}-brute-step", "kind": "brute-step"}, type="number", value=vals["brute_step"])),
            dbc.Col(delete_row_button(name))
        ]
    )


def ui():
    """Intputs fields with names and delete buttons"""
    update_button = html.Button(id="update-button", children="Update", n_clicks=0)
    reset_button = html.Button(id="reset-button", children="Reset", n_clicks=0)

    temp_test_button = html.Button(id="SERVER-TRIGGER", children="Test")
    return html.Div(
        children=[
            fields_header(), 
            fields_input(), 
            update_button, 
            reset_button, 
            temp_test_button],
        id="input-fields",
        # additional fields needed for formatting?
    )


fields = ui()


# Callbacks ===================================================================
@app.callback(
    Output("parameters-input-div", "children"),
    Input("visible-parameters-data", "data"),
)
def update_fields_input(data):
    """Updated visible fields when visible data is changed"""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "update-button":
        raise PreventUpdate

    if data is None:  # Empty data
        return

    rows = [make_input_row(k, v) for k, v in data.items()]
    return rows


@app.callback(
    Output("stored-parameters-data", "data"),
    Input("SERVER-TRIGGER", "n_clicks"),
    State("stored-parameters-data", "data")
)
def update_stored_params_data(tr, stored_data):
    """Sets stored params data on trigger from server"""
    # How to send dict between server and client?

    # Verify stored data on load 
    if not ctx.triggered:
        if not set(KEY_LIST) == set([k for d in stored_data.values() for k in d.keys()]):
            return testing_params_dict
            # return {}  # Remove invalid data
        return stored_data

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "SERVER-TRIGGER":
        return testing_params_dict

    return stored_data


@app.callback(
    Output("visible-parameters-data", "data"),

    Input("update-button", "n_clicks"),
    Input("reset-button", "n_clicks"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    Input("stored-parameters-data", "data"),

    State("visible-parameters-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),
    State({"kind": "value", "name": ALL}, "value"),
    State({"kind": "vary", "name": ALL}, "checked"),
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    # State({"kind": "expr", "name": ALL}, "value"),
    State({"kind": "brute-step", "name": ALL}, "value"),
)
def update_visible_data(n1, n2, n3, data, visible_data, names, *vals):
    """Sets visible data from either fields inputs or stored data"""
    if not ctx.triggered:
        return data

    trigger_id = trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Comprehension triggers
    if trigger_id[0] == "{":
        trigger_id = json.loads(trigger_id)  # Cast to dict
        if "name" in trigger_id and trigger_id["name"][:6] == "delete":
            del visible_data[trigger_id["name"].split("-")[1]]
            return visible_data

    if trigger_id == "reset-button":
        return data

    if trigger_id == "update-button":
        zip_vals = list(zip(*vals))
        params_dict = {}
        for i, name in enumerate(names):
            params_dict[name] = {key: zip_vals[i][j] for j, key in enumerate(KEY_LIST)}
        print(params_dict)
        return params_dict

    return data
    

# Validate input callback

# Disable checkbox if 'expr' is used
