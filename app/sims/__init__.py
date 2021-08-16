# -*- coding: utf-8 -*-
import datetime

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Simulator
from mrsimulator.signal_processing import SignalProcessor
from mrsimulator.utils.spectral_fitting import add_csdm_dvs

from . import navbar
from .features import features_body
from .fit_report import fit_report_body
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
    # store graph view data.
    dcc.Store(id="graph-view-layout", storage_type="memory", data=[]),
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
body_content = [
    home_body,
    spin_system_body,
    method_body,
    features_body,
    fit_report_body,
    spectrum_body,
]
main_body = html.Div(body_content, className="mobile-scroll")

# temp items
temp = [html.Div(id=f"temp{i}") for i in range(10)]

# content page
content = html.Div([*temp, main_body, store_items, bottom_nav], className="app-1")

# main app content
mrsimulator_app = html.Div(
    [top_nav, html.Div([sidebar, content], className="mrsim-page")]
)


# ==================================================================================== #

# Main function. Evaluates the spectrum and update the plot.
@app.callback(
    Output("alert-message-simulation", "children"),
    Output("alert-message-simulation", "is_open"),
    # Output("local-computed-data", "data"),
    Output("local-simulator-data", "data"),
    Output("graph-view-layout", "data"),
    Input("local-mrsim-data", "data"),
    State("graph-view-layout", "data"),
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
    n_sys = 1 if "spin_systems" not in mrsim_data else len(mrsim_data["spin_systems"])

    if mrsim_data is None:
        raise PreventUpdate

    if len(mrsim_data["methods"]) == 0:
        mrsim_data["timestamp"] = datetime.datetime.now()
        return [no_update, no_update, mrsim_data, no_update]

    try:
        sim = Simulator.parse_dict_with_units(mrsim_data)
        decompose = sim.config.decompose_spectrum[:]
        sim.config.decompose_spectrum = "spin_system"
        sim.run()
        sim.config.decompose_spectrum = decompose
    except Exception as e:
        return [f"SimulationError: {e}", True, no_update, no_update]

    process_data = mrsim_data["signal_processors"]
    for proc, mth in zip(process_data, sim.methods):
        processor = SignalProcessor.parse_dict_with_units(proc)

        # Adjust baseline offset for multi-spin_system spectra
        # Otherwise given baseline offset will be multiplied by number of spin_systems
        # (future) need to adjust polynomial as well when implemented
        for op in processor.operations:
            if op.__class__.__name__ == "ConstantOffset":
                op.offset = op.offset / n_sys

        mth.simulation = processor.apply_operations(data=mth.simulation).real

    if decompose == "none":
        for mth in sim.methods:
            mth.simulation = add_csdm_dvs(mth.simulation)

    serialize = sim.json(include_methods=True, include_version=True)
    serialize["signal_processors"] = process_data

    layout = ctx.states["graph-view-layout.data"]
    # for _ in range(len(sim.methods)-len(layout)):
    #     layout.append(None)

    # for i, mth in enumerate(sim.methods):
    #     if layout[i] is None:
    #         if len(mth.simulation.x) == 1:
    #             x = mth.simulation.x[0].coordinates.value
    #             y = mth.simulation.y[0].components[0].real
    #             layout[i] = {
    #                 'xaxis': {"range": [x.max(), x.min()]},
    #                 'yaxis': {"range": [y.min(), y.max()]}
    #             }

    return ["", False, serialize, layout]


@app.callback(
    Output("nmr_spectrum", "figure"),
    Output("local-processed-data", "data"),
    # Input("local-computed-data", "modified_timestamp"),
    Input("local-simulator-data", "data"),
    Input("normalize_amp", "n_clicks"),
    Input("select-method", "value"),
    State("normalize_amp", "active"),
    # State("local-computed-data", "data"),
    State("nmr_spectrum", "figure"),
    State("graph-view-layout", "data"),
    prevent_initial_call=True,
)
def plot(*args):
    """Generate and return a one-dimensional plot instance."""
    # time_of_computation = ctx.inputs["local-computed-data.modified_timestamp"]
    trigger = ctx.triggered[0]["prop_id"]
    trigger_id = trigger.split(".")[0]

    sim_data = ctx.inputs["local-simulator-data.data"]

    if sim_data is None:
        return [DEFAULT_FIGURE, no_update]

    if sim_data["methods"] == []:
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

    if trigger == "normalize_amp.n_clicks":
        normalized = not normalized

    decompose = False
    if "decompose_spectrum" in sim_data["config"]:
        decompose = sim_data["config"]["decompose_spectrum"] == "spin_system"

    print("plot trigger, trigger id", trigger, trigger_id)

    dim_axes = None
    plot_trace = []
    if experiment_data is not None:
        dim_axes = made_dimensionless(experiment_data)
        exp_data = cp.parse_dict(experiment_data).real
        plot_trace += get_plot_trace(
            exp_data,
            normalized,
            decompose=False,
            name="experiment",
            dimensionless_axes=dim_axes,
        )

    if simulation_data is not None:
        sim_data = cp.parse_dict(simulation_data).real
        plot_trace += get_plot_trace(
            sim_data,
            normalized,
            decompose=decompose,
            name="simulation",
            dimensionless_axes=dim_axes,
        )

    if experiment_data is not None and simulation_data is not None:
        index = [-i - 1 for i, x in enumerate(exp_data.x) if x.increment.value < 0]
        residue = exp_data.copy()
        sim_sum = np.asarray([y.components for y in sim_data.y]).sum(axis=0)
        residue.y[0].components -= np.flip(sim_sum, axis=tuple(index))
        plot_trace += get_plot_trace(
            residue,
            normalized,
            decompose=decompose,
            name="residual",
            dimensionless_axes=dim_axes,
        )

    layout = figure["layout"]
    # layout_graph = ctx.states['graph-view-layout.data'][method_index]
    # layout.update(layout_graph)

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


def made_dimensionless(exp):
    return [
        False
        if "origin_offset" not in item
        else cp.ScalarQuantity(item["origin_offset"]).quantity.value != 0
        for item in exp["csdm"]["dimensions"]
    ]


def get_plot_trace(data, normalized, decompose=False, name="", dimensionless_axes=None):
    plot_trace = []

    dimensionless_axes = (
        dimensionless_axes
        if dimensionless_axes is not None
        else [True] * len(data.dimensions)
    )
    _ = [
        dim.to("ppm", "nmr_frequency_ratio")
        for item, dim in zip(dimensionless_axes, data.dimensions)
        if item
    ]

    if len(data.dimensions) == 1:
        plot_trace += plot_1D_trace(data, normalized, decompose, name)

    if len(data.dimensions) == 2:
        plot_trace += plot_2D_trace(data, normalized, decompose)

    return plot_trace
