# -*- coding: utf-8 -*-
import csdmpy as cp
import numpy as np
import plotly.graph_objs as go
from mrinversion.linear_model import SmoothLassoCV


def solve(l1, l2, data):
    inverse_dimensions = [
        cp.LinearDimension(**item) for item in data["inverse_dimensions"]
    ]

    compressed_K = np.asarray(data["kernel"], dtype=np.float64)
    compressed_s = cp.parse_dict(data["signal"])

    # s_lasso = SmoothLassoLS(
    #     alpha=l2,
    #     lambda1=l1,
    #     inverse_dimension=inverse_dimensions,
    #     method="lars",
    #     tolerance=1e-3,
    # )
    s_lasso = SmoothLassoCV(
        # alphas=l2,
        # lambdas=l1,
        inverse_dimension=inverse_dimensions,
        method="lars",
        tolerance=1e-3,
    )
    s_lasso.fit(K=compressed_K, s=compressed_s)

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
    fig = {"data": [trace]}
    return [fig, s_lasso.hyperparameters["lambda"], s_lasso.hyperparameters["alpha"]]
