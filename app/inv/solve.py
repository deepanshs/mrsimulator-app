# -*- coding: utf-8 -*-
import csdmpy as cp
import numpy as np

# from mrinversion.linear_model import SmoothLassoCV

# from mrinversion.linear_model import SmoothLasso

# from mrinversion.linear_model import SmoothLassoLS


def solve(l1, l2, data):
    inverse_dimensions = [
        cp.LinearDimension(**item) for item in data["inverse_dimensions"]
    ]

    compressed_K = np.asarray(data["kernel"], dtype=np.float64)
    compressed_s = cp.parse_dict(data["signal"])

    print(compressed_K, compressed_s, inverse_dimensions)
    # s_lasso = SmoothLassoCV(
    #     # alpha=l2,
    #     # lambda1=l1,
    #     inverse_dimension=inverse_dimensions,
    #     # method="lars",
    #     tolerance=1e-3,
    # )
    # s_lasso = SmoothLasso(
    #     alpha=l2,
    #     lambda1=l1,
    #     inverse_dimension=inverse_dimensions,
    #     method="lars",
    #     tolerance=1e-3,
    # )
    # s_lasso.fit(K=compressed_K, s=compressed_s)
    # res = s_lasso.f / s_lasso.f.max()

    # return [
    #     res.to_dict(),
    #     s_lasso.hyperparameters["lambda"],
    #     s_lasso.hyperparameters["alpha"],
    # ]

    return [{}, 0, 0]
