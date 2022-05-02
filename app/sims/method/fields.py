# -*- coding: utf-8 -*-
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

from app import app
from app.custom_widgets import collapsable_card
from app.custom_widgets import container
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group


__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


def experiment_ui():
    """upload options for experiment csdf file"""
    # upload experiment dataset
    tooltip = (
        "Click to attach a measurement file to the selected method. "
        "Alternatively, drag and drop the file onto the Simulation area."
    )
    icon = html.I(className="fas fa-paperclip fa-lg", title=tooltip)
    clip_btn = html.Button(icon, className="icon-button")
    upload = dcc.Upload(clip_btn, id="import-measurement-for-method")

    # standard deviation
    calc_tooltip = (
        "Click to calculate the noise standard deviation from the selected region of "
        "the experiment spectrum. Use the 'Draw rectangle' button to select the region."
    )
    calc_icon = html.I(className="fas fa-calculator", title=calc_tooltip)
    calc_btn = html.Button(calc_icon, id="calc-sigma-button", className="icon-button")
    sigma = custom_input_group(
        prepend_label="Noise standard deviation (σ)",  # Text overwraps the input field
        append_label=calc_btn,
        value=1.0,
        min=1e-6,
        id="measurement-sigma",
        debounce=True,
    )

    return container(text=["Experiment", upload], featured=[sigma])


def spectral_dimension_ui(i):
    """Return a list of widgets whose entries are used in evaluating the dimension
    coordinates along the i^th dimension. The widgets includes number of points (count),
    spectral width, and reference offset.

    Args:
        i: An integer with the dimension index.
    """
    # count
    count = custom_input_group(
        prepend_label="Number of points",
        value=512,
        min=2,
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
    # origin_offset = custom_input_group(
    #     prepend_label="Origin offset",
    #     append_label="MHz",
    #     value=0.0,
    #     id=f"origin_offset-{i}",
    #     debounce=True,
    # )

    # label
    label = custom_input_group(
        prepend_label="Label",
        append_label="",
        input_type="text",
        value="frequency",
        id=f"label-{i}",
        debounce=True,
    )

    return collapsable_card(
        text=f"Spectral Dimension - {i}",
        id_=f"dim-{i}",
        featured=[count, spectral_width, reference_offset],
        hidden=[label],
        message="Show/Hide",
        outer=True,
    )


def global_environment():
    """Generate a list of widgets whose entries are the sample global environment
    parameter. The widgets includes flux density, rotor frequency, and rotor angle."""

    flux_density = custom_input_group(
        prepend_label="Magnetic flux density (B₀)",
        append_label="T",
        value=9.4,
        id="magnetic_flux_density",
        min=0.0,
        debounce=True,
    )

    # rotor frequency
    rotor_frequency = custom_input_group(
        prepend_label="Rotor frequency (𝜈ᵣ)",
        append_label="kHz",
        value=0.0,
        id="rotor_frequency",
        min=0.0,
        debounce=True,
    )

    # rotor angle
    magic_angle = custom_button(
        icon_classname="fas fa-magic",
        tooltip="Set value to the magic angle.",
        id="set-to-magic-angle",
        className="icon-button",
        module="html",
    )
    # dbc.Button(
    #     html.I(className="fas fa-magic"),
    #     color="light",
    #     id="set-to-magic-angle",
    #     size="sm",
    # )
    # datalist = html.Datalist([0, 54.7356103172, 90], id="datalist-magic-angle")
    rotor_angle = custom_input_group(
        prepend_label=html.Div(["Rotor angle (θᵣ)", magic_angle]),
        append_label="deg",
        value=54.7356103172,
        id="rotor_angle",
        max=90,
        min=0,
        debounce=True,
        # list="datalist-magic-angle",
    )

    app.clientside_callback(
        """function(n) { return 54.7356103172; }""",
        Output("rotor_angle", "value"),
        Input("set-to-magic-angle", "n_clicks"),
    )

    return container(
        text="Global Environment Parameters",
        featured=[flux_density, rotor_frequency, rotor_angle],
    )
