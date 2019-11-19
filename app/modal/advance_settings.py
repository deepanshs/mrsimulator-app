# -*- coding: utf-8 -*-
"""
    Model page layout and callbacks for advance settings.
    Advance setting includes:
        - Integration density: Number of triangles along the edge of octahedron.
        - Integration volume: Enumeration with literals, 'octant', 'hemisphere'.
        - Number of sidebands: Number of sidebands to evaluate.
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# Number of triangles along the edge of octahedron.
integration_density = dbc.Row(
    [
        dbc.Col(dbc.Label("Integration density")),
        dbc.Col(
            dbc.Input(
                type="number",
                value=35,
                # type="slider",
                min=1,
                max=4096,
                step=1,
                id="integration_density",
            )
        ),
    ]
)

# Integration volume. Options are Octant, Hemisphere
integration_volume = dbc.Row(
    [
        dbc.Col(dbc.Label("Integration volume")),
        dbc.Col(
            dcc.Dropdown(
                id="integration_volume",
                options=[
                    {"label": "Octant", "value": "octant"},
                    {"label": "Hemisphere", "value": "hemisphere"},
                    # {"label": "Sphere", "value": 2},
                ],
                value="octant",
                clearable=False,
                searchable=False,
            )
        ),
    ]
)

# Field to hold information on the total number of averaging points.
integration_info = dbc.FormText(id="total_integration_points")


# callback for calculating total number of integration points
@app.callback(
    Output("total_integration_points", "children"),
    [Input("integration_density", "value"), Input("integration_volume", "value")],
)
def update_number_of_orientations(integration_density, integration_volume):
    """
    Update the number of orientation for powder averaging.
    Option for advance modal.
    """
    ori = int((integration_density + 1) * (integration_density + 2) / 2)
    if integration_volume == 0:
        return f"Averaging over {ori} orientations."
    if integration_volume == 1:
        return f"Averaging over {4*ori} orientations."


# Layout ----------------------------------------------------------------------
# model user-interface
advance_settings = dbc.Modal(
    [
        dbc.ModalHeader("Advance setting"),
        dbc.ModalBody(
            dbc.FormGroup([integration_density, integration_volume, integration_info])
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="close_setting",
                color="dark",
                className="ml-auto",
                outline=True,
            )
        ),
    ],
    id="modal_setting",
    role="document",
    className="modal-dialog",
)


# callback to toggle advance setting modal.
@app.callback(
    Output("modal_setting", "is_open"),
    [Input("advance_setting", "n_clicks"), Input("close_setting", "n_clicks")],
    [State("modal_setting", "is_open")],
)
def toggle_modal_setting(n1, n2, is_open):
    """Model window for advance input."""
    if n1 is None and n2 is None:
        raise PreventUpdate
    if n1 or n2:
        return not is_open
    return is_open
