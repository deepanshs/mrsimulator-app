# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# dropdown_menu_items_1 = [
#     dbc.DropdownMenuItem("kHz", id="kHz_1"),
#     dbc.DropdownMenuItem("ppm", id="ppm_1"),
# ]


def coordinate_grid(i):
    # number of points
    range_num = [8, 10, 12, 14, 16]
    list_of_numbers = {i: f"{2 ** i}" for i in range_num}
    number_of_points = custom_slider(
        label="Number of points",
        return_function=lambda x: 2 ** x,
        min=7,
        max=17,
        step=1,
        value=11,
        marks=list_of_numbers,
        id=f"number_of_points-{i}",
    )

    # spectral width
    spectral_width = custom_input_group(
        prepend_label="Spectral width",
        append_label="kHz",
        value=25.0,
        min=0.0,
        id=f"spectral_width-{i}",
    )

    # reference offset
    reference_offset = custom_input_group(
        prepend_label="Reference offset",
        append_label="kHz",
        value=0.0,
        id=f"reference_offset-{i}",
    )

    return [number_of_points, html.Br(), spectral_width, reference_offset]


def environment(i):
    # spectrometer frequency
    field_strength = {
        2: "200 MHz",
        4: "400 MHz",
        6: "600 MHz",
        8: "0.8 GHz",
        10: "1 GHz",
    }
    spectrometer_frequency = custom_slider(
        label="Spectrometer frequency @1H",
        return_function=lambda x: f"{int(x*100)} MHz" if x < 10 else f"{x/10} GHz",
        min=1,
        max=12,
        step=0.5,
        value=4,
        marks=field_strength,
        id=f"spectrometer_frequency-{i}",
    )

    # rotor frequency
    rotor_frequency = custom_input_group(
        prepend_label="Rotor frequency",
        append_label="kHz",
        value=0.0,
        id=f"rotor_frequency-{i}",
        min=0.0,
        # list=["0", "54.7356", "30", "60", "90"],
    )

    # rotor angle
    rotor_angle = custom_input_group(
        prepend_label="Rotor angle",
        append_label="deg",
        value=54.735,
        id=f"rotor_angle-{i}",
        max=90,
        min=0,
    )

    # filter_spin = [
    #     {"label": "1/2", "value": 0.5},
    #     {"label": "1", "value": 1},
    #     {"label": "3/2", "value": 1.5},
    #     {"label": "5/2", "value": 2.5},
    # ]

    isotope_and_filter = dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Isotope", color="dark"),
                        dcc.Dropdown(
                            id=f"isotope_id-{i}", searchable=False, clearable=False
                        ),
                    ]
                )
            ),
            # dbc.Col(
            #     dbc.FormGroup(
            #         [
            #             dbc.Label("Filter", className="mr-2"),
            #             dcc.Dropdown(id="filter_spin", options=filter_spin,
            #                          value=0.5),
            #         ]
            #     )
            # ),
        ]
    )

    return [
        isotope_and_filter,
        spectrometer_frequency,
        html.Br(),
        rotor_frequency,
        rotor_angle,
    ]