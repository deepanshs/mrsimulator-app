# -*- coding: utf-8 -*-
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def input_tables():
    """Returns spinum_system and method tables"""
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
        # html.Button(id="reload-param-groups", className="hidden"),
        html.Button(id="refresh-groups-and-tables", className="hidden"),
        html.Button(id="close-features-modal", className="hidden"),
        html.Button(id="open-features-modal", className="hidden"),
        html.Button(id="force-refresh-method", className="hidden"),
    ]


def more_settings_modal():
    """More settings features modal for min, max and expr"""
    head = dbc.ModalHeader(
        [html.Div("More Options"), html.Div("", id="features-modal-subtitle")]
    )
    body = dbc.ModalBody(
        [
            html.Div(
                [
                    "Minimum",
                    dcc.Input(value=None, type="number", id="features-modal-min"),
                ]
            ),
            html.Div(
                [
                    "Maximum",
                    dcc.Input(value=None, type="number", id="features-modal-max"),
                ]
            ),
            html.Div(
                ["Expression", dbc.Textarea(value=None, id="features-modal-expr")]
            ),
        ]
    )
    foot = dbc.ModalFooter(dbc.Button("Save", id="features-modal-save"))

    return dbc.Modal([head, body, foot], id="features-modal", is_open=False)


def ui():
    """Main UI for fitting interface"""
    content = input_tables() + hidden_buttons()
    return html.Div(
        children=content,
        id="input-fields",
        className="fit-scroll",
    )


fields = ui()
features_modal = more_settings_modal()


# JavaScript Callbacks =================================================================
# app.clientside_callback(
#     ClientsideFunction(namespace="features", function_name="reloadParamGroups"),
#     Output("temp3", "children"),
#     Input("local-mrsim-data", "data"),
#     prevent_initial_call=True,
# )


# NOTE: This callback may be unneeded
# callback for refreshing data in both tables
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="refreshTables"),
    Output("temp4", "children"),
    Input("refresh-groups-and-tables", "n_clicks"),
    Input("view-features", "n_clicks"),
    # State("sys-feature-select", "value"),
    # State("mth-feature-select", "value"),
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


# Callback for opening features modal
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="openOrCloseModal"),
    Output("features-modal", "is_open"),
    Input("open-features-modal", "n_clicks"),
    Input("close-features-modal", "n_clicks"),
    Input("features-modal-save", "n_clicks"),
    prevent_initial_call=True,
)


# Callback for population modal fields after open
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="populateModalFields"),
    Output("temp7", "children"),
    Input("features-modal", "is_open"),
    prevent_initial_call=True,
)


# callback for updating feature select buttons
app.clientside_callback(
    ClientsideFunction(namespace="features", function_name="pageFeatureSelect"),
    Output("temp8", "children"),  # dummy
    Input("page-sys-feature-left", "n_clicks"),  # button
    Input("page-sys-feature-right", "n_clicks"),  # button
    Input("page-mth-feature-left", "n_clicks"),  # button
    Input("page-mth-feature-right", "n_clicks"),  # button
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
