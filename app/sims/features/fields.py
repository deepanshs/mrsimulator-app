# -*- coding: utf-8 -*-
from datetime import datetime

import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


# TODO: Need to implement modals
# TODO: Need to implement fit-report


def input_tables():
    """Returns spin_system and method tables"""
    sys_table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(),
                        html.Th("Spin System", id="sys-feature-title"),
                        html.Th("Value"),
                        html.Th(),
                    ]
                )
            ),
            html.Tbody(id="sys-feature-rows", className="feature-rows"),
        ],
        id="sys-feature-table",
    )
    mth_table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th(),
                        html.Th("Method", id="mth-feature-title"),
                        html.Th("Value"),
                        html.Th(),
                    ]
                )
            ),
            html.Tbody(id="mth-feature-rows", className="feature-rows"),
        ],
        id="mth-feature-table",
    )

    return [sys_table, mth_table]


def hidden_buttons():
    """Hidden buttons to detach callbacks"""
    return [
        html.Button(id="make-lmfit-params", className="hidden"),
        html.Button(id="reload-param-groups", className="hidden"),
        html.Button(id="refresh-groups-and-tables", className="hidden"),
    ]


def ui():
    """Main UI for fitting interface"""
    content = input_tables() + hidden_buttons()
    return html.Div(
        children=content,
        id="input-fields",
        className="fit-scroll",
    )


fields = ui()


# JavaScript Callbacks =================================================================
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="reloadParamGroups"),
    Output("temp3", "children"),
    Input("reload-param-groups", "n_clicks"),
    Input("local-mrsim-data", "data"),
    prevent_initial_call=True,
)


# callback for refreshing data in both tables
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="refreshTables"),
    Output("temp4", "children"),
    Input("refresh-groups-and-tables", "n_clicks"),
    Input("view-features", "n_clicks"),
    State("sys-feature-select", "value"),
    State("mth-feature-select", "value"),
    prevent_initial_call=True,
)


# callback for clicking refresh button after a fit routine
app.clientside_callback(
    """function (processed_data_ts, fit_ts) {
        if (processed_data_ts > fit_ts) {
            document.getElementById("refresh-groups-and-tables").click();
        }
        return null;
    }
    """,
    Output("temp5", "children"),
    Input("local-processed-data", "modified_timestamp"),  # int (timestamp)
    State("trigger-fit", "modified_timestamp"),  # int (timestamp)
    prevent_initial_call=True,
)


# callback for causing a simulation or fitting routine
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="triggerSimOrFit"),
    Output("params-data", "data"),  # JSON str
    Output("trigger-sim", "data"),  # flag (timestamp)
    Output("trigger-fit", "data"),  # flag (timestamp)
    Input("trigger-params-update", "data"),  # flag (timestamp)
    Input("which-workflow", "data"),  # flag ("fit" or "sim")
    prevent_initial_call=True,
)

# TODO: Callback for opening modal


# callback for updating sys value
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="selectNewSys"),
    Output("temp6", "children"),
    Input("sys-feature-select", "value"),
    prevent_initial_call=True,
)


# callback for updating mth value
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="selectNewMth"),
    Output("temp7", "children"),
    Input("mth-feature-select", "value"),
    prevent_initial_call=True,
)


# Callbacks ============================================================================
@app.callback(
    Output("trigger-params-update", "data"),  # flag (timestamp)
    Output("which-workflow", "data"),  # flag ("fit" or "sim")
    Input("sim-button", "n_clicks"),  # Button
    Input("fit-button", "n_clicks"),  # Button
    prevent_initial_call=True,
)
def run_fit_or_sim(n1, n2):
    """Callback to begin a fit routine or simulation. Cascades into JS callback"""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("fit or sim", trigger_id)

    return int(datetime.now().timestamp() * 1000), trigger_id[:3]


@app.callback(
    Output("sys-feature-select", "options"),  # list of dict
    Output("mth-feature-select", "options"),  # list of dict
    Output("sys-feature-select", "value"),  # int
    Output("mth-feature-select", "value"),  # int
    Input("local-mrsim-data", "data"),
    State("sys-feature-select", "value"),
    State("mth-feature-select", "value"),
)
def update_feature_select_buttons(mrsim_data, sys_idx, mth_idx):
    """Updates feature select values to reflect number of spin_systems and methods"""
    n_sys = len(mrsim_data["spin_systems"])
    n_mth = len(mrsim_data["methods"])

    print(f"Update feature select: sys - {n_sys}, mth - {n_mth}")

    sys_options = [{"label": i, "value": i} for i in range(n_sys)]
    mth_options = [{"label": i, "value": i} for i in range(n_mth)]

    # Current selected spin_system out of range
    if sys_idx is None or sys_idx > n_sys:
        sys_idx = 0

    # Current selected method out of range
    if mth_idx is None or mth_idx > n_sys:
        mth_idx = 0

    return sys_options, mth_options, sys_idx, mth_idx
