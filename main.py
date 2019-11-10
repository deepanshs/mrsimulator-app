# -*- coding: utf-8 -*-
import csdmpy as cp
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
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
from app.methods.post_simulation_functions import line_broadening
from app.methods.post_simulation_functions import post_simulation

# from app.modal.about import about_modal

# from mrsimulator.app.post_simulation import line_broadening


__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]

test = html.Div(
    className="upload-btn-wrapper",
    children=[html.Button("Upload a file", className="btn"), dcc.Upload()],
)

app.layout = html.Div(
    app_1, className="wrapper", id="article1", **{"data-role": "page"}
)

server = app.server


# Main function. Evaluates the spectrum and update the plot.
@app.callback(
    [Output("local-computed-data", "data"), Output("larmor_frequency-0", "data")],
    [
        Input("rotor_frequency-0", "value"),
        Input("rotor_angle-0", "value"),
        Input("number_of_points-0", "value"),
        Input("spectral_width-0", "value"),
        Input("reference_offset-0", "value"),
        Input("spectrometer_frequency-0", "value"),
        Input("isotope_id-0", "value"),
        Input("close_setting", "n_clicks"),
    ],
    [
        State("integration_density", "value"),
        State("integration_volume", "value"),
        State("local-metadata", "data"),
    ],
)
def simulation(
    # input
    rotor_frequency,
    rotor_angle,
    number_of_points,
    spectral_width,
    reference_offset,
    spectrometer_frequency,
    isotope_id,
    close_setting_model,
    # state
    integration_density,
    integration_volume,
    local_metadata,
):
    """Evaluate the spectrum and update the plot."""
    # exit when the following conditions are True
    if isotope_id in ["", None]:
        raise PreventUpdate

    ctx = dash.callback_context
    print(ctx.triggered)
    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        value = ctx.triggered[0]["value"]
        if value in [None, "", ".", "-"]:
            raise PreventUpdate
        if "isotope_id" not in button_id:
            try:
                float(value)
            except ValueError:
                raise PreventUpdate

    if spectral_width == 0:
        raise PreventUpdate

    magnetic_flux_density = spectrometer_frequency / 42.57748

    sim = Simulator()
    dim = {
        "isotope": isotope_id,
        "magnetic_flux_density": str(magnetic_flux_density * 100) + " T",
        "rotor_frequency": str(rotor_frequency) + " kHz",
        "rotor_angle": str(rotor_angle) + " deg",
        "number_of_points": 2 ** number_of_points,
        "spectral_width": str(spectral_width) + " kHz",
        "reference_offset": str(reference_offset) + " kHz",
        "nt": integration_density,
    }
    sim.spectrum = [Dimension.parse_dict_with_units(dim)]
    abs_larmor_freq = abs(sim.spectrum[0].larmor_frequency)
    sim.isotopomers = [
        Isotopomer.parse_dict_with_units(item) for item in local_metadata["isotopomers"]
    ]

    sim.run(
        one_d_spectrum,
        geodesic_polyhedron_frequency=integration_density,
        individual_spectrum=True,
        averaging=integration_volume,
    )

    local_computed_data = sim.as_csdm_object().to_dict(update_timestamp=True)
    return [local_computed_data, abs_larmor_freq]


@app.callback(
    [Output("spectral_width-0", "value"), Output("reference_offset-0", "value")],
    # Output("buffer", "className"),
    [Input("nmr_spectrum", "relayoutData")],
    [
        State("larmor_frequency-0", "data"),
        State("number_of_points-0", "value"),
        State("spectral_width-0", "value"),
    ],
)
def display_relayout_data(relayoutData, larmor_freq, npts, sw):
    if relayoutData is None:
        raise PreventUpdate
    keys = relayoutData.keys()
    if "xaxis.range[0]" not in keys:
        raise PreventUpdate
    if "yaxis.range[0]" in keys:
        raise PreventUpdate
    if None in [
        relayoutData["xaxis.range[0]"],
        relayoutData["xaxis.range[1]"],
        larmor_freq,
    ]:
        raise PreventUpdate

    x_min = relayoutData["xaxis.range[0]"] * larmor_freq
    x_max = relayoutData["xaxis.range[1]"] * larmor_freq
    increment = float(sw) * 1000 / (2 ** npts)
    sw_ = x_min - x_max + increment
    ref_offset = x_max + sw_ / 2.0
    return ["{0:.5f}".format(sw_ / 1000.0), "{0:.5f}".format(ref_offset / 1000.0)]


@app.callback(
    Output("nmr_spectrum", "figure"),
    [
        Input("local-computed-data", "modified_timestamp"),
        Input("decompose", "active"),
        Input("local-csdm-data", "modified_timestamp"),
        Input("normalize_amp", "active"),
        Input("broadening_points-0", "value"),
        Input("Apodizing_function-0", "value"),
    ],
    [
        State("local-computed-data", "data"),
        State("local-csdm-data", "data"),
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
    local_computed_data,
    local_csdm_data,
    isotope_id,
    figure,
):
    """Generate and return a one-dimensional plot instance."""
    if local_computed_data is None and local_csdm_data is None:
        raise PreventUpdate

    data = []
    if isotope_id is None:
        isotope_id = ""

    if local_computed_data is not None:

        local_computed_data = cp.parse_dict(local_computed_data)

        local_computed_data = post_simulation(
            line_broadening,
            csdm_object=local_computed_data,
            sigma=broadening,
            broadType=apodization,
        )

        origin_offset = local_computed_data.dimensions[0].origin_offset
        if origin_offset.value == 0.0:
            x = local_computed_data.dimensions[0].coordinates.to("kHz").value
        else:
            x = (
                (local_computed_data.dimensions[0].coordinates / origin_offset)
                .to("ppm")
                .value
            )
        x0 = x[0]
        dx = x[1] - x[0]
        if decompose:
            maximum = 1.0
            if normalized:
                y_data = 0
                for datum in local_computed_data.dependent_variables:
                    y_data += datum.components[0]
                    maximum = y_data.max()
            for datum in local_computed_data.dependent_variables:
                name = datum.name
                if name == "":
                    name = None
                data.append(
                    go.Scatter(
                        x0=x0,
                        dx=dx,
                        y=datum.components[0] / maximum,
                        mode="lines",
                        opacity=0.8,
                        line={"width": 1.2},
                        fill="tozeroy",
                        name=name,
                    )
                )

        else:
            y_data = 0
            for datum in local_computed_data.dependent_variables:
                y_data += datum.components[0]
            if normalized:
                y_data /= y_data.max()
            data.append(
                go.Scatter(
                    x0=x0,
                    dx=dx,
                    y=y_data,
                    mode="lines",
                    line={"color": "black", "width": 1.2},
                    name=f"simulation",
                )
            )

    if local_csdm_data is not None:
        local_csdm_data = cp.parse_dict(local_csdm_data)

        origin_offset = local_csdm_data.dimensions[0].origin_offset
        if origin_offset.value == 0.0:
            x_spectrum = local_csdm_data.dimensions[0].coordinates.to("kHz").value
        else:
            x_spectrum = (
                (local_csdm_data.dimensions[0].coordinates / origin_offset)
                .to("ppm")
                .value
            )
        x0 = x_spectrum[0]
        dx = x_spectrum[1] - x_spectrum[0]
        y_spectrum = local_csdm_data.dependent_variables[0].components[0]
        if normalized:
            y_spectrum /= np.abs(y_spectrum.max())
        data.append(
            go.Scatter(
                x0=x0,
                dx=dx,
                y=y_spectrum.real,
                mode="lines",
                line={"color": "grey", "width": 1.2},
                name=f"experiment",
            )
        )

    layout = figure["layout"]
    layout["xaxis"]["title"] = f"{isotope_id} frequency ratio / ppm"
    data_object = {"data": data, "layout": go.Layout(**layout)}
    return data_object


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
    [Input("local-metadata", "data")],
)
def update_isotope_list(data):
    if data is None:
        raise PreventUpdate
    if data["isotopomers"] == []:
        return [[], ""]

    sim_m = Simulator()
    sim_m.isotopomers = [
        Isotopomer.parse_dict_with_units(item) for item in data["isotopomers"]
    ]
    isotope_list = [
        {"label": site_iso, "value": site_iso} for site_iso in sim_m.get_isotopes()
    ]
    isotope = isotope_list[0]["value"]

    return [isotope_list, isotope]


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True)
