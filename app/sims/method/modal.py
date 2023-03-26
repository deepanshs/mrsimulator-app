# -*- coding: utf-8 -*-
"""Modal window for method selection"""
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from mrsimulator.method import lib as mr_lib
from mrsimulator.method import SpectralDimension

from app import app
from app.sims.spin_system.site import isotope_options_list

__author__ = ["Deepansh J. Srivastava"]
__email__ = "srivastava.89@osu.edu"


SUPPORTED_METHODS = {
    0: {
        "label": "Bloch Decay Spectrum",
        "function": mr_lib.BlochDecaySpectrum,
        "spectral_dimensions": [SpectralDimension(count=512, spectral_width=25000)],
    },
    1: {
        "label": "Bloch Decay Central Transition Spectrum",
        "function": mr_lib.BlochDecayCTSpectrum,
        "spectral_dimensions": [SpectralDimension(count=512, spectral_width=25000)],
    },
    2: {
        "label": "Triple-quantum variable-angle spinning",
        "function": mr_lib.ThreeQ_VAS,
        "spectral_dimensions": [
            SpectralDimension(count=128, spectral_width=25000),
            SpectralDimension(count=512, spectral_width=25000),
        ],
    },
}


METHOD_OPTIONS = [
    {"label": value["label"], "value": key} for key, value in SUPPORTED_METHODS.items()
]

# title
head = dbc.ModalHeader("Select a method")

# method selection
method_selection = dcc.Dropdown(id="method-type", options=METHOD_OPTIONS, value=0)

# Channel selection
ch_label = dbc.InputGroupText("Channel")
ch_selection = dbc.Select(options=isotope_options_list, value="1H", id="channel")
channel_ui = dbc.InputGroup([ch_label, ch_selection], class_name="container")

# select button
button = dbc.Button(
    "Select",
    id="close-method-selection",
    color="dark",
    class_name="ml-auto",
    outline=True,
)

app.clientside_callback(
    "function(n1, n2, is_open) { return !is_open; }",
    Output("method-modal", "is_open"),
    Input("add-method-button", "n_clicks"),
    Input("close-method-selection", "n_clicks"),
    State("method-modal", "is_open"),
    prevent_initial_call=True,
)

method_selection_modal = dbc.Modal(
    [head, dbc.ModalBody(method_selection), channel_ui, dbc.ModalFooter(button)],
    is_open=False,
    id="method-modal",
)
