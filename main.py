# -*- coding: utf-8 -*-
import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
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
from app.modal.about import about_modal

# from mrsimulator.app.post_simulation import line_broadening


__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]

test = html.Div(
    className="upload-btn-wrapper",
    children=[html.Button("Upload a file", className="btn"), dcc.Upload()],
)

app.layout = html.Div(
    dbc.Container(
        [
            navbar.navbar_top,
            navbar.import_options,
            html.Div(id="buffer", className="buffer"),
            # navbar.side_panel,
            html.Div(
                [
                    importer.isotopomer_import_layout,
                    importer.spectrum_import_layout,
                    importer.example_drawer,
                ],
                id="drawers-import",
            ),
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
            about_modal,
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
    # exit when the following conditions are True
    if isotope_id in ["", None]:
        print("---simulation prevented---")
        print("isotope_id", isotope_id)
        raise PreventUpdate

    if spectral_width in [None, 0, "", ".", "-"]:
        print("---simulation prevented---")
        print("spectral_width  up", spectral_width)
        raise PreventUpdate
    if reference_offset in [None, "", ".", "-"]:
        print("---simulation prevented---")
        print("reference_offset  up", reference_offset)
        raise PreventUpdate
    if rotor_frequency in [None, "", ".", "-"]:
        print("---simulation prevented---")
        print("rotor_frequency up", rotor_frequency)
        raise PreventUpdate
    if rotor_angle in [None, "", ".", "-"]:
        print("---simulation prevented---")
        print("rotor_angle  up", rotor_angle)
        raise PreventUpdate

    # calculating spectral_width
    try:
        spectral_width = float(spectral_width)
    except ValueError:
        print("---simulation prevented---")
        print("spectral_width", spectral_width)
        raise PreventUpdate

    # calculating rotor_frequency
    try:
        rotor_frequency = float(rotor_frequency)
    except ValueError:
        print("---simulation prevented---")
        print("rotor_frequency", rotor_frequency)
        raise PreventUpdate
    except SyntaxError:
        try:
            rotor_frequency = float(rotor_frequency)
        except ValueError:
            print("---simulation prevented---")
            print("rotor_frequency", rotor_frequency)
            raise PreventUpdate

    # calculating reference_offset
    try:
        reference_offset = float(reference_offset)
    except ValueError:
        print("---simulation prevented---")
        print("reference_offset", reference_offset)
        raise PreventUpdate

    try:
        magnetic_flux_density = float(spectrometer_frequency) / 42.57747892
    except ValueError:
        print("---simulation prevented---")
        print("magnetic_flux_density", magnetic_flux_density)
        raise PreventUpdate

    # calculating rotor angle
    try:
        rotor_angle = float(rotor_angle)  # 54.735
    except ValueError:
        print("---simulation prevented---")
        print("rotor_angle", rotor_angle)
        raise PreventUpdate
    except SyntaxError:
        print("---simulation prevented---")
        print("rotor_angle", rotor_angle)
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
        print("---plot update prevented---")
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
            y_spectrum /= y_spectrum.max()
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
            margin={"l": 50, "b": 45, "t": 5, "r": 5},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            template="none",
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
    app.run_server(debug=True, threaded=True)
