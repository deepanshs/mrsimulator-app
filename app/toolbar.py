# -*- coding: utf-8 -*-
import json
import os
import uuid

import csdmpy as cp
import dash_bootstrap_components as dbc
import flask
import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_switch


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# Scale amplitude ------------------------------------------------------------------- #
scale_amplitude_button = custom_switch(
    icon="fas fa-arrows-alt-v",
    id="normalize_amp",
    tooltip="Scale maximum amplitude to one.",
    outline=True,
    color="dark",
)


# Show spectrum from individual isotopomers ----------------------------------------- #
decompose_button = custom_switch(
    # text="decompose",
    icon="fas fa-chart-area",
    id="decompose",
    tooltip="Show simulation from individual isotopomers.",
    outline=True,
    color="dark",
)

# Button group ---------------------------------------------------------------------- #
group_1_buttons = dbc.ButtonGroup(
    [scale_amplitude_button, decompose_button],
    # className="btn-group mr-2",
)


# Download dataset ------------------------------------------------------------------ #
# Download button
collapsible_download_menu = dbc.Collapse(
    [
        dbc.DropdownMenuItem(
            "Download as CSDM, (.csdf)", id="download_csdm", external_link="True"
        ),
        dbc.DropdownMenuItem(
            "Download as CSV, (.csv)", id="download_csv", external_link="True"
        ),
    ],
    id="download-collapse",
)

# layout for the button
download_layout = [
    custom_button(
        icon="fas fa-download",
        id="download-button",
        tooltip="Download dataset",
        outline=True,
        color="dark",
    )
]


# toggle download collapsible
@app.callback(
    Output("download-collapse", "is_open"),
    [
        Input("download-button", "n_clicks_timestamp"),
        Input("download_csdm", "n_clicks_timestamp"),
        Input("download_csv", "n_clicks_timestamp"),
    ],
    [State("download-collapse", "is_open")],
)
def toggle_frame(n1, n2, n3, is_open):
    print(n1, n2, n3)
    if all(_ is None for _ in [n1, n2, n3]):
        print("---Download prevented---")
        raise PreventUpdate
    max_ = max(i for i in [n1, n2, n3] if i is not None)
    if max_ == n1:
        return not is_open
    if max_ in [n2, n3]:
        return False


# Serialize the computed spectrum and download the serialized file.
@app.server.route("/downloads/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, "downloads"), path, as_attachment=True
    )


# update the link to the downloadable serialized file.
@app.callback(
    [Output("download_csdm", "href"), Output("download_csv", "href")],
    [Input("download-button", "n_clicks")],
    [State("local-computed-data", "data")],
)
def file_download_link(n_clicks, local_computed_data):
    """Update the link to the downloadable file."""
    if local_computed_data is None:
        raise PreventUpdate
    if n_clicks is None:
        raise PreventUpdate

    uuid_1 = uuid.uuid1()
    relative_filename_csdm = os.path.join("downloads", f"{uuid_1}.csdf")
    with open(relative_filename_csdm, "w") as f:
        json.dump(local_computed_data, f)

    relative_filename_csv = os.path.join("downloads", f"{uuid_1}.csv")
    obj = cp.parse_dict(local_computed_data)
    lst = []
    header = []
    lst.append(obj.dimensions[0].coordinates.to("Hz").value)
    header.append("frequency / Hz")
    for item in obj.dependent_variables:
        lst.append(item.components[0])
        header.append(
            item.application["com.github.DeepanshS.mrsimulator"]["isotopomers"][0][
                "name"
            ]
        )
    header = ", ".join(header)
    np.savetxt(relative_filename_csv, np.asarray(lst).T, delimiter=",", header=header)
    return relative_filename_csdm, relative_filename_csv


# Button group 1 -------------------------------------------------------------------- #
group_2_buttons = dbc.ButtonGroup(download_layout)

# toolbar icons --------------------------------------------------------------------- #
toolbar = dbc.Row([dbc.Col(group_1_buttons), dbc.Col(group_2_buttons)])


# add callback for toggling the collapse on small screens
@app.callback(
    Output("toolbar-collapse", "is_open"),
    [Input("toolbar-toggler", "n_clicks")],
    [State("toolbar-collapse", "is_open")],
)
def toggle_toolbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
