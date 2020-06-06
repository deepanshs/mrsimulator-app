# -*- coding: utf-8 -*-
"""
    Model page layout and callbacks for advance settings.
    Advanced setting includes:
        - Integration density: Number of triangles along the edge of octahedron.
        - Integration volume: Enumeration with literals, 'octant', 'hemisphere'.
        - Number of sidebands: Number of sidebands to evaluate.
"""
import json
import os

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# {"label": "Spectrum (Comma Separated Values, .csv)", "value": "csv"},
# {"label": "Spectrum (Core Scientific Dataset Format, .csdf)", "value": "csdf"},

# Select format
select_format = dcc.Dropdown(
    id="select-format",
    options=[{"label": "Mrsimulator file (.JSON)", "value": "json"}],
    value="json",
    clearable=False,
    searchable=False,
)

# Download link
link = html.Div(id="download-div")

# Serialize the computed spectrum and download the serialized file.


@app.server.route("/downloads/<path:path>")
def serve_static(path):
    root_dir = os.getcwd()
    # time.sleep(1)
    return flask.send_from_directory(
        os.path.join(root_dir, "downloads"),
        path,
        as_attachment=True,
        conditional=True,
        mimetype="application/json",
    )


# update the link to the downloadable serialized file.
@app.callback(
    Output("download-href", "href"),
    [Input("select-format", "value"), Input("download-button", "n_clicks")],
    [
        State("local-processed-data", "data"),
        State("decompose", "active"),
        State("local-simulator-data", "data"),
    ],
    prevent_initial_call=True,
)
def file_download_link(
    format_value, fill, local_processed_data, decompose, simulator_data
):
    """Update the link to the downloadable file."""
    if simulator_data is None:
        raise PreventUpdate

    # uuid_1 = uuid.uuid1()
    name = simulator_data["name"]
    name = f"-{name}" if name != "" else ""

    for item in simulator_data["methods"]:
        for dv in item["simulation"]["csdm"]["dependent_variables"]:
            dv.pop("application")

    if format_value == "json":
        filename = f"SpinSystem{name}.json"
        relative_filename = os.path.join("downloads", filename)
        with open(relative_filename, "w") as f:
            json.dump(simulator_data, f)
        return relative_filename

    if local_processed_data is None:
        raise PreventUpdate

    content = local_processed_data
    if not decompose:
        data = cp.parse_dict(local_processed_data)
        d_ = 0
        for item in data.split():
            d_ += item
        content = d_.to_dict(update_timestamp=True)

    if format_value == "csdf":
        filename = f"Spectrum{name}.csdf"
        relative_filename = os.path.join("downloads", filename)
        with open(relative_filename, "w") as f:
            json.dump(content, f)
        return relative_filename

    if format_value == "csv":
        filename = f"Spectrum{name}.csv"
        relative_filename = os.path.join("downloads", filename)
        obj = cp.parse_dict(content)
        lst = []
        header = []
        lst.append(obj.dimensions[0].coordinates.to("Hz").value)
        header.append("frequency / Hz")
        for item in obj.dependent_variables:
            lst.append(item.components[0])
            header.append(
                item.application["com.github.DeepanshS.mrsimulator"]["spin_systems"][0][
                    "name"
                ]
            )
        header = ", ".join(header)
        np.savetxt(relative_filename, np.asarray(lst).T, delimiter=",", header=header)

        return relative_filename


# Layout ----------------------------------------------------------------------
# model user-interface
download_modal = dbc.Modal(
    [
        dbc.ModalHeader("Select download type"),
        dbc.ModalBody(dbc.FormGroup([select_format, link])),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Close",
                    id="close_download_setting",
                    color="dark",
                    className="mr-auto",
                    outline=True,
                ),
                html.A(
                    ["Download  ", html.I(className="fas fa-download fa-lg")],
                    href="",
                    id="download-href",
                    className="download-csdm-style",
                ),
            ]
        ),
    ],
    id="download-modal",
    role="document",
    className="modal-dialog",
)


# callback to toggle advance setting modal.
@app.callback(
    Output("download-modal", "is_open"),
    [Input("download-button", "n_clicks"), Input("close_download_setting", "n_clicks")],
    [State("download-modal", "is_open"), State("local-processed-data", "data")],
    prevent_initial_call=True,
)
def toggle_modal_setting(n1, n2, is_open, local_processed_data):
    """Model window for advance input."""
    if local_processed_data is None:
        raise PreventUpdate
    if n1 is None and n2 is None:
        raise PreventUpdate
    if n1 or n2:
        return not is_open
    return is_open
