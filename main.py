# -*- coding: utf-8 -*-
import json
import os
import uuid

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.graph_objs as go
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Dimension
from mrsimulator import Isotopomer
from mrsimulator import Simulator
from mrsimulator.methods import one_d_spectrum

from app import importer
from app import navbar
from app import sidebar
from app.app import app
from app.body import main_body

# from mrsimulator.app.post_simulation import line_broadening


__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]

# Load default csdm compliant file.
with open("static/default_file.json", "r") as f:
    default_computed_data = json.load(f)


test = html.Div(
    className="upload-btn-wrapper",
    children=[html.Button("Upload a file", className="btn"), dcc.Upload()],
)

app.layout = html.Div(
    dbc.Container(
        [
            navbar.navbar_top,
            navbar.side_panel,
            importer.isotopomer_import_layout,
            importer.spectrum_import_layout,
            importer.example_drawer,
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(sidebar.sidebar, xs=12, sm=12, md=12, lg=12, xl=3),
                        dbc.Col(
                            [
                                html.Div(main_body),
                                html.Div(id="isotopomer_computed_log"),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl=9,
                        ),
                    ]
                )
            ),
            # test,
            # dbc.Jumbotron(),
            navbar.navbar_bottom,
        ],
        fluid=True,
        # style={"max-width": "1400px"},
        className="master-padding",
    ),
    className="wrapper",
    id="article1",
    **{"data-role": "page"},
)
server = app.server


# # Serialize the computed spectrum and download the serialized file.
@app.server.route("/downloads/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, "downloads"), path, as_attachment=True
    )


# update the link to the downloadable serialized file.
@app.callback(
    [Output("download_csdm", "href"), Output("temp-state-file", "data")],
    [Input("nmr_spectrum", "figure")],
    [State("local-computed-data", "data"), State("temp-state-file", "data")],
)
def file_download_link(figure, local_computed_data, temp_state_file):
    """Update the link to the downloadable file."""
    # print(figure["layout"])
    # print(figure["data"])
    if local_computed_data is None:
        return [None, "#"]
    if temp_state_file is not None:
        try:
            os.remove(temp_state_file)
        except:
            pass
    relative_filename = os.path.join("downloads", f"{uuid.uuid1()}.csdf")
    with open(relative_filename, "w") as f:
        json.dump(local_computed_data, f)
    return ["/{}".format(relative_filename), "./{}".format(relative_filename)]


# Main function. Evaluates the spectrum and update the plot.
@app.callback(
    Output("local-computed-data", "data"),
    [
        Input("rotor_frequency-0", "value"),
        Input("rotor_angle-0", "value"),
        Input("number_of_points-0", "value"),
        Input("spectral_width-0", "value"),
        Input("reference_offset-0", "value"),
        Input("spectrometer_frequency-0", "value"),
        Input("isotope_id-0", "value"),
        # Input("broadening_points-0", "value"),
        Input("close_setting", "n_clicks"),
    ],
    [
        State("integration_density", "value"),
        State("integration_volume", "value"),
        State("local-metadata", "data"),
    ],
)
def update_data(
    # input
    rotor_frequency,
    rotor_angle,
    number_of_points,
    spectral_width,
    reference_offset,
    spectrometer_frequency,
    isotope_id,
    close_setting_model,
    # broadening,
    # state
    integration_density,
    integration_volume,
    local_metadata,
):
    """Evaluate the spectrum and update the plot."""
    local_computed_data = default_computed_data

    if spectral_width in [None, 0, "", ".", "-"]:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate
    if reference_offset in [None, "", ".", "-"]:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate
    if rotor_frequency in [None, "", ".", "-"]:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    # exit when the following conditions are True
    if isotope_id in ["", None]:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    # calculating spectral_width
    try:
        spectral_width = float(spectral_width)
    except ValueError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    # calculating rotor_frequency
    try:
        rotor_frequency = float(eval(str(rotor_frequency)))
    except ValueError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate
    except SyntaxError:
        try:
            rotor_frequency = float(rotor_frequency)
        except ValueError:
            # return local_computed_data
            print("---simulation prevented---")
            raise PreventUpdate

    # calculating reference_offset
    try:
        reference_offset = float(reference_offset)
    except ValueError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    try:
        magnetic_flux_density = float(spectrometer_frequency) / 42.57747892
    except ValueError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    # calculating rotor angle
    try:
        rotor_angle = float(eval(str(rotor_angle)))  # 54.735
    except ValueError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate
    except SyntaxError:
        # return local_computed_data
        print("---simulation prevented---")
        raise PreventUpdate

    print("---simulate data---")
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
    # metadata = json.loads(local_metadata)
    sim.isotopomers = [
        Isotopomer.parse_dict_with_units(item) for item in local_metadata["isotopomers"]
    ]

    print(sim.spectrum[0].rotor_frequency)
    sim.run(
        one_d_spectrum,
        geodesic_polyhedron_frequency=integration_density,
        individual_spectrum=True,
        averaging=integration_volume,
    )
    print(sim.spectrum[0].rotor_frequency)
    local_computed_data = sim.as_csdm_object().to_dict(update_timestamp=True)
    return local_computed_data


@app.callback(
    Output("nmr_spectrum", "figure"),
    [
        Input("local-computed-data", "modified_timestamp"),
        Input("decompose", "active"),
        Input("local-csdm-data", "modified_timestamp"),
        Input("normalize_amp", "active"),
    ],
    [
        State("local-computed-data", "data"),
        State("local-csdm-data", "data"),
        State("isotope_id-0", "value"),
    ],
)
def plot_1D(
    time_of_computation,
    decompose,
    csdm_upload_time,
    normalized,
    local_computed_data,
    local_csdm_data,
    isotope_id,
):
    """Generate and return a one-dimensional plot instance."""
    if local_computed_data is None and local_csdm_data is None:
        print("---prevented plot update---")
        raise PreventUpdate

    data = []
    if isotope_id is None:
        isotope_id = ""

    if local_computed_data is not None:

        local_computed_data = cp.parse_dict(local_computed_data)

        origin_offset = local_computed_data.dimensions[0].origin_offset
        if origin_offset.value == 0.0:
            x = local_computed_data.dimensions[0].coordinates.to("kHz").value
        else:
            x = (local_computed_data.dimensions[0].coordinates / origin_offset).to(
                "ppm"
            )
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
                        x=x,
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
                    x=x,
                    y=y_data,
                    mode="lines",
                    line={"color": "black", "width": 1.2},
                    name=f"spectrum",
                )
            )

    if local_csdm_data is not None:
        local_csdm_data = cp.parse_dict(local_csdm_data)

        origin_offset = local_csdm_data.dimensions[0].origin_offset
        if origin_offset.value == 0.0:
            x_spectrum = local_csdm_data.dimensions[0].coordinates.to("kHz").value
        else:
            x_spectrum = (local_csdm_data.dimensions[0].coordinates / origin_offset).to(
                "ppm"
            )
        y_spectrum = local_csdm_data.dependent_variables[0].components[0]
        if normalized:
            y_spectrum /= y_spectrum.max()
        data.append(
            go.Scatter(
                x=x_spectrum,
                y=y_spectrum.real,
                mode="lines",
                line={"color": "grey", "width": 1.2},
                name=f"experiment",
            )
        )

    x_label = str(isotope_id + f" frequency / ppm")

    data_object = {
        "data": data,
        "layout": go.Layout(
            xaxis=dict(
                title=x_label,
                ticks="outside",
                showline=True,
                autorange="reversed",
                zeroline=False,
            ),
            yaxis=dict(
                title="arbitrary unit",
                ticks="outside",
                showline=True,
                zeroline=False,
                rangemode="tozero",
            ),
            autosize=True,
            transition={
                "duration": 175,
                "easing": "sin-out",
                "ordering": "traces first",
            },
            margin={"l": 50, "b": 40, "t": 5, "r": 5},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            paper_bgcolor="rgba(255,255,255,4)",
            # plot_bgcolor="rgba(0,0,0,0)",
            # template="plotly_dark",
        ),
    }
    print("---update plot---")
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


# def post_simulation(function, **kwargs):
#     return [
#         function(datum, **kwargs)
#         for datum in sim.original
#         if not isinstance(datum, list)
#     ]


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
    app.run_server(debug=True, threaded=False)
