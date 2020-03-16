# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


def coordinate_grid(i):
    """
        Return a list of widgets whose entries are used in evaluating the dimension
        coordinates along the i^th dimension. The widgets includes number of points,
        spectral width, and reference offset.

        Args:
            i: An integer with the dimension index.
    """
    # number of points
    range_num = [7, 8, 10, 12, 14, 16, 18]
    list_of_numbers = {i: f"{2 ** i}" for i in range_num}
    number_of_points = custom_slider(
        label="Number of points",
        return_function=lambda x: 2 ** x,
        min=7,
        max=18,
        step=1,
        value=11,
        marks=list_of_numbers,
        id=f"dim-number_of_points-{i}",
    )

    # spectral width
    spectral_width = custom_input_group(
        prepend_label="Spectral width",
        append_label="kHz",
        value=25.0,
        min=0.0,
        id=f"dim-spectral_width-{i}",
    )

    # reference offset
    reference_offset = custom_input_group(
        prepend_label="Reference offset",
        append_label="kHz",
        value=0.0,
        id=f"dim-reference_offset-{i}",
    )

    return html.Div(
        [number_of_points, spectral_width, reference_offset],
        className="collapsible-body-control",
    )


def environment(i):
    """
        Return a list of widgets whose entries are used for evaluating the sample
        environment along the i^th dimension. The widgets includes isotope,
        spectrometer frequency, rotor frequency, and rotor angle.

        Args:
            i: An integer with the dimension index.
    """
    # spectrometer frequency
    field_strength = {
        1: "100 MHz",
        4: "400 MHz",
        7: "700 MHz",
        10: "1 GHz",
        13: "1.3 GHz",
    }
    spectrometer_frequency = custom_slider(
        label="Spectrometer frequency @1H",
        return_function=lambda x: f"{int(x*100)} MHz" if x < 10 else f"{x/10} GHz",
        min=1,
        max=13,
        step=0.5,
        value=4,
        marks=field_strength,
        id=f"dim-spectrometer_frequency-{i}",
    )

    # rotor frequency
    rotor_frequency = custom_input_group(
        prepend_label="Rotor frequency",
        append_label="kHz",
        value=0.0,
        id=f"dim-rotor_frequency-{i}",
        min=0.0,
        # list=["0", "54.7356", "30", "60", "90"],
    )

    # rotor angle
    rotor_angle = custom_input_group(
        prepend_label="Rotor angle",
        append_label="deg",
        value=54.735,
        id=f"dim-rotor_angle-{i}",
        max=90,
        min=0,
    )

    isotope_and_filter = html.Div(
        [
            "Isotope",
            dcc.Dropdown(
                id=f"isotope_id-{i}",
                searchable=False,
                clearable=False,
                placeholder="Select an isotope...",
            ),
        ],
        className="justify-items-stretch form-group",
    )

    return html.Div(
        [isotope_and_filter, spectrometer_frequency, rotor_frequency, rotor_angle],
        className="collapsible-body-control form",
    )
