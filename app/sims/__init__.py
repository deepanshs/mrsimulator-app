# -*- coding: utf-8 -*-
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

# from .method.post_simulation_widgets import appodization_ui
# from .methods.post_simulation_functions import line_broadening
# from .methods.post_simulation_functions import post_simulation

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# storage data
store = [
    # memory for holding the spin systems data.
    dcc.Store(id="local-mrsim-data", storage_type="session"),
    # memort for storing local simulator data.
    dcc.Store(id="local-simulator-data", storage_type="memory"),
    # memory for storing the experimental data
    dcc.Store(id="local-exp-external-data", storage_type="memory"),
    # memory for storing the local computed data.
    dcc.Store(id="local-computed-data", storage_type="memory"),
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
    dcc.Store(id="signal-processor-data", storage_type="memory"),
    dcc.Store(id="signal-processor-data-temp", storage_type="memory"),
]
store_items = html.Div(store)

# aler items
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

# top navbar items
top_nav = html.Div([navbar.navbar_top, simulation_alert, import_alert, graph_alert])

# bottom navbar items
bottom_nav = navbar.navbar_bottom
# main bodt items
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


def check_for_spin_system_update(new, old):
    """Return True if the spin system is updates, else False. For simulation, the system
    is considered unchanged when metadata such as name and description is modified."""
    if old is None:
        return True

    print(new["spin_systems"], old["spin_systems"])
    size1 = len(new["spin_systems"])
    size2 = len(old["spin_systems"])
    if size1 != size2:
        return True

    features = [
        "isotope",
        "isotropic_chemical_shift",
        "shielding_symmetric",
        "quadrupolar",
    ]

    for i in range(size1):
        s_1 = len(new["spin_systems"][i]["sites"])
        s_2 = len(new["spin_systems"][i]["sites"])
        if s_1 != s_2:
            return True
        for j in range(s_1):
            site_new = new["spin_systems"][i]["sites"][j]
            site_old = old["spin_systems"][i]["sites"][j]

            for item in features:
                if site_new[item] != site_old[item]:
                    return True

    return False


def check_if_old_and_new_spin_systems_data_are_equal(new, old):
    """Check if the two spin_systems are the same. This does not include the
    name and the description of the spin_systems."""
    size1 = len(new["spin_systems"])
    size2 = len(old["spin_systems"])
    size_min = min(size1, size2)

    true_index = [False] * size1
    for i in range(size_min):
        if new["spin_systems"][i]["sites"] == old["spin_systems"][i]["sites"]:
            true_index[i] = True

    return true_index


def check_for_simulation_update(
    isotope_id,
    config,
    local_spin_systems_data,
    previous_local_computed_data,
    previous_local_spin_system_index_map,
    figure,
):
    """
    Check if the simulation needs to update. The check search for
    1) If the simulation on display has a different isotope than the isotope requested
        for simulation, perform an update.
    2) If the display (from spectrum) and requested isotopes (from dimension) are the
        same, check if the last modified spin-system
        a) was triggered with a change of isotope. If true, check if the previously
            selected isotope was used in simulation. If yes, re-simulate, else prevent
            update.
        b) was triggered with any other site attribute. If true, check if the modified
            spin-system has the same isotope as on display. If yes, re-simulate, else,
            prevent update.
    """
    # checking for the first condition.
    isotope_on_graph = (
        figure["layout"]["xaxis"]["title"]["text"].split()[0]
        if previous_local_computed_data is not None
        else isotope_id
    )
    print("spectrum isotope", isotope_on_graph)
    if isotope_on_graph != isotope_id:
        return

    # cheking for the second condition.
    # the `index_last_modified` attribute of the config holds the index of the
    # spin-system that was last modified. Here, we check if the changes made to the
    # spin-system pertains the isotope used in the simulation. If the site isotopes
    # in the spin-system is not the same as `isotope_id`, prevent the update.
    modified_index = config["index_last_modified"]
    if modified_index is None:
        raise PreventUpdate

    # site isotopes in the modified spin-system
    modified_site_isotopes = [
        site["isotope"]
        for site in local_spin_systems_data["spin_systems"][modified_index]["sites"]
    ]

    if previous_local_computed_data is None:
        return
    # checking part a of the second condition
    # the previous_local_spin_system_index_map contains a list of spin-system indexes
    # that were used in the simulation. To check if the identity of the isotope changed
    # in the modified spin-system, we compare the identity of the isotopes from the
    # spin_systems from previous_local_computed_data.
    if modified_index in previous_local_spin_system_index_map:

        index_in_computed_data = np.where(
            np.asarray(previous_local_spin_system_index_map) == modified_index
        )[0][0]
        print(index_in_computed_data)
        dv = previous_local_computed_data["csdm"]["dependent_variables"][
            index_in_computed_data
        ]
        previous_site_isotopes = [
            site["isotope"]
            for site in dv["application"]["com.github.DeepanshS.mrsimulator"][
                "spin_systems"
            ][0]["sites"]
        ]
        if modified_site_isotopes != previous_site_isotopes:
            return

    # checking part b of the second condition
    if isotope_on_graph not in modified_site_isotopes:
        print(
            "update pervented because the changes does not involve "
            f"{isotope_id} isotope."
        )
        raise PreventUpdate


# Main function. Evaluates the spectrum and update the plot.
@app.callback(
    [
        Output("alert-message-simulation", "children"),
        Output("alert-message-simulation", "is_open"),
        Output("local-computed-data", "data"),
        Output("local-simulator-data", "data"),
    ],
    [Input("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
def simulation(local_mrsim_data):
    """Evaluate the spectrum and update the plot."""

    if not ctx.triggered:
        print("simulation stopped, ctx not triggered")
        raise PreventUpdate

    if local_mrsim_data is None:
        raise PreventUpdate

    if len(local_mrsim_data["methods"]) == 0:
        raise PreventUpdate

    if len(local_mrsim_data["spin_systems"]) == 0:
        raise PreventUpdate

    if "trigger" in local_mrsim_data:
        if not local_mrsim_data["trigger"]:
            raise PreventUpdate
    # if not check_for_spin_system_update(local_mrsim_data, previous_local_mrsim_data):
    #     raise PreventUpdate

    print("simulate")
    try:
        sim = Simulator(**local_mrsim_data)
        sim.run()

    except Exception as e:
        return [str(e), True, no_update, no_update]

    local_computed_data = [
        item.simulation.to_dict(update_timestamp=True) for item in sim.methods
    ]

    return [
        "",
        False,
        local_computed_data,
        sim.json(include_methods=True, include_version=True),
    ]


# @app.callback(
#     [
#         Output("dim-reference_offset-0", "value"),
#         Output("dim-spectral_width-0", "value"),
#     ],
#     [Input("nmr_spectrum", "relayoutData")],
#     [State("local-method-data", "data")],
# )
# def display_relayout_data(relayoutData, method_data):
#     if None in [relayoutData, method_data]:
#         raise PreventUpdate

#     keys = relayoutData.keys()

#     if method_data["larmor_frequency"] is None:
#         raise PreventUpdate
#     if "yaxis.range[0]" in keys or "yaxis.range[1]" in keys:
#         raise PreventUpdate
#     if "xaxis.range[0]" not in keys and "xaxis.range[1]" not in keys:
#         raise PreventUpdate

#     # Check larmor frequency and ppm scale. Current scale is in Hz
#     larmor_frequency = 1
#     # larmor_frequency = abs(method_data["larmor_frequency"])  # in MHz

#     # old increment
#     dim = method_data["spectral_dimensions"][0]
#     sw = float(dim["spectral_width"])  # in Hz
#     increment = float(sw / dim["count"])  # in Hz
#     rf = float(dim["reference_offset"])  # in Hz

#     # new x-min in Hz, larmor_frequency is in MHz
#     if "xaxis.range[0]" in keys and relayoutData["xaxis.range[0]"] is not None:
#         x_min = relayoutData["xaxis.range[0]"] * larmor_frequency
#     else:
#         x_min = sw / 2.0 + rf - increment

#     # new x-max in Hz, larmor_frequency is in MHz
#     if "xaxis.range[1]" in keys and relayoutData["xaxis.range[1]"] is not None:
#         x_max = relayoutData["xaxis.range[1]"] * larmor_frequency
#     else:
#         x_max = -sw / 2.0 + rf

#     # new spectral-width and reference offset in Hz
#     sw_ = x_min - x_max + increment
#     ref_offset = x_max + sw_ / 2.0
#     return ["{0:.5f}".format(ref_offset / 1000.0),
#               "{0:.5f}".format(abs(sw_) / 1000.0)]


# @app.callback(Output("buffer", "children"), [Input("nmr_spectrum", "restyleData")])
# def getSelectedLegend(selected):
#     print("restyleData", selected)
#     raise PreventUpdate


@app.callback(
    [Output("nmr_spectrum", "figure"), Output("local-processed-data", "data")],
    [
        Input("local-computed-data", "modified_timestamp"),
        Input("local-simulator-data", "data"),
        Input("normalize_amp", "n_clicks"),
        Input("select-method", "value"),
        Input("signal-processor-data-temp", "data"),
    ],
    [
        State("normalize_amp", "active"),
        State("local-computed-data", "data"),
        State("nmr_spectrum", "figure"),
    ],
    prevent_initial_call=True,
)
def plot(*args):
    """Generate and return a one-dimensional plot instance."""
    time_of_computation = ctx.inputs["local-computed-data.modified_timestamp"]
    sim_data = ctx.inputs["local-simulator-data.data"]
    method_index = ctx.inputs["select-method.value"]

    normalized = ctx.states["normalize_amp.active"]
    local_computed_data = ctx.states["local-computed-data.data"]
    figure = ctx.states["nmr_spectrum.figure"]

    print("inside plot, time of computation", time_of_computation)
    print("method_index", method_index)
    # if method_index is None or method_options == []:
    # return [DEFAULT_FIGURE, no_update]

    if local_computed_data is None and sim_data is None:
        return [DEFAULT_FIGURE, no_update]

    # if not ctx.triggered:
    #     raise PreventUpdate

    trigger = ctx.triggered[0]["prop_id"]

    if trigger == "normalize_amp.n_clicks":
        normalized = not normalized

    trigger_id = trigger.split(".")[0]
    print("plot trigger, trigger id", trigger, trigger_id)

    # trigger_spin_system = (
    #     True
    #     if local_computed_data is None
    #     else local_computed_data["trigger-spin-system"]
    # )
    # print("local_computed_data", local_computed_data)
    plot_trace = []

    if local_computed_data is not None:
        local_computed_data = [cp.parse_dict(item) for item in local_computed_data]
        process_data = ctx.inputs["signal-processor-data-temp.data"]
        if process_data is not None:
            local_processed_data = []
            print(process_data)
            for proc, dat in zip(process_data, local_computed_data):
                processor = SignalProcessor.parse_dict_with_units(proc)
                local_processed_data.append(processor.apply_operations(data=dat).real)
            # print(local_processed_data)
        else:
            local_processed_data = local_computed_data
            # print(local_processed_data)

        # local_processed_data = [
        #     post_simulation(
        #         line_broadening,
        #         csdm_object=item,
        #         sigma=broadening,
        #         broadType=apodization,
        #     )
        #     for item in local_computed_data
        # ]

        current_data = local_processed_data[method_index]

        # try:
        [item.to("ppm", "nmr_frequency_ratio") for item in current_data.dimensions]
        # except (ZeroDivisionError, ValueError):
        #     pass

        decompose = sim_data["config"]["decompose_spectrum"] == "spin_system"

        if len(current_data.dimensions) == 1:
            plot_trace += plot_1D_trace(current_data, normalized, decompose)

        if len(current_data.dimensions) == 2:
            plot_trace += plot_2D_trace(current_data, normalized, decompose)

    mth = sim_data["methods"][method_index]
    local_experiment_data = None if "experiment" not in mth else mth["experiment"]

    if local_experiment_data is not None:
        local_experiment_data = cp.parse_dict(local_experiment_data)

        dimensions = [
            item.to("ppm", "nmr_frequency_ratio") or item.coordinates.value
            if item.origin_offset.value != 0
            else item.coordinates.to("Hz").value
            for item in local_experiment_data.dimensions
        ]
        # if local_experiment_data.dimensions[0].origin_offset.value != 0:
        #  local_experiment_data.dimensions[0].to("ppm", "nmr_frequency_ratio")
        #  x_spectrum = local_experiment_data.dimensions[0].coordinates.value
        # else:
        #  x_spectrum = local_experiment_data.dimensions[0].coordinates.to("Hz").value

        x_spectrum = dimensions[0]
        x0 = x_spectrum[0]
        dx = x_spectrum[1] - x_spectrum[0]
        y_spectrum = local_experiment_data.dependent_variables[0].components[0]
        if normalized:
            y_spectrum /= np.abs(y_spectrum.max())
        plot_trace.append(
            go.Scatter(
                x0=x0,
                dx=dx,
                y=y_spectrum.real,
                mode="lines",
                line={"color": "rgba(175, 0, 114, 0.494)", "width": 2.2},
                name="experiment",
            )
        )

    layout = figure["layout"]

    # if config is None or trigger in [
    #     "normalize_amp.n_clicks",
    #     "local-exp-external-data.modified_timestamp",
    # ]:
    #     print("axis update is True", config, trigger)
    #     layout["xaxis"]["autorange"] = True
    #     layout["yaxis"]["autorange"] = True
    # elif config["is_new_data"] and trigger_spin_system:
    #     print("axis update is True", config)
    #     layout["xaxis"]["autorange"] = True
    #     layout["yaxis"]["autorange"] = True

    layout["xaxis"]["autorange"] = "reversed"
    layout["yaxis"]["autorange"] = True
    # layout["xaxis"]["title"] = f"{isotope_id} frequency ratio / ppm"

    # print("isotope_id", isotope_id)
    # print("clickData", clickData)

    # if clickData is not None and decompose:
    #     layout["xaxis"]["autorange"] = False
    #     layout["yaxis"]["autorange"] = False
    #     index = clickData["points"][0]["curveNumber"]
    #     # data[index], data[-1] = data[-1], data[index]
    #     if index < len(data):
    #         data[index].line["width"] = 3.0
    #     # print("fillcolor", data[index].fillcolor)
    #     # for i in range(len(data)):
    #     #     if i != index:
    #     #         data[i].opacity = 0.25

    data_object = {"data": plot_trace, "layout": go.Layout(**layout)}

    if trigger_id in [
        "local-exp-external-data",
        "normalize_amp",
        # "nmr_spectrum",
    ]:
        return [data_object, no_update]
    if local_computed_data is None:
        return [data_object, no_update]

    local_processed_data = [item.to_dict() for item in local_processed_data]
    return [data_object, local_processed_data]
