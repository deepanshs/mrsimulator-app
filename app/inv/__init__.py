# -*- coding: utf-8 -*-
import base64

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrinversion.kernel.nmr import ShieldingPALineshape
from mrinversion.linear_model import TSVDCompression

from .layout import page
from app import app
from app.sims.importer import load_csdm

# from mrinversion.linear_model import SmoothLassoLS

# from mrinversion.linear_model import SmoothLasso

SmoothLassoLS = None


mrinv = html.Div(
    [
        dbc.Navbar(
            html.Div(
                dcc.Link(
                    dbc.NavbarBrand("MRInversion", style={"color": "#d6d6d6"}), href="/"
                ),
                className="nav-burger",
            ),
            color=None,
            dark=None,
            expand="md",
        ),
        page,
    ],
    className="inv-page",
    # **{"data-app-link": ""},
)


@app.callback(
    [Output("INV-spectrum", "figure"), Output("INV-input-data", "data")],
    [Input("INV-upload-from-graph", "contents"), Input("INV-transpose", "n_clicks")],
    [State("INV-spectrum", "figure"), State("INV-input-data", "data")],
    prevent_initial_call=True,
)
def update_input_graph(contents, tr_val, figure, data):
    if contents is None:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "INV-upload-from-graph":
        content_string = contents.split(",")[1]
        decoded = base64.b64decode(content_string)
        success, exp_data, error_message = load_csdm(decoded)

        if not success:
            raise PreventUpdate

        [item.to("ppm", "nmr_frequency_ratio") for item in exp_data.x]
        x, y = [item.coordinates.value for item in exp_data.x]
        z = exp_data.y[0].components[0].real
        trace = go.Heatmap(x=x, y=y, z=z, colorscale="jet")
        figure["data"][0] = trace

        layout = figure["layout"]
        layout["xaxis"]["autorange"] = "reversed"
        layout["yaxis"]["autorange"] = "reversed"

        label = exp_data.x[0].label
        label = label if label not in [None, ""] else "frequency"
        layout["xaxis"]["title"] = f"{label} / ppm"

        label = exp_data.x[1].label
        label = label if label not in [None, ""] else "frequency"
        layout["yaxis"]["title"] = f"{label} / ppm"

        return [figure, exp_data.real.dict()]

    if trigger_id == "INV-transpose":
        if data is None:
            raise PreventUpdate
        data = cp.parse_dict(data).T

        figure["data"][0]["x"] = data.x[0].coordinates.value
        figure["data"][0]["y"] = data.x[1].coordinates.value
        figure["data"][0]["z"] = data.y[0].components[0]
        return [figure, data.dict()]


@app.callback(
    Output("INV-data-range", "data"),
    [Input("INV-spectrum", "relayoutData")],
    [State("INV-spectrum", "figure")],
    prevent_initial_call=True,
)
def display_relayout_data(relayoutData, fig):
    if relayoutData is None:
        raise PreventUpdate

    keys = relayoutData.keys()

    if "yaxis.range[0]" in keys:
        y = np.asarray(fig["data"][0]["y"])
        index_min = np.where(y > relayoutData["yaxis.range[0]"])[0][0]
        index_max = np.where(y < relayoutData["yaxis.range[1]"])[0][-1]
        range_zoom_y = np.sort([index_min, index_max])

    if "xaxis.range[0]" in keys:
        x = np.asarray(fig["data"][0]["x"])
        index_min = np.where(x > relayoutData["xaxis.range[0]"])[0][0]
        index_max = np.where(x < relayoutData["xaxis.range[1]"])[0][-1]
        range_zoom_x = np.sort([index_min, index_max])

    if "yaxis.range[0]" in keys and "xaxis.range[0]" in keys:
        print(range_zoom_x, range_zoom_y)
        return [range_zoom_x, range_zoom_y]

    if "yaxis.range[0]" in keys and "xaxis.range[0]" not in keys:
        print([0, -1], range_zoom_y)
        return [[0, -1], range_zoom_y]

    if "yaxis.range[0]" not in keys and "xaxis.range[0]" in keys:
        print(range_zoom_x, [0, -1])
        return [range_zoom_x, [0, -1]]

    if "xaxis.autorange" in keys:
        return [0, -1]

    raise PreventUpdate


@app.callback(
    Output("INV-kernel-rotor_angle", "value"),
    [Input("INV-kernel-type", "value")],
    prevent_initial_call=True,
)
def update_number_of_sidebands(k_typ):
    if k_typ == "sideband-correlation":
        return 54.735
    if k_typ == "MAF":
        return 90


@app.callback(
    Output("INV-kernel", "data"),
    [Input("INV-generate-kernel", "n_clicks")],
    [
        State("INV-input-data", "data"),
        State("INV-dimension-0-count", "value"),
        State("INV-dimension-0-increment", "value"),
        State("INV-dimension-1-count", "value"),
        State("INV-dimension-1-increment", "value"),
        State("INV-kernel-channel", "value"),
        State("INV-kernel-flux", "value"),
        State("INV-kernel-rotor_angle", "value"),
        State("INV-supersampling", "value"),
        State("INV-data-range", "data"),
        State("INV-kernel-type", "value"),
    ],
    prevent_initial_call=True,
)
def generate_kernel(
    n, data, count0, inc0, count1, inc1, channel, B0, theta, n_su, d_range, k_typ
):
    if data is None:
        raise PreventUpdate

    if d_range is None:
        d_range = [[0, -1], [0, -1]]

    data = cp.parse_dict(data)

    anisotropic_dimension = data.dimensions[0]
    inverse_dimensions = [
        cp.LinearDimension(count=count0, increment=f"{inc0} Hz", label="x"),
        cp.LinearDimension(count=count1, increment=f"{inc1} Hz", label="y"),
    ]

    vr = 0
    ns = 1

    if k_typ == "sideband-correlation":
        vr = anisotropic_dimension.increment.to("Hz")
        ns = anisotropic_dimension.count

    if k_typ == "MAF":
        vr = "1 GHz"
        ns = 1

    K = ShieldingPALineshape(
        anisotropic_dimension=anisotropic_dimension,
        inverse_dimension=inverse_dimensions,
        channel=channel,
        magnetic_flux_density=f"{B0} T",
        rotor_angle=f"{theta} °",
        rotor_frequency=f"{vr}",
        number_of_sidebands=ns,
    ).kernel(supersampling=int(n_su))

    ranges = slice(d_range[1][0], d_range[1][1], None)
    data_truncated = data[:, ranges]

    new_system = TSVDCompression(K, data_truncated)
    compressed_K = new_system.compressed_K
    compressed_s = new_system.compressed_s

    return {
        "kernel": compressed_K,
        "signal": compressed_s.dict(),
        "inverse_dimensions": [item.dict() for item in inverse_dimensions],
    }


@app.callback(
    [
        Output("INV-output", "figure"),
        Output("INV-l1", "value"),
        Output("INV-l2", "value"),
    ],
    [Input("INV-solve", "n_clicks")],
    [
        State("INV-l1", "value"),
        State("INV-l2", "value"),
        State("INV-kernel", "data"),
        State("INV-output", "figure"),
    ],
    prevent_initial_call=True,
)
def solve(n, l1, l2, data, fig):
    inverse_dimensions = [
        cp.LinearDimension(**item) for item in data["inverse_dimensions"]
    ]

    compressed_K = np.asarray(data["kernel"], dtype=np.float64)
    compressed_s = cp.parse_dict(data["signal"])

    # new_system = TSVDCompression(K, s)
    # compressed_K = new_system.compressed_K
    # compressed_s = new_system.compressed_s

    s_lasso = SmoothLassoLS(
        alpha=l2,
        lambda1=l1,
        inverse_dimension=inverse_dimensions,
        method="lars",
        tolerance=1e-3,
    )
    s_lasso.fit(K=compressed_K, s=compressed_s)
    # print(s_lasso.estimator.intercept_)
    # residue = s_lasso.residuals(K, s)

    res = s_lasso.f / s_lasso.f.max()

    [item.to("ppm", "nmr_frequency_ratio") for item in res.x]
    x, y, z = [item.coordinates.value for item in res.x]
    x_, y_, z_ = np.meshgrid(x, y, z, indexing="ij")

    trace = go.Volume(
        x=x_.ravel(),
        y=y_.ravel(),
        z=z_.ravel(),
        value=res.y[0].components[0].T.ravel(),
        isomin=0.05,
        isomax=0.95,
        opacity=0.1,  # needs to be small to see through all surfaces
        surface_count=25,  # needs to be a large number for good volume rendering
        colorscale="RdBu",
    )
    fig["data"][0] = trace
    return [fig, s_lasso.hyperparameters["lambda"], s_lasso.hyperparameters["alpha"]]
