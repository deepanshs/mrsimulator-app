# -*- coding: utf-8 -*-
from app.custom_widgets import collapsable_card
from app.custom_widgets import container
from app.custom_widgets import custom_input_group

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


def spectral_dimension_ui(i):
    """
    Return a list of widgets whose entries are used in evaluating the dimension
    coordinates along the i^th dimension. The widgets includes number of points,
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

    # origin offset
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
    )


def global_environment():
    """
    Return a list of widgets whose entries are used for evaluating the sample
    environment along the i^th dimension. The widgets includes isotope,
    spectrometer frequency, rotor frequency, and rotor angle.

    Args:
        i: An integer with the dimension index.
    """

    flux_density = custom_input_group(
        prepend_label="Magnetic flux density (H₀)",
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
    rotor_angle = custom_input_group(
        prepend_label="Rotor angle (θᵣ)",
        append_label="deg",
        value=54.735610317,
        id="rotor_angle",
        max=90,
        min=0,
        debounce=True,
    )

    return container(
        text="Global Environment Parameters",
        featured=[flux_density, rotor_frequency, rotor_angle],
    )
