# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .app import app
from .custom_widgets import custom_button
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
    [State("local-isotopomer-index-map", "data"), State("decompose", "active")],
)


# download
download_layout = html.Div(
    [
        custom_button(
            text="Download ",
            icon_classname="fas fa-download",
            id="download-button",
            tooltip="Download spectrum and isotopomers",
            outline=True,
            color="dark",
        ),
        download_modal,
    ]
)

sidebar = dbc.Card(
    dbc.CardBody(
        [data_info, download_layout], className="d-flex justify-content-between"
    ),
    className="my-card-sidebar",
    inverse=False,
    id="sidebar",
)
