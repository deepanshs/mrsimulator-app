# -*- coding: utf-8 -*-
import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Simulator
from mrsimulator.signal_processing import SignalProcessor

from . import navbar
from .fit import fit_body
from .graph import DEFAULT_FIGURE
from .graph import plot_1D_trace
from .graph import plot_2D_trace
from .graph import spectrum_body
from .home import home_body
from .method import method_body
from .sidebar import sidebar
from .spin_system import spin_system_body
from app import app
from app.utils import slogger

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"

DEFAULT_MRSIM_DATA = {
    "name": "",
    "description": "",
    "spin_systems": [],
    "methods": [],
    "config": {},
}

# storage data
store = [
    # memory for holding the spin systems data.
    dcc.Store(id="local-mrsim-data", storage_type="session", data=DEFAULT_MRSIM_DATA),
    # memory for storing local simulator data.
    dcc.Store(id="local-simulator-data", storage_type="memory"),
    # memory for storing the experimental data
    # dcc.Store(id="local-exp-external-data", storage_type="memory"),
    # memory for storing the local computed data.
    # dcc.Store(id="local-computed-data", storage_type="memory"),
    # memory for holding the computed + processed data. Processing over the
    # computed data is less computationally expensive.
    dcc.Store(id="local-processed-data", storage_type="memory"),
    # memory for holding the method data
    dcc.Store(id="local-method-data", storage_type="memory"),
    dcc.Store(id="new-spin-system", storage_type="memory"),
    dcc.Store(id="new-method", storage_type="memory"),
    # store a bool indicating if the data is from an external file
    dcc.Store(id="config", storage_type="memory"),
    # method-template data
    dcc.Store(id="add-method-from-template", storage_type="memory"),
    dcc.Store(id="user-config", storage_type="local"),
    # signal processor
]
store_items = html.Div(store)

# alert items
simulation_alert = dbc.Alert(
    id="alert-message-simulation",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

import_alert = dbc.Alert(
    id="alert-message-import",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

graph_alert = dbc.Alert(
    id="alert-message-spectrum",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

# top and bottom navbar items
top_nav = html.Div([navbar.navbar_top, simulation_alert, import_alert, graph_alert])
bottom_nav = navbar.navbar_bottom

# main body items
body_content = [home_body, spin_system_body, method_body, fit_body, spectrum_body]
main_body = html.Div(body_content, className="mobile-scroll")

# temp items
temp = [html.Div(id=f"temp{i}") for i in range(6)]

# content page
content = html.Div([*temp, main_body, store_items, bottom_nav], className="app-1")

# main app content
mrsimulator_app = html.Div(
    [top_nav, html.Div([sidebar, content], className="mrsim-page")]
)


# ==================================================================================== #

# Main function. Evaluates the spectrum and update the plot.
@app.callback(
    [
        Output("alert-message-simulation", "children"),
        Output("alert-message-simulation", "is_open"),
        # Output("local-computed-data", "data"),
        Output("local-simulator-data", "data"),
    ],
    [Input("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
def simulation(*args):
    """Evaluate the spectrum and update the plot."""

    if not ctx.triggered:
        slogger("simulation", "simulation stopped, ctx not triggered")
        raise PreventUpdate

    return one_time_simulation()


def one_time_simulation():
    mrsim_data = ctx.inputs["local-mrsim-data.data"]

    if mrsim_data is None:
        raise PreventUpdate

    if len(mrsim_data["methods"]) == 0 or len(mrsim_data["spin_systems"]) == 0:
        return [no_update, no_update, mrsim_data]

    try:
        sim = Simulator.parse_dict_with_units(mrsim_data)
        decompose = sim.config.decompose_spectrum[:]
        sim.config.decompose_spectrum = "spin_system"
        sim.run()
        sim.config.decompose_spectrum = decompose
    except Exception as e:
        return [f"SimulationError: {e}", True, no_update]

    process_data = mrsim_data["signal_processors"]
    for proc, mth in zip(process_data, sim.methods):
        processor = SignalProcessor.parse_dict_with_units(proc)
        mth.simulation = processor.apply_operations(data=mth.simulation).real

    if decompose == "none":
        for mth in sim.methods:
            mth.simulation = add_csdm_with_multiple_dv_to_one(mth.simulation)

    serialize = sim.json(include_methods=True, include_version=True)
    serialize["signal_processors"] = process_data

    return ["", False, serialize]


def add_csdm_with_multiple_dv_to_one(data):
    new_data = data.split()
    new_csdm = 0
    for item in new_data:
        new_csdm += item
    return new_csdm if new_data != [] else None


@app.callback(
    [Output("nmr_spectrum", "figure"), Output("local-processed-data", "data")],
    [
        # Input("local-computed-data", "modified_timestamp"),
        Input("local-simulator-data", "data"),
        Input("normalize_amp", "n_clicks"),
        Input("select-method", "value"),
    ],
    [
        State("normalize_amp", "active"),
        # State("local-computed-data", "data"),
        State("nmr_spectrum", "figure"),
    ],
    prevent_initial_call=True,
)
def plot(*args):
    """Generate and return a one-dimensional plot instance."""
    # time_of_computation = ctx.inputs["local-computed-data.modified_timestamp"]
    sim_data = ctx.inputs["local-simulator-data.data"]

    if sim_data is None:
        return [DEFAULT_FIGURE, no_update]

    if sim_data["methods"] == [] or sim_data["spin_systems"] == []:
        return [DEFAULT_FIGURE, no_update]

    method_index = ctx.inputs["select-method.value"]
    if method_index is None:
        raise PreventUpdate

    normalized = ctx.states["normalize_amp.active"]
    figure = ctx.states["nmr_spectrum.figure"]

    mth = sim_data["methods"][method_index]
    simulation_data = None if "simulation" not in mth else mth["simulation"]
    experiment_data = None if "experiment" not in mth else mth["experiment"]

    # [item["simulation"] for item in sim_data["methods"]]

    # print("inside plot, time of computation", time_of_computation)
    print("method_index", method_index)
    # if method_index is None or method_options == []:
    # return [DEFAULT_FIGURE, no_update]

    # if not ctx.triggered:
    #     raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if trigger == "normalize_amp.n_clicks":
        normalized = not normalized

    decompose = False
    if "decompose_spectrum" in sim_data["config"]:
        decompose = sim_data["config"]["decompose_spectrum"] == "spin_system"

    trigger_id = trigger.split(".")[0]
    print("plot trigger, trigger id", trigger, trigger_id)

    plot_trace = []
    if experiment_data is not None:
        plot_trace += get_plot_trace(
            experiment_data, normalized, decompose=False, name="experiment"
        )
    if simulation_data is not None:
        plot_trace += get_plot_trace(
            simulation_data, normalized, decompose=decompose, name="simulation"
        )

    layout = figure["layout"]
    layout["xaxis"]["autorange"] = "reversed"
    layout["yaxis"]["autorange"] = True

    data_object = {"data": plot_trace, "layout": go.Layout(**layout)}

    if trigger_id in [
        "local-exp-external-data",
        "normalize_amp",
        # "nmr_spectrum",
    ]:
        return [data_object, no_update]
    if simulation_data is None:
        return [data_object, no_update]

    # simulation_data = simulation_data.to_dict()
    # print(simulation_data)
    return [data_object, simulation_data]


def get_plot_trace(data, normalized, decompose=False, name=""):
    plot_trace = []
    data = cp.parse_dict(data).real
    [
        item.to("ppm", "nmr_frequency_ratio")
        for item in data.dimensions
        if item.origin_offset.value != 0
    ]
    if len(data.dimensions) == 1:
        plot_trace += plot_1D_trace(data, normalized, decompose, name)

    if len(data.dimensions) == 2:
        plot_trace += plot_2D_trace(data, normalized, decompose)

    return plot_trace
