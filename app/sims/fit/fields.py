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

from .fit_modal import make_modal
from app import app


CSS_STR = "*{font-family:'Helvetica',sans-serif;}td{padding: 0 8px}"
# TITLE = {"sys": "Spin System", "mth": "Method", "SP": "Method"}
GROUPING = {"Spin System": ["sys"], "Method": ["mth", "SP"]}
GROUP_WIDTH = 5  # How many table choices are on each page


def inputs():
    """Parameters tables html div"""
    sys_tables = html.Div(id="sys-tables-div", children="Presh refresh to load tables")
    mth_tables = html.Div(id="mth-tables-div", children=[])
    return html.Div([sys_tables, mth_tables])


def modals():
    """Hidden modals div"""
    sys_modals = html.Div(id="sys-modals-div", children=[])
    mth_modals = html.Div(id="mth-modals-div", children=[])
    return html.Div([sys_modals, mth_modals])


def ui():
    """Main UI for fitting interface"""
    return html.Div(
        children=[inputs(), modals()],
        id="input-fields",
        className="fit-scroll",
    )


fields = ui()


# Callbacks ============================================================================
# TODO: Have tables update after fitting routine
@app.callback(
    Output("sys-tables-div", "children"),  # List of tables
    Output("mth-tables-div", "children"),  # List of tables
    Output("sys-modals-div", "children"),  # List of modals
    Output("mth-modals-div", "children"),  # List of modals
    Output({"key": "table-select-btn", "title": "Spin System"}, "value"),  # int
    Output({"key": "table-select-btn", "title": "Method"}, "value"),  # int
    Output({"key": "table-select-btn", "title": "Spin System"}, "options"),  # dict list
    Output({"key": "table-select-btn", "title": "Method"}, "options"),  # dict list
    Output("fit-report-iframe", "srcDoc"),  # html string
    Output("fit-report-iframe", "hidden"),  # bool
    Output("params-data", "data"),
    Output("trigger-sim", "data"),
    Output("trigger-fit", "data"),
    Input({"kind": "delete", "name": ALL}, "n_clicks"),
    Input("page-sys-left-btn", "n_clicks"),
    Input("page-sys-right-btn", "n_clicks"),
    Input("page-mth-left-btn", "n_clicks"),
    Input("page-mth-right-btn", "n_clicks"),
    Input("refresh-button", "n_clicks"),
    Input("simulate-button", "n_clicks"),
    Input("run-fitting-button", "n_clicks"),
    State("local-mrsim-data", "data"),
    State("params-data", "data"),
    State({"key": "table-select-btn", "title": "Spin System"}, "value"),
    State({"key": "table-select-btn", "title": "Method"}, "value"),
    State({"kind": "name", "name": ALL}, "children"),  # Requires states to be generated
    State({"kind": "value", "name": ALL}, "value"),  # to be made in the order which
    State({"kind": "vary", "name": ALL}, "checked"),  # they appear on the page.
    State({"kind": "min", "name": ALL}, "value"),
    State({"kind": "max", "name": ALL}, "value"),
    State({"kind": "expr", "name": ALL}, "value"),
    prevent_initial_call=True,
)
def update_fit_elements(n1, n2, n3, n4, n5, n6, n7, n8, mrd, pd, sysi, mthi, *vals):
    "Main fitting callback dealing with visible elements"
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fit elements", trigger_id)

    if trigger_id.startswith("{"):
        py_dict = json.loads(trigger_id)
        name, trigger_id = py_dict["name"], py_dict["kind"]
        return CALLBACKS[trigger_id](name, vals)

    return CALLBACKS[trigger_id](vals)


# Sets visibility of selected spin system and method
# NOTE: When `GROUP_WIDTH` is changed, first statement must be adjusted also
app.clientside_callback(
    """function (set_index, className_list) {
        // Adjust set_index to conform to `GROUP_WIDTH`
        set_index = set_index % 5;
        // Set first table active if no active table
        if (!className_list.includes("fields-table active")) {
            className_list[0] = "fields-table active";
            return className_list;
        }
        // Set current active table to inactive and set_index table to active
        let active_index = className_list.indexOf("fields-table active");
        className_list[active_index] = "fields-table";
        className_list[set_index] = "fields-table active";
        return className_list;
    }""",
    Output({"key": "fit-table", "index": ALL, "title": MATCH}, "className"),
    Input({"key": "table-select-btn", "title": MATCH}, "value"),
    State({"key": "fit-table", "index": ALL, "title": MATCH}, "className"),
    prevent_initial_call=True,
)


# Reveals feature select UI when refresh button is pressed
# NOTE: Will reveal selection UI even if no loaded data
app.clientside_callback(
    """function (n1) { return false; }""",
    Output("feature-select-div", "hidden"),
    Input("refresh-button", "n_clicks"),
    prevent_initial_call=True,
)


# Helper Methods =======================================================================
def update_params_and_simulate(vals):
    """Updates stored Parameters object JSON and triggers a simulation"""
    params_data = ctx.states["params-data.data"]
    mrsim_data = ctx.states["local-mrsim-data.data"]

    if len(mrsim_data["spin_systems"]) == 0 or len(mrsim_data["methods"]) == 0:
        raise PreventUpdate

    new_data = update_params_obj(params_data=params_data, vals=vals).dumps()

    return expand_out(
        {
            "tables": [no_update] * 2,
            "modals": [no_update] * 2,
            "options": [no_update] * 4,
            "report": [no_update] * 2,
            "data": [new_data],
            "triggers": [int(datetime.now().timestamp() * 1000), no_update],
        }
    )


def update_params_and_fit(vals):
    """Updates stored Parameters object JSON and triggers fitting"""
    if file_is_empty():
        raise PreventUpdate

    params_data = ctx.states["params-data.data"]
    new_data = update_params_obj(params_data=params_data, vals=vals).dumps()

    return expand_out(
        {
            "tables": [no_update] * 2,
            "modals": [no_update] * 2,
            "options": [no_update] * 4,
            "report": [no_update] * 2,
            "data": [new_data],
            "triggers": [no_update, int(datetime.now().timestamp() * 1000)],
        }
    )


def delete_param(name, vals):
    """Deletes specified param (row) from interface"""
    if file_is_empty():
        raise PreventUpdate

    params_data = ctx.states["params-data.data"]
    sys_index = ctx.states['{"key":"table-select-btn","title":"Spin System"}.value']
    mth_index = ctx.states['{"key":"table-select-btn","title":"Method"}.value']

    params_obj = update_params_obj(params_data=params_data, vals=vals)
    name = name.split("-")[1]
    del params_obj[name]
    new_data = params_obj.dumps()

    sys_params, mth_params = group_params(params_obj_to_dict(params_obj))
    sys_tables, *_ = make_new_page_elements(
        params=sys_params, index=sys_index, title="Spin System"
    )
    mth_tables, *_ = make_new_page_elements(
        params=mth_params, index=mth_index, title="Method"
    )
    out = {
        "tables": [sys_tables, mth_tables],
        "modals": [no_update] * 2,
        "options": [no_update] * 4,
        "report": [no_update] * 2,
        "data": [new_data],
        "triggers": [no_update] * 2,
    }

    return expand_out(out)


def page_sys_tables_left(vals):
    return page_tables(name="Spin Systems", _dir="left", vals=vals)


def page_sys_tables_right(vals):
    return page_tables(name="Spin Systems", _dir="right", vals=vals)


def page_mth_tables_left(vals):
    return page_tables(name="Methods", _dir="left", vals=vals)


def page_mth_tables_right(vals):
    return page_tables(name="Methods", _dir="right", vals=vals)


def page_tables(name="", _dir="", vals=[]):
    """Updates current table page params and pages to the next table group"""
    if name not in ["Spin Systems", "Methods"] or _dir not in ["left", "right"]:
        raise PreventUpdate

    if file_is_empty():
        raise PreventUpdate

    params_data = ctx.states["params-data.data"]
    sys_index = ctx.states['{"key":"table-select-btn","title":"Spin System"}.value']
    mth_index = ctx.states['{"key":"table-select-btn","title":"Method"}.value']

    params_obj = update_params_obj(params_data=params_data, vals=vals)
    new_data = params_obj.dumps()
    sys_params, mth_params = group_params(params_obj_to_dict(params_obj))

    if name == "Spin Systems":
        sys_tables, sys_modals, sys_value, sys_options = make_new_page_elements(
            params=sys_params, index=sys_index, title="Spin System", _dir=_dir
        )
        out = {
            "tables": [sys_tables, no_update],
            "modals": [sys_modals, no_update],
            "options": [sys_value, no_update, sys_options, no_update],
            "report": [no_update] * 2,
            "data": [new_data],
            "triggers": [no_update] * 2,
        }
    elif name == "Methods":
        mth_tables, mth_modals, mth_values, mth_options = make_new_page_elements(
            params=mth_params, index=mth_index, title="Method", _dir=_dir
        )
        out = {
            "tables": [no_update, mth_tables],
            "modals": [no_update, mth_modals],
            "options": [no_update, mth_values, no_update, mth_options],
            "report": [no_update] * 2,
            "data": [new_data],
            "triggers": [no_update] * 2,
        }

    return expand_out(out)


def reset_params_body(*args):
    return update_tables(*args, reset=True)


def update_params_body(*args):
    return update_tables(*args)


def update_tables(*args, reset=False):
    data = ctx.states["local-mrsim-data.data"]
    sys_index = ctx.states['{"key":"table-select-btn","title":"Spin System"}.value']
    mth_index = ctx.states['{"key":"table-select-btn","title":"Method"}.value']

    if file_is_empty():
        raise PreventUpdate

    sim, processor, report = parse(data)

    if "params" in data and data["params"] is not None and not reset:
        params_obj = Parameters().loads(data["params"])
    else:
        params_obj = make_LMFIT_params(sim, processor, include={"rotor_frequency"})

    sys_params, mth_params = group_params(params_obj_to_dict(params_obj))

    # Check if selected indexes are out of bounds
    if sys_index is None or sys_index > len(sys_params):
        sys_index = 0
    if mth_index is None or mth_index > len(mth_params):
        mth_index = 0

    sys_tables, sys_modals, sys_value, sys_options = make_new_page_elements(
        params=sys_params, index=sys_index, title="Spin System"
    )
    mth_tables, mth_modals, mth_value, mth_options = make_new_page_elements(
        params=mth_params, index=mth_index, title="Method"
    )

    out = {  # `tables` and `modals` are unpacked in `expand_out`
        "tables": [sys_tables, mth_tables],
        "modals": [sys_modals, mth_modals],
        "options": [sys_value, mth_value, sys_options, mth_options],
        "report": ["", True] if "report" not in data else [data["report"], False],
        "data": [params_obj.dumps()],
        "triggers": [no_update] * 2,
    }

    return expand_out(out)


def group_params(params_dict):
    """Groups params_dict based on `GROUPING`

    Params:
        params_dict: dict reporesentation of whole Parameters object

    Returns:
        sys_group: list of spin system (dict, int, str) tuples
        mth_group: list of method (dict, int, str) tuples
    """
    sys_group, mth_group = [], []
    keys = sorted(list(params_dict.keys()), key=lambda x: int(x.split("_")[1]))

    if len(keys) == 0:
        return {}

    tmp_sys, tmp_mth = [], []
    index_sys, index_mth = 0, 0
    for key in keys:
        group, index = key.split("_")[0], int(key.split("_")[1])
        if group in GROUPING["Spin System"]:
            if index_sys != index:
                sys_group.append(({k: params_dict[k] for k in tmp_sys}, index_sys))
                index_sys += 1
                tmp_sys = []
            tmp_sys += [key]
        elif group in GROUPING["Method"]:
            if index_mth != index:
                mth_group.append(({k: params_dict[k] for k in tmp_mth}, index_mth))
                index_mth += 1
                tmp_mth = []
            tmp_mth += [key]

    sys_group.append(({k: params_dict[k] for k in tmp_sys}, index_sys))
    mth_group.append(({k: params_dict[k] for k in tmp_mth}, index_mth))
    return sys_group, mth_group


# Truncate decimal places (using css?)
def fit_table(_dict, index, title="Name"):
    """Constructs html table of parameter inputs fields

    Params:
        _dict: slice from dict representation of Parameters object
        index: index of table used for callback visibility
        title: string to display in second column header

    Returns:
        html.Table
    """
    fit_header = ["", f"{title} {index}", "Value", "", ""]
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
        className="fields-table active"
        if index == 0
        else "fields-table",  # index check will change w/ pages
        children=fit_rows,
        id={"key": "fit-table", "index": index, "title": title},
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


def make_new_page_elements(params, index, title, _dir=None):
    """Helper for making new tables, modals, and options

    Params:
        params: dict representation of single Parameter object
        index: index of the parameter
        title: title added to table header
        _dir: weather to page left or right

    Returns:
        new_tables: list of html.Table
        new_modals: list of dbc.Modal
        new_value: int of current table index
        new_options: dict of options for table select buttons
    """
    num_tables = len(params)
    page_index = index // GROUP_WIDTH
    new_value = index

    # Move page index left or right (+1 or -1)
    if _dir == "left":
        page_index = max(page_index - 1, 0)
        # Do not update if `page_index` has not changed (for efficency)
        if page_index == index // GROUP_WIDTH:
            raise PreventUpdate
        new_value = page_index * GROUP_WIDTH
    elif _dir == "right":
        page_index = min(page_index + 1, (num_tables - 1) // GROUP_WIDTH)
        # Do not update if `page_index` has not changed (for efficency)
        if page_index == index // GROUP_WIDTH:
            raise PreventUpdate
        new_value = page_index * GROUP_WIDTH

    opt_min = page_index * GROUP_WIDTH
    opt_max = min((page_index + 1) * GROUP_WIDTH, num_tables)

    new_params = [
        tup for tup in params if page_index <= tup[1] // GROUP_WIDTH < page_index + 1
    ]

    # Make new tables, modals and options
    new_tables = [fit_table(*item, title) for item in new_params]
    new_modals = [make_modal(k, v) for param in new_params for k, v in param[0].items()]
    new_options = [{"label": i, "value": i} for i in range(opt_min, opt_max)]

    return new_tables, new_modals, new_value, new_options


def update_params_obj(params_data, vals):
    """Update Parameters object from rendered tables

    Params:
        params_data: JSON string
        vals: currently rendered fields

    Returns:
        Parameters object
    """
    params_obj = Parameters().loads(params_data)
    zip_vals = list(zip(*vals))

    for row in zip_vals:
        del params_obj[row[0]]  # Delete Paremeter by name
        params_obj.add(*row)

    return params_obj


def file_is_empty():
    """Returns True if loaded file is empty, false otherwise"""
    mrsim_data = ctx.states["local-mrsim-data.data"]
    return len(mrsim_data["spin_systems"]) == 0 or len(mrsim_data["methods"]) == 0


CALLBACKS = {
    "simulate-button": update_params_and_simulate,
    "run-fitting-button": update_params_and_fit,
    "refresh-button": reset_params_body,
    "page-sys-left-btn": page_sys_tables_left,
    "page-sys-right-btn": page_sys_tables_right,
    "page-mth-left-btn": page_mth_tables_left,
    "page-mth-right-btn": page_mth_tables_right,
    "trigger-table-update": update_params_body,
    "delete": delete_param,
}


def expand_out(out):
    """Helper method for return values of `update_fit_elements`"""
    return [
        *out["tables"],
        *out["modals"],
        *out["options"],
        *out["report"],
        *out["data"],
        *out["triggers"],
    ]
