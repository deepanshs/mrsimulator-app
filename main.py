# -*- coding: utf-8 -*-
import csdmpy as cp
import dash
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Dimension
from mrsimulator import Isotopomer
from mrsimulator import Simulator
from mrsimulator.methods import one_d_spectrum

from app.app import app
from app.body import app_1
from app.graph import DEFAULT_FIGURE
from app.methods.post_simulation_functions import line_broadening
from app.methods.post_simulation_functions import post_simulation

# import dash_core_components as dcc

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]


RAD_FACTOR = np.pi / 180.0
app.layout = html.Div(app_1, id="article1", **{"data-role": "page"})


server = app.server


def check_if_old_and_new_isotopomers_data_are_equal(new, old):
    """Check if the two isotopomers are the same. This does not include the
        name and the description of the isotopomers."""
    size1 = len(new["isotopomers"])
    size2 = len(old["isotopomers"])
    size_min = min(size1, size2)

    true_index = [False] * size1
    for i in range(size_min):
        if new["isotopomers"][i]["sites"] == old["isotopomers"][i]["sites"]:
            true_index[i] = True

    return true_index


def check_for_simulation_update(
    isotope_id,
    config,
    local_isotopomers_data,
    previous_local_computed_data,
    previous_local_isotopomer_index_map,
    figure,
):
    """
    Check if the simulation needs to update. The check search for
    1) If the simulation on display has a different isotope than the isotope requested
        for simulation, perform an update.
    2) If the display (from spectrum) and requested isotopes (from dimension) are the
        same, check if the last modified isotopomer
        a) was triggered with a change of isotope. If true, check if the previously
            selected isotope was used in simulation. If yes, re-simulate, else prevent
            update.
        b) was triggered with any other site attribute. If true, check if the modified
            isotopomer has the same isotope as on display. If yes, re-simulate, else,
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
    # isotopomer that was last modified. Here, we check if the changes made to the
    # isotopomer pertains the isotope used in the simulation. If the site isotopes
    # in the isotopomer is not the same as `isotope_id`, prevent the update.
    modified_index = config["index_last_modified"]
    if modified_index is None:
        raise PreventUpdate

    # site isotopes in the modified isotopomer
    modified_site_isotopes = [
        site["isotope"]
        for site in local_isotopomers_data["isotopomers"][modified_index]["sites"]
    ]

    if previous_local_computed_data is None:
        return
    # checking part a of the second condition
    # the previous_local_isotopomer_index_map contains a list of isotopomer indexes
    # that were used in the simulation. To check if the identity of the isotope changed
    # in the modified isotopomer, we compare the identity of the isotopes from the
    # isotopomers from previous_local_computed_data.
    if modified_index in previous_local_isotopomer_index_map:

        index_in_computed_data = np.where(
            np.asarray(previous_local_isotopomer_index_map) == modified_index
        )[0][0]
        print(index_in_computed_data)
        dv = previous_local_computed_data["csdm"]["dependent_variables"][
            index_in_computed_data
        ]
        previous_site_isotopes = [
            site["isotope"]
            for site in dv["application"]["com.github.DeepanshS.mrsimulator"][
                "isotopomers"
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
        Output("local-computed-data", "data"),
        Output("local-dimension-data", "data"),
        Output("local-isotopomer-index-map", "data"),
    ],
    [
        Input("dim-rotor_frequency-0", "value"),
        Input("dim-rotor_angle-0", "value"),
        Input("dim-number_of_points-0", "value"),
        Input("dim-spectral_width-0", "value"),
        Input("dim-reference_offset-0", "value"),
        Input("dim-flux_density-0", "value"),
        Input("isotope_id-0", "value"),
        Input("close_setting", "n_clicks"),
    ],
    [
        State("integration_density", "value"),
        State("integration_volume", "value"),
        State("number_of_sidebands", "value"),
        State("local-isotopomers-data", "data"),
        State("local-computed-data", "data"),
        State("local-isotopomer-index-map", "data"),
        State("config", "data"),
        State("nmr_spectrum", "figure"),
    ],
)
def simulation(
    # input
    rotor_frequency,
    rotor_angle,
    number_of_points,
    spectral_width,
    reference_offset,
    magnetic_flux_density,
    isotope_id,
    close_setting_model,
    # state
    integration_density,
    integration_volume,
    number_of_sidebands,
    local_isotopomers_data,
    previous_local_computed_data,
    previous_local_isotopomer_index_map,
    config,
    figure,
):
    """Evaluate the spectrum and update the plot."""
    # if "removed" in config.keys():
    #     raise PreventUpdate
    # exit when the following conditions are True
    if isotope_id is None:
        if previous_local_computed_data is not None:
            print("simulation cleared because isotope id is", isotope_id)
            return [[], no_update, no_update]
        raise PreventUpdate

    ctx = dash.callback_context
    # print(ctx.triggered)
    if not ctx.triggered:
        print("simulation stopped ctx not triggered")
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # if the data is new, skip the check and simulate the spectrum.
    # if "isotope" in trigger_id and not config["is_new_data"]:
    #     check_for_simulation_update(
    #         isotope_id,
    #         config,
    #         local_isotopomers_data,
    #         previous_local_computed_data,
    #         previous_local_isotopomer_index_map,
    #         figure,
    #     )

    value = ctx.triggered[0]["value"]
    if value in [".", "-"]:
        print("simulation stopped triggered value is", value)
        raise PreventUpdate

    if "isotope" not in trigger_id:
        try:
            float(value)
        except (ValueError, TypeError):
            print("simulation stopped triggered value is", value)
            raise PreventUpdate

    if spectral_width == 0:
        print("simulation stopped spectral_width is 0")
        raise PreventUpdate

    # magnetic_flux_density = spectrometer_frequency / 42.57748

    if "dim" in trigger_id:
        if value in [None, ""]:
            print("simulation stopped trigger value is", value)
            raise PreventUpdate

    dim = {
        "isotope": isotope_id,
        "magnetic_flux_density": float(magnetic_flux_density),  # in T
        "rotor_frequency": float(rotor_frequency) * 1000,  # in Hz
        "rotor_angle": float(rotor_angle) * RAD_FACTOR,  # in rad
        "number_of_points": int(number_of_points),
        "spectral_width": float(spectral_width) * 1000,  # in Hz
        "reference_offset": float(reference_offset) * 1000,  # in Hz
    }

    # def check_val(val):
    #     return val if val not in [None, ""] else 0

    # states = dash.callback_context.states
    # site = {
    #     "isotope": states[f"{i}-isotope"],
    #     "isotropic_chemical_shift": check_val(
    #         states[f"{i}-isotropic_chemical_shift"]
    #     ),  # in ppm
    #     "shielding_symmetric": {
    #         "zeta": check_val(states[f"{i}-shielding_symmetric-zeta"]),  # in ppm
    #         "eta": check_val(states[f"{i}-shielding_symmetric-eta"]),
    #         "alpha": check_val(states[f"{i}-shielding_symmetric-alpha"])
    #         * RAD_FACTOR,  # in rad
    #         "beta": check_val(states[f"{i}-shielding_symmetric-beta"])
    #         * RAD_FACTOR,  # in rad
    #         "gamma": check_val(states[f"{i}-shielding_symmetric-gamma"])
    #         * RAD_FACTOR,  # in rad
    #     },
    #     "quadrupolar": {
    #         "Cq": check_val(states[f"{i}-quadrupolar-Cq"]) * 1e6,  # in Hz
    #         "eta": check_val(states[f"{i}-quadrupolar-eta"]),
    #         "alpha": check_val(states[f"{i}-quadrupolar-alpha"])*RAD_FACTOR,# in rad
    #         "beta": check_val(states[f"{i}-quadrupolar-beta"])*RAD_FACTOR,# in rad
    #         "gamma": check_val(states[f"{i}-quadrupolar-gamma"])*RAD_FACTOR,# in rad
    #     },
    # }

    # true_index = [False] * len(local_isotopomers_data['isotopomers'])
    # if trigger_id not in [
    #     "dim-rotor_frequency-0",
    #     "dim-rotor_angle-0",
    #     "dim-number_of_points-0",
    #     "dim-spectral_width-0",
    #     "dim-reference_offset-0",
    #     "dim-spectrometer_frequency-0",
    #     "isotope_id-0",
    #     "close_setting",
    # ]:
    #     true_index = check_if_old_and_new_isotopomers_data_are_equal(
    #         local_isotopomers_data, old_local_isotopomers_data
    #     )

    # if np.all(true_index):
    #     raise PreventUpdate
    print("simulate")
    sim = Simulator()
    sim.dimensions = [Dimension(**dim)]

    mapping = []
    # for i, item in enumerate(true_index):
    #     if not item:
    #         site_isotope = [site["isotope"] for site in
    #                   local_isotopomers_data["isotopomers"][i]["sites"]]
    #         if isotope_id in site_isotope:
    #             sim.isotopomers.append(Isotopomer.parse_dict_with_units(
    #                           local_isotopomers_data["isotopomers"][i])
    #               )
    #             # print(item)
    #             mapping.append(i)

    for i, item in enumerate(local_isotopomers_data["isotopomers"]):
        site_isotope = [site["isotope"] for site in item["sites"]]
        if isotope_id in site_isotope:
            sim.isotopomers.append(Isotopomer(**item))
            mapping.append(i)

    # filter_isotopomers = [
    #     Isotopomer.parse_dict_with_units(item)
    #     for item in local_isotopomers_data["isotopomers"]
    # ]
    # sim.isotopomers = [
    #     Isotopomer.parse_dict_with_units(item)
    #     for item in local_isotopomers_data["isotopomers"]
    # ]

    sim.config.integration_density = integration_density
    sim.config.decompose = True
    sim.config.integration_volume = integration_volume
    sim.config.number_of_sidebands = number_of_sidebands

    sim.run(one_d_spectrum)

    dim.update({"larmor_frequency": sim.dimensions[0].larmor_frequency})
    local_computed_data = sim.as_csdm_object().to_dict(update_timestamp=True)
    print(
        "check with previous data",
        previous_local_computed_data == local_isotopomers_data,
    )
    print("local computed data generated", local_computed_data["csdm"]["timestamp"])
    return [local_computed_data, dim, mapping]


# @app.callback(
#     Output("buffer", "children"),
#     [Input("nmr_spectrum", "restyleData")],
#     [State("local-computed-data", "data"), State("decompose", "active")],
# )
# def display_click_data(restyleData, local_computed_data, decompose):
#     print(restyleData)
#     return ""


# @app.callback(
#     Output("buffer", "children"),
#     [Input("nmr_spectrum", "clickData"), Input("nmr_spectrum", "relayoutData")],
#     [State("local-computed-data", "data"), State("decompose", "active")],
# )
# def drag_selected_data(clickData, relayoutData, local_computed_data, decompose):
#     if None in [relayoutData, clickData, local_computed_data]:
#         raise PreventUpdate

#     keys = relayoutData.keys()
#     print(keys)
#     return ""


@app.callback(
    [
        Output("dim-reference_offset-0", "value"),
        Output("dim-spectral_width-0", "value"),
    ],
    [Input("nmr_spectrum", "relayoutData")],
    [State("local-dimension-data", "data")],
)
def display_relayout_data(relayoutData, dimension_data):
    if None in [relayoutData, dimension_data]:
        raise PreventUpdate

    keys = relayoutData.keys()

    if dimension_data["larmor_frequency"] is None:
        raise PreventUpdate
    if "yaxis.range[0]" in keys or "yaxis.range[1]" in keys:
        raise PreventUpdate
    if "xaxis.range[0]" not in keys and "xaxis.range[1]" not in keys:
        raise PreventUpdate

    larmor_frequency = abs(dimension_data["larmor_frequency"] / 1e6)  # to MHz

    # old increment
    sw = float(dimension_data["spectral_width"])  # in Hz
    rf = float(dimension_data["reference_offset"])  # in Hz
    increment = sw / dimension_data["number_of_points"]  # in Hz

    # new x-min in Hz, larmor_frequency is in MHz
    if "xaxis.range[0]" in keys and relayoutData["xaxis.range[0]"] is not None:
        x_min = relayoutData["xaxis.range[0]"] * larmor_frequency
    else:
        x_min = sw / 2.0 + rf - increment

    # new x-max in Hz, larmor_frequency is in MHz
    if "xaxis.range[1]" in keys and relayoutData["xaxis.range[1]"] is not None:
        x_max = relayoutData["xaxis.range[1]"] * larmor_frequency
    else:
        x_max = -sw / 2.0 + rf

    # new spectral-width and reference offset in Hz
    sw_ = x_min - x_max + increment
    ref_offset = x_max + sw_ / 2.0
    return ["{0:.5f}".format(ref_offset / 1000.0), "{0:.5f}".format(abs(sw_) / 1000.0)]


@app.callback(
    [Output("nmr_spectrum", "figure"), Output("local-processed-data", "data")],
    [
        Input("local-computed-data", "modified_timestamp"),
        Input("decompose", "active"),
        Input("local-exp-external-data", "modified_timestamp"),
        Input("normalize_amp", "active"),
        Input("broadening_points-0", "value"),
        Input("Apodizing_function-0", "value"),
        Input("nmr_spectrum", "clickData"),
    ],
    [
        State("local-computed-data", "data"),
        State("local-exp-external-data", "data"),
        State("isotope_id-0", "value"),
        State("nmr_spectrum", "figure"),
    ],
)
def plot_1D(
    time_of_computation,
    decompose,
    csdm_upload_time,
    normalized,
    broadening,
    apodization,
    clickData,
    # state
    local_computed_data,
    local_exp_external_data,
    isotope_id,
    figure,
):
    """Generate and return a one-dimensional plot instance."""
    print("inside plot, time of computation", time_of_computation)
    if local_computed_data is None and local_exp_external_data is None:
        raise PreventUpdate

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("plot trigger id", trigger_id)

    if isotope_id is None:
        if local_exp_external_data is None:
            return [DEFAULT_FIGURE, None]

    data = []
    if local_computed_data is not None:

        local_computed_data = cp.parse_dict(local_computed_data)

        local_processed_data = post_simulation(
            line_broadening,
            csdm_object=local_computed_data,
            sigma=broadening,
            broadType=apodization,
        )

        try:
            local_processed_data.dimensions[0].to("ppm", "nmr_frequency_ratio")
            x = local_processed_data.dimensions[0].coordinates.value
        except (ZeroDivisionError, ValueError):
            pass

        x0 = x[0]
        dx = x[1] - x[0]

        # get the max data point
        y_data = 0
        maximum = 1.0
        for datum in local_processed_data.split():
            y_data += datum

        if normalized:
            maximum = y_data.max()
            y_data /= maximum

        if decompose:
            for datum in local_processed_data.dependent_variables:
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
                    name=f"simulation",
                )
            )

    if local_exp_external_data is not None:
        local_exp_external_data = cp.parse_dict(local_exp_external_data)

        try:
            local_exp_external_data.dimensions[0].to("ppm", "nmr_frequency_ratio")
            x_spectrum = local_exp_external_data.dimensions[0].coordinates.value
        except (ZeroDivisionError, ValueError):
            pass

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
                line={"color": "grey", "width": 1.2},
                name="experiment",
            )
        )

    layout = figure["layout"]
    layout["xaxis"]["autorange"] = True
    layout["yaxis"]["autorange"] = True
    layout["xaxis"]["title"] = f"{isotope_id} frequency ratio / ppm"

    print("isotope_id", isotope_id)
    print("clickData", clickData)
    if trigger_id == "nmr_spectrum" and decompose:
        if clickData is not None:
            index = clickData["points"][0]["curveNumber"]
            # data[index], data[-1] = data[-1], data[index]
            data[index].line["width"] = 3.0
            # print("fillcolor", data[index].fillcolor)
            # for i in range(len(data)):
            #     if i != index:
            #         data[i].opacity = 0.25

    data_object = {"data": data, "layout": go.Layout(**layout)}
    return [data_object, local_processed_data.to_dict(update_timestamp=True)]


# line={"shape": "hv", "width": 1},

#  ['linear', 'quad', 'cubic', 'sin', 'exp', 'circle',
#             'elastic', 'back', 'bounce', 'linear-in', 'quad-in',
#             'cubic-in', 'sin-in', 'exp-in', 'circle-in', 'elastic-in',
#             'back-in', 'bounce-in', 'linear-out', 'quad-out',
#             'cubic-out', 'sin-out', 'exp-out', 'circle-out',
#             'elastic-out', 'back-out', 'bounce-out', 'linear-in-out',
#             'quad-in-out', 'cubic-in-out', 'sin-in-out', 'exp-in-out',
#             'circle-in-out', 'elastic-in-out', 'back-in-out',
#             'bounce-in-out']


@app.callback(
    [Output("isotope_id-0", "options"), Output("isotope_id-0", "value")],
    [Input("local-isotopomers-data", "modified_timestamp")],
    [State("local-isotopomers-data", "data"), State("isotope_id-0", "value")],
)
def update_isotope_list(data_modify_time, data, old_isotope_value):
    if data is None:
        raise PreventUpdate
    if data["isotopomers"] == []:
        return [[], None]

    isotopes = set(
        [site["isotope"] for item in data["isotopomers"] for site in item["sites"]]
    )
    isotope_option_list = [
        {"label": site_iso, "value": site_iso} for site_iso in isotopes
    ]

    if old_isotope_value in isotopes:
        isotope = old_isotope_value
    else:
        isotope = isotope_option_list[0]["value"]

    return [isotope_option_list, isotope]


if __name__ == "__main__":
    app.run_server(
        host="0.0.0.0",
        port=5001,
        debug=True,
        dev_tools_ui=True,
        dev_tools_hot_reload=True,
    )
