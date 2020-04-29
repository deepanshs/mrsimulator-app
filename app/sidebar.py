# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .app import app
from .custom_widgets import custom_button
from .modal.advance_settings import advance_settings
from .modal.download import download_modal

colors = {"background": "#e2e2e2", "text": "#585858"}

# Info ------------------------------------------------------------------------------ #
isotopomers_info_button = custom_button(
    icon_classname="fas fa-info-circle",
    id="indicator_status",
    tooltip="Isotopomers info",
    outline=True,
    color="dark",
)

data_info = html.Div(
    [
        html.H5("Sample", id="filename_dataset"),
        html.P(
            "Sample description ... ",
            id="data_description",
            style={"textAlign": "left", "color": colors["text"]},
        ),
    ]
)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="selected_isotopomer"),
    Output("temp3", "children"),
    [Input("nmr_spectrum", "clickData")],
    [
        State("local-isotopomer-index-map", "data"),
        State("decompose", "active"),
        State("select-method", "value"),
    ],
)

sample_info = dbc.Card(
    dbc.CardBody(data_info), className="my-card-sidebar", inverse=False
)

# download
download_layout = html.Div(
    [
        custom_button(
            text="Download",
            icon_classname="fas fa-download",
            id="download-button",
            tooltip="Download spectrum and isotopomers",
            outline=True,
            color="dark",
        ),
        download_modal,
    ]
)

# Advanced settings ----------------------------------------------------------------- #
advance_setting_button = custom_button(
    text="Setting",
    icon_classname="fas fa-cog",
    id="advance_setting",
    tooltip="Advanced setting",
    outline=True,
    color="dark",
)
dimension_toolbar = html.Div([advance_setting_button, advance_settings])

# open mrsimulator file
mrsimulator_button = dcc.Upload(
    custom_button(
        text="Open",
        icon_classname="fas fa-folder-open",
        id="_open-mrsimulator-file",
        tooltip="Open mrsimulator file",
        outline=True,
        color="dark",
    ),
    id="open-mrsimulator-file",
)

master_toolbar = html.Div(
    [mrsimulator_button, dimension_toolbar, download_layout], className="master-toolbar"
)
