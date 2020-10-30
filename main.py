# -*- coding: utf-8 -*-
import sys

import csdmpy as cp
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Simulator

from app.app import app
from app.body import app_1
from app.body import nav_group
from app.body import sidebar
from app.graph import DEFAULT_FIGURE
from app.methods.post_simulation_functions import line_broadening
from app.methods.post_simulation_functions import post_simulation

# from app_inv import mrinv
# from app_main import home_mrsims

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]


html_body = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # html.Div(id="placeholder"),
        html.A(id="url-search", href=""),
    ],
    className="main",
)

app.layout = html_body

server = app.server

# home = html.Div(
#     [
#         dcc.Link("Simulator", href="/simulator", id="simulator-app"),
#         dcc.Link("Inversion", href="/inversion", id="inversion-app"),
#         dcc.Link("Home", href="/home", id="home-app"),
#     ],
#     className="home-screen",
#     **{"data-app-link": ""},
# )
mrsimulator_app = html.Div(
    [nav_group, html.Div([sidebar, app_1], className="main-split")]
)

# layout_2 = mrinv
# layout_3 = home_mrsims


@app.callback(
    [Output("page-content", "children"), Output("url-search", "href")],
    [Input("url", "pathname")],
    [State("url", "search")],
)
def display_page(pathname, search):
    print(pathname)
    # if pathname == "/simulator":
    #     return [mrsimulator_app, search]
    # if pathname == "/inversion":
    #     return [layout_2, search]
    # if pathname == "/home":
    #     return [layout_3, search]
    # else:
    return [mrsimulator_app, search]


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="initialize"),
    Output("placeholder", "children"),
    [Input("simulator-app", "n_clicks")],
    prevent_initial_call=True,
)


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
        Output("local-spin-system-index-map", "data"),
    ],
    [Input("local-mrsim-data", "data")],
    [
        State("local-simulator-data", "data"),
        State("local-spin-system-index-map", "data"),
        State("config", "data"),
        State("nmr_spectrum", "figure"),
    ],
)
def simulation(
    # input
    local_mrsim_data,
    # state
    previous_local_mrsim_data,
    previous_local_spin_system_index_map,
    config,
    figure,
):
    """Evaluate the spectrum and update the plot."""
    # if "removed" in config.keys():
    #     raise PreventUpdate
    # exit when the following conditions are True
    # if isotope_id is None:
    #     if previous_local_computed_data is not None:
    #         print("simulation cleared because isotope id is", isotope_id)
    #         return [None, no_update, no_update]
    #     raise PreventUpdate

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
        return [str(e), True, no_update, no_update, no_update]

    local_computed_data = [
        item.simulation.to_dict(update_timestamp=True) for item in sim.methods
    ]

    return [
        "",
        False,
        local_computed_data,
        sim.to_dict_with_units(include_methods=True),
        sim.indexes,
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
        Input("broadening_points-0", "value"),
        Input("Apodizing_function-0", "value"),
        # Input("nmr_spectrum", "clickData"),
        Input("select-method", "value"),
        Input("select-method", "options"),
    ],
    [
        State("normalize_amp", "active"),
        State("local-computed-data", "data"),
        State("nmr_spectrum", "figure"),
        State("config", "data"),
    ],
)
def plot(
    time_of_computation,
    sim_data,
    normalized_clicked,
    broadening,
    apodization,
    # clickData,
    method_index,
    method_options,
    # state
    normalized,
    local_computed_data,
    figure,
    config,
):
    """Generate and return a one-dimensional plot instance."""
    print("inside plot, time of computation", time_of_computation)
    print("method_index", method_index, method_options)
    if method_index is None or method_options == []:
        return [DEFAULT_FIGURE, no_update]

    if local_computed_data is None and sim_data is None:
        return [DEFAULT_FIGURE, no_update]

    if not ctx.triggered:
        raise PreventUpdate

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
    data = []
    if local_computed_data is not None:
        local_computed_data = [cp.parse_dict(item) for item in local_computed_data]

        local_processed_data = [
            post_simulation(
                line_broadening,
                csdm_object=item,
                sigma=broadening,
                broadType=apodization,
            )
            for item in local_computed_data
        ]

        current_data = local_processed_data[method_index]

        try:
            [item.to("ppm", "nmr_frequency_ratio") for item in current_data.dimensions]
        except (ZeroDivisionError, ValueError):
            pass

        if len(current_data.dimensions) == 1:
            x = current_data.dimensions[0].coordinates.value
            x0 = x[0]
            dx = x[1] - x[0]

            # get the max data point
            y_data = 0
            maximum = 1.0
            for datum in current_data.split():
                y_data += datum

            if normalized:
                maximum = y_data.max()
                y_data /= maximum

            decompose = sim_data["config"]["decompose_spectrum"] == "spin_system"
            if decompose:
                for datum in current_data.dependent_variables:
                    name = datum.name
                    if name == "":
                        name = None
                    data.append(
                        go.Scatter(
                            x0=x0,
                            dx=dx,
                            y=datum.components[0] / maximum,
                            mode="lines",
                            opacity=0.6,
                            line={"width": 1.2},
                            fill="tozeroy",
                            name=name,
                        )
                    )

            else:
                data.append(
                    go.Scatter(
                        x0=x0,
                        dx=dx,
                        y=y_data.dependent_variables[0].components[0],
                        mode="lines",
                        line={"color": "black", "width": 1.2},
                        name="simulation",
                    )
                )

        if len(current_data.dimensions) == 2:
            x = current_data.dimensions[0].coordinates.value
            y = current_data.dimensions[1].coordinates.value

            # get the max data point
            y_data = 0
            maximum = 1.0
            for datum in current_data.split():
                y_data += datum

            if normalized:
                maximum = y_data.max()
                y_data /= maximum

            decompose = sim_data["config"]["decompose_spectrum"] == "spin_system"
            if decompose:
                for datum in current_data.dependent_variables:
                    name = datum.name
                    if name == "":
                        name = None
                    data.append(
                        go.Contour(
                            dx=x[1] - x[0],
                            dy=y[1] - y[0],
                            x0=x[0],
                            y0=y[0],
                            z=datum.components[0] / maximum,
                            fillcolor=False,
                            # type="heatmap",
                            showscale=False,
                            # mode="lines",
                            opacity=0.6,
                            colorscale="dense",
                            # line={"width": 1.2},
                            # fill="tozeroy",
                            name=name,
                        )
                    )

            else:
                data.append(
                    go.Heatmap(
                        dx=x[1] - x[0],
                        dy=y[1] - y[0],
                        x0=x[0],
                        y0=y[0],
                        z=y_data.dependent_variables[0].components[0],
                        type="heatmap",
                        showscale=False,
                        # line_smoothing=0,
                        # contours_coloring="lines",
                        # line_width=1.2,
                        # mode="lines",
                        # line={"color": "black", "width": 1.2},
                        colorscale="dense",
                        # "tempo", "curl", "armyrose", "dense",  # "electric_r",
                        # zmid=0,
                        name="simulation",
                    )
                )

    local_exp_external_data = None
    if "experiment" in sim_data["methods"][method_index]:
        local_exp_external_data = sim_data["methods"][method_index]["experiment"]

    if local_exp_external_data is not None:
        local_exp_external_data = cp.parse_dict(local_exp_external_data)

        if local_exp_external_data.dimensions[0].origin_offset.value != 0:
            local_exp_external_data.dimensions[0].to("ppm", "nmr_frequency_ratio")
            x_spectrum = local_exp_external_data.dimensions[0].coordinates.value
        else:
            x_spectrum = (
                local_exp_external_data.dimensions[0].coordinates.to("Hz").value
            )

        x0 = x_spectrum[0]
        dx = x_spectrum[1] - x_spectrum[0]
        y_spectrum = local_exp_external_data.dependent_variables[0].components[0]
        if normalized:
            y_spectrum /= np.abs(y_spectrum.max())
        data.append(
            go.Scatter(
                x0=x0,
                dx=dx,
                y=y_spectrum.real,
                mode="lines",
                line={"color": "#af0072", "width": 1.2},
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

    data_object = {"data": data, "layout": go.Layout(**layout)}

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


if __name__ == "__main__":
    host = "127.0.0.1"
    is_host = ["--host" in arg for arg in sys.argv]
    if any(is_host):
        host_index = np.where(np.asarray(is_host))[0][0]
        host = sys.argv[host_index].split("=")[1]

    port = 8050
    is_port = ["--port" in arg for arg in sys.argv]
    if any(is_port):
        port_index = np.where(np.asarray(is_port))[0][0]
        port = int(sys.argv[port_index].split("=")[1])

    debug = False
    is_debug = ["--debug" in arg for arg in sys.argv]
    if any(is_debug):
        debug_index = np.where(np.asarray(is_debug))[0][0]
        debug = True if sys.argv[debug_index].split("=")[1] == "True" else False

    app.run_server(host=host, port=port, debug=debug, use_reloader=False)
