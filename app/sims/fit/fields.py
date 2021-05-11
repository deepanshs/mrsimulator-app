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
from dash.dependencies import MATCH
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from lmfit import Parameters
from mrsimulator import parse
from mrsimulator.utils.spectral_fitting import make_LMFIT_params

from app import app


CSS_STR = "*{font-family:'Helvetica',sans-serif;}td{padding: 0 8px}"
TITLE = {"sys": "Spin System", "mth": "Method", "SP": "Method"}


def inputs():
    """Parameters input html div"""
    return html.Div(id="params-input-div", children=[])


def modals():
    """Hidden modals div"""
    return html.Div(id="params-modals-div", children=[], hidden=False)


def report():
    """LMFIT report html div"""
    return html.Div(id="params-report-div", children=[])


def ui():
    """Main UI for fitting interface"""
    return html.Div(
        children=[inputs(), modals(), report()],
        id="input-fields",
        className="fit-scroll",
    )


fields = ui()


# Callbacks ============================================================================
# Two callbacks are needed to avoid circular dependency error
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
def update_fit_data(n1, n2, mr_data, p_data, *vals):
    """Main fitting callback dealing with data management"""
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fit data", trigger_id)

    return CALLBACKS[trigger_id](vals)


@app.callback(
    Output("params-input-div", "children"),
    Output("params-modals-div", "children"),
    Output("params-report-div", "children"),
    Output("params-report-div", "hidden"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    Input("refresh-button", "n_clicks"),  # Goes away soon
    # Input("local-mrsim-data", "data"),
    Input("trigger-table-update", "data"),
    State("local-mrsim-data", "data"),
    State({"kind": "name", "name": ALL}, "children"),  # Requires states to be generated
    State({"kind": "value", "name": ALL}, "value"),  # to be made in the order which
    State({"kind": "vary", "name": ALL}, "checked"),  # they appear on the page.
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    State({"kind": "expr", "name": ALL}, "value"),
    prevent_initial_call=True,
)
def update_fit_elements(n1, n2, trig, mr_data, *vals):
    "Main fitting callback dealing with visible elements"
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fit elements", trigger_id)

    if trigger_id.startswith("{"):
        py_dict = json.loads(trigger_id)
        name, trigger_id = py_dict["name"], py_dict["kind"]
        return CALLBACKS[trigger_id](name, vals)

    return CALLBACKS[trigger_id](vals)


# Opens/closes params modal
# BUG: On delete spin system `nonexistant object as Input` error.
app.clientside_callback(
    "function (n1, n2, is_open) { if(n1 == null) { return false; } return !is_open; }",
    Output({"kind": "modal", "parrent": MATCH}, "is_open"),
    Input({"kind": "modal-btn", "parrent": MATCH}, "n_clicks"),
    # Input({"kind": "modal-sub-btn", "parrent": MATCH}, "n_clicks"),
    State({"kind": "modal", "parrent": MATCH}, "is_open"),
    prevent_initial_call=True,
)


# Helper Methods =======================================================================
def update_params_and_simulate(vals):
    """Updates stored Parameters object JSON and triggers a simulation"""
    return get_new_params_json(vals), int(datetime.now().timestamp() * 1000), no_update


def update_params_and_fit(vals):
    """Updates stored Parameters object JSON and triggers fitting"""
    return get_new_params_json(vals), no_update, int(datetime.now().timestamp() * 1000)


def delete_param(name, vals):
    """Deletes specified param (row) from interface and updates stored JSON"""
    params_data = get_new_params_json(vals)
    params_obj = Parameters().loads(params_data)

    name = name.split("-")[1]
    # Add check to make sure name is in params
    del params_obj[name]

    tables = make_fit_tables(params_obj_to_dict(params_obj))
    modals = make_modals_div(params_obj_to_dict(params_obj))

    return tables, modals, no_update, no_update


def reset_params_body(*args):
    return update_tables(*args, reset=True)


def update_params_body(*args):
    return update_tables(*args)


def update_tables(*args, reset=False):
    # data = ctx.inputs["local-mrsim-data.data"]
    data = ctx.states["local-mrsim-data.data"]

    if len(data["spin_systems"]) == 0:
        return None, no_update, True, True

    sim, processor, report = parse(data)

    if "params" in data and data["params"] is not None and not reset:
        params_obj = Parameters().loads(data["params"])
    else:
        params_obj = make_LMFIT_params(sim, processor, include={"rotor_frequency"})

    tables = make_fit_tables(params_obj_to_dict(params_obj))
    modals = make_modals_div(params_obj_to_dict(params_obj))
    report, hide = ("", True) if "report" not in data else (data["report"], False)
    report = html.Iframe(sandbox="", srcDoc=report, id="fit-report-iframe")

    return tables, modals, report, hide


def make_modals_div(params_dict):
    """Constructs hidden html.Div containing params modals

    Params:
        params_dict: dict representation of Parameters object

    Returns:
        list of modals
    """

    def make_modal(key, vals):
        """Helper method to make each modal"""
        min_id = {"name": f"{key}-min", "kind": "min"}
        max_id = {"name": f"{key}-max", "kind": "max"}
        expr_id = {"name": f"{key}-expr", "kind": "expr"}
        modal_id = {"kind": "modal", "parrent": key}
        # submit_id = {"kind": "modal-sub-btn", "parrent": key}

        min_ = html.Div(
            ["Minimum", dcc.Input(value=vals["min"], id=min_id)], className="input-form"
        )
        max_ = html.Div(
            ["Maximum", dcc.Input(value=vals["max"], id=max_id)], className="input-form"
        )
        expr = html.Div(
            ["Expression", dcc.Input(value=vals["expr"], type="text", id=expr_id)],
            className="input-form",
        )

        head = dbc.ModalHeader(html.B(key))
        body = dbc.ModalBody([min_, max_, expr])
        # foot = dbc.ModalFooter(dbc.Button("Submit", id=submit_id))

        return dbc.Modal([head, body], id=modal_id)

    # Add dummy modal to prevent MATCH error?
    modals = []
    for key, vals in params_dict.items():
        modals += [make_modal(key, vals)]

    return modals


def make_fit_tables(params_dict):
    """Makes list of grouped html.Table elements

    Params:
        params_dict: dict reporesentation of whole Parameters object

    Returns:
        tables: list of html.Table
    """
    tables = []
    # Slice params_dict
    keys = list(params_dict.keys())

    if len(keys) == 0:
        return

    prefix = keys[0][:5]
    tmp = []
    search_sys = ["Spin Systems"]
    search_mth = ["Methods"]

    index_sys, index_mth, index = 0, 0, 0
    for key in keys:
        if key[:5] != prefix:
            if tmp[0][:3] == "sys":
                search_sys.append(
                    html.Button(index_sys, id={"key": "fit-table-btn", "index": index})
                )
                index_sys += 1
            else:
                search_mth.append(
                    html.Button(index_mth, id={"key": "fit-table-btn", "index": index})
                )
                index_mth += 1
            lst = tmp[0].split("_")
            title = f"{TITLE[lst[0]]} {lst[1]}"
            tables.append(fit_table({k: params_dict[k] for k in tmp}, index, title))
            tmp, prefix = [], key[:5]
            index += 1

        tmp.append(key)

    if tmp[0][:3] == "sys":
        search_sys.append(
            html.Button(index_sys, id={"key": "fit-table-btn", "index": index})
        )
    else:
        search_mth.append(
            html.Button(index_mth, id={"key": "fit-table-btn", "index": index})
        )
    lst = tmp[0].split("_")
    title = f"{TITLE[lst[0]]} {lst[1]}"
    tables.append(
        fit_table(
            {k: params_dict[k] for k in tmp},
            index,
            title,
        )
    )

    return html.Div([html.Div(search_sys), html.Div(search_mth), html.Div(tables)])


# Truncate decimal places (using css?)
def fit_table(_dict, index, title="Name"):
    """Constructs html table of parameter inputs fields

    Params:
        _dict: slice from dict representation of Parameters object

    Returns:
        html.Table
    """
    fit_header = ["", title, "Value", "", ""]
    fit_rows = [html.Thead(html.Tr([html.Th(html.B(item)) for item in fit_header]))]

    input_args = {"type": "number", "autoComplete": "off"}
    for key, vals in _dict.items():
        vary_id = {"name": f"{key}-vary", "kind": "vary"}
        name_id = {"name": f"{key}-label", "kind": "name"}
        val_id = {"name": f"{key}-value", "kind": "value"}
        mod_btn_id = {"kind": "modal-btn", "parrent": key}
        del_id = {"name": f"delete-{key}-row", "kind": "delete"}

        name = html.Div(id=name_id, children=key)
        vary = dbc.Checkbox(id=vary_id, checked=vals["vary"])
        val = dcc.Input(id=val_id, value=vals["value"], **input_args)

        modal_ic = html.Span(
            html.I(className="fas fa-sliders-h", title="More Settings"),
            id=mod_btn_id,
            className="icon-button",
        )

        del_ic = html.Span(
            html.I(className="fas fa-times", title="Remove Parameter"),
            id=del_id,
            className="icon-button",
        )

        pack = [vary, name, val, modal_ic, del_ic]
        fit_rows += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return html.Table(
        className="fields-table active" if index == 0 else "fields-table",
        children=fit_rows,
        id={"key": "fit-table", "index": index},
    )


app.clientside_callback(
    """function (n, className) {
        let check = className.includes('active');
        if (check) return className.replace('active', '').trim();
        if (!check) return `${className} active`;
    }""",
    Output({"key": "fit-table", "index": MATCH}, "className"),
    Input({"key": "fit-table-btn", "index": MATCH}, "n_clicks"),
    State({"key": "fit-table", "index": MATCH}, "className"),
    prevent_initial_call=True,
)


def params_obj_to_dict(params_obj):
    """Makes dictionary representation of params object from json string
    Params:
        params_obj: Parameters object

    Return:
        params_dict: dictionary of lmfit parameters
    """
    KEY_LIST = ["vary", "value", "min", "max", "expr"]

    return {
        name: {key: getattr(param, key) for key in KEY_LIST}
        for name, param in params_obj.items()
    }


def get_new_params_json(vals):
    """Returns new Parameters JSON dump from input values"""
    zip_vals = list(zip(*vals))
    new_obj = Parameters()

    for row in zip_vals:
        new_obj.add(*row)

    return new_obj.dumps()


CALLBACKS = {
    "simulate-button": update_params_and_simulate,
    "run-fitting-button": update_params_and_fit,
    "refresh-button": reset_params_body,
    "trigger-table-update": update_params_body,
    "delete": delete_param,
}
