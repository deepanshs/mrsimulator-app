# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_input_group


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


def spectral_dimension_ui(i):
    """
        Return a list of widgets whose entries are used in evaluating the dimension
        coordinates along the i^th dimension. The widgets includes number of points,
        spectral width, and reference offset.

        Args:
            i: An integer with the dimension index.
    """
    # number of points
    # range_num = [7, 8, 10, 12, 14, 16, 18]
    # list_of_numbers = {i: f"{2 ** i}" for i in range_num}
    # number_of_points = custom_slider(
    #     label="Number of points",
    #     return_function=lambda x: 2 ** x,
    #     min=7,
    #     max=18,
    #     step=1,
    #     value=11,
    #     marks=list_of_numbers,
    #     id=f"dim-number_of_points-{i}",
    # )
    number_of_points = custom_input_group(
        prepend_label="Number of points",
        value=512,
        min=2,
        # step=1,
        id=f"count-{i}",
        debounce=True,
        pattern="[0-9]*",
    )

    # spectral width
    spectral_width = custom_input_group(
        prepend_label="Spectral width",
        append_label="kHz",
        value=25.0,
        min=1e-6,
        id=f"spectral_width-{i}",
        debounce=True,
    )

    # reference offset
    reference_offset = custom_input_group(
        prepend_label="Reference offset",
        append_label="kHz",
        value=0.0,
        id=f"reference_offset-{i}",
        debounce=True,
    )

    # origin offset
    origin_offset = custom_input_group(
        prepend_label="Origin offset",
        append_label="MHz",
        value=0.0,
        id=f"origin_offset-{i}",
        debounce=True,
    )

    # origin offset
    label = custom_input_group(
        prepend_label="Label",
        append_label="",
        input_type="text",
        value="frequency",
        id=f"label-{i}",
        debounce=True,
    )

    button = html.Label(
        [
            html.I(className="fas fa-chevron-down"),
            dbc.Tooltip("Expand/Collapse", target=f"dim-{i}-collapsible-button"),
        ],
        id=f"dim-{i}-collapsible-button",
    )

    @app.callback(
        Output(f"dim-{i}-collapsible", "is_open"),
        [Input(f"dim-{i}-collapsible-button", "n_clicks")],
        [State(f"dim-{i}-collapsible", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_event_collapsible1(n, is_open):
        if n is None:
            raise PreventUpdate

        return not is_open

    collapsible = dbc.Collapse(
        [origin_offset, label], id=f"dim-{i}-collapsible", is_open=False
    )

    return html.Div(
        [
            html.H6(html.Div(["Properties", button])),
            html.Div(
                [number_of_points, spectral_width, reference_offset, collapsible],
                className="container",
            ),
        ]
    )


def property_setup(i):
    # channel

    # fields for spectral dimensions
    spec_fields = spectral_dimension_ui(i)

    # fields for events. limiting events to 2
    events_i = []
    for j in range(2):
        button = html.Label(
            [
                html.I(className="fas fa-chevron-down"),
                dbc.Tooltip(
                    "Show/Hide event", target=f"event-{i}-{j}-collapsible-button"
                ),
            ],
            id=f"event-{i}-{j}-collapsible-button",
        )

        events_i.append(
            # custom_subcard(
            #     text=html.Div([f"Event - {j}", button]),
            #     children=dbc.Collapse(
            #         environment(i, j),
            #         id=f"event-{i}-{j}-collapsible",
            #         is_open=True,
            #     ),
            #     id=f"event-{i}-{j}",
            # )
            html.Div(
                [
                    html.H6(html.Div([f"Event - {j}", button])),
                    dbc.Collapse(
                        environment(i, j),
                        id=f"event-{i}-{j}-collapsible",
                        is_open=True,
                    ),
                ],
                id=f"event-{i}-{j}",
            )
        )

        @app.callback(
            Output(f"event-{i}-{j}-collapsible", "is_open"),
            [Input(f"event-{i}-{j}-collapsible-button", "n_clicks")],
            [State(f"event-{i}-{j}-collapsible", "is_open")],
            prevent_initial_call=True,
        )
        def toggle_event_collapsible(n, is_open):
            if n is None:
                raise PreventUpdate

            return not is_open

    # button = html.Label(
    #     [
    #         html.I(className="fas fa-chevron-down"),
    #         dbc.Tooltip("Expand/Collapse", target=f"dim-{i}-collapsible-button"),
    #     ],
    #     id=f"dim-{i}-collapsible-button",
    # )

    # @app.callback(
    #     Output(f"dim-{i}-collapsible", "is_open"),
    #     [Input(f"dim-{i}-collapsible-button", "n_clicks")],
    #     [State(f"dim-{i}-collapsible", "is_open")],
    #     prevent_initial_call=True,
    # )
    # def toggle_event_collapsible1(n, is_open):
    #     if n is None:
    #         raise PreventUpdate

    #     return not is_open

    dimension_fields = html.Div(
        [spec_fields, *events_i],
        className="tab-scroll method method-scroll scroll-cards",
    )

    return dimension_fields


def environment(i, j):
    """
        Return a list of widgets whose entries are used for evaluating the sample
        environment along the i^th dimension. The widgets includes isotope,
        spectrometer frequency, rotor frequency, and rotor angle.

        Args:
            i: An integer with the dimension index.
    """
    # spectrometer frequency
    # field_strength = {
    #     1: "100 MHz",
    #     4: "400 MHz",
    #     7: "700 MHz",
    #     10: "1 GHz",
    #     13: "1.3GHz",
    # }
    # spectrometer_frequency = custom_slider(
    #     label="Spectrometer frequency @1H",
    #     return_function=lambda x: f"{int(x*100)} MHz" if x < 10 else f"{x/10} GHz",
    #     min=1,
    #     max=13,
    #     step=0.5,
    #     value=4,
    #     marks=field_strength,
    #     id=f"dim-spectrometer_frequency-{i}",
    # )
    flux_density = custom_input_group(
        prepend_label="Magnetic flux density (H₀)",
        append_label="T",
        value=9.4,
        id=f"magnetic_flux_density-{i}-{j}",
        min=0.0,
        debounce=True,
    )

    # rotor frequency
    rotor_frequency = custom_input_group(
        prepend_label="Rotor frequency (𝜈ᵣ)",
        append_label="kHz",
        value=0.0,
        id=f"rotor_frequency-{i}-{j}",
        min=0.0,
        debounce=True,
        # list=["0", "54.7356", "30", "60", "90"],
    )

    # rotor angle
    rotor_angle = custom_input_group(
        prepend_label="Rotor angle (θᵣ)",
        append_label="deg",
        value=54.735,
        id=f"rotor_angle-{i}-{j}",
        max=90,
        min=0,
        debounce=True,
    )

    # transition P
    transition = custom_input_group(
        prepend_label="Transition symmetry (P)",
        append_label="",
        value=0,
        id=f"transition-{i}-{j}",
        style={"display": "none"},
        debounce=True,
    )

    # isotope_and_filter = html.Div(
    #     [
    #         "Isotope",
    #         dcc.Dropdown(
    #             id=f"isotope_id-{i}",
    #             searchable=False,
    #             clearable=False,
    #             placeholder="Select an isotope...",
    #         ),
    #     ],
    #     className="justify-items-stretch form-group",
    # )

    return html.Div(
        [flux_density, rotor_frequency, rotor_angle, transition], className="container"
    )
