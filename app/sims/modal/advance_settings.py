# -*- coding: utf-8 -*-
"""
    Model page layout and callbacks for advance settings.
    Advance setting includes:
        - Integration density: Number of triangles along the edge of octahedron.
        - Integration volume: Enumeration with literals, 'octant', 'hemisphere'.
        - Number of sidebands: Number of sidebands to evaluate.
"""
from dash.dependencies import Input
from dash.dependencies import Output

from app import app


app.clientside_callback(
    """function (data) {
        if (data == null) { throw window.dash_clientside.PreventUpdate; }
        return data.auto_update.toString();
    }""",
    Output("auto-update", "children"),
    Input("user-config", "data"),
    prevent_initial_call=True,
)
