# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .custom_widgets import custom_switch
from app.app import app
from app.custom_widgets import custom_button

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# Scale amplitude ------------------------------------------------------------------- #
scale_amplitude_button = custom_switch(
    # text="Normalize",
    icon_classname="fas fa-arrows-alt-v",
    id="normalize_amp",
    # size="sm",
    tooltip="Scale maximum amplitude to one.",
    outline=True,
    color="dark",
    style={"zIndex": 0},
)


# Show spectrum from individual spin systems ----------------------------------------- #
decompose_button = custom_switch(
    # text="Decompose",
    icon_classname="fac fa-decompose",
    id="decompose",
    # size="sm",
    tooltip="Decompose spectrum from individual spin systems.",
    outline=True,
    color="dark",
    style={"zIndex": 0},
)

# select method  -------------------------------------------------------------------- #
select_method = dcc.Dropdown(
    id="select-method",
    value=0,
    searchable=False,
    clearable=False,
    placeholder="View simulation from method ...",
)

download = custom_button(
    icon_classname="fas fa-download fa-lg",
    tooltip="Download Simulation from selected method",
    id="export-simulation-from-method",
    className="icon-button",
    module="html",
)
app.clientside_callback(
    ClientsideFunction(
        namespace="method", function_name="export_simulation_from_selected_method"
    ),
    Output("export-simulation-from-method-link", "href"),
    [Input("export-simulation-from-method", "n_clicks")],
    [State("local-processed-data", "data")],
    prevent_initial_call=True,
)
spectrum_download_link = html.A(
    id="export-simulation-from-method-link", style={"display": "none"}
)

# Button group ---------------------------------------------------------------------- #
toolbar = html.Div(
    [
        dbc.ButtonGroup([scale_amplitude_button, decompose_button]),
        html.Div([download, spectrum_download_link]),
    ]
)


# toolbar icons --------------------------------------------------------------------- #
toolbar_select_method = html.Div(select_method, style={"display": "none"})
