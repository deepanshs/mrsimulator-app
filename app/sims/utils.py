# -*- coding: utf-8 -*-
from dash import no_update


def expand_output(out):
    """Plotly callback outputs for `update_simulator` function"""
    return [
        *out["alert"],
        *out["mrsim"],
        *out["children"],
        *out["mrsim_config"],
        *out["processor"],
    ]


def update_processor_ui(processor):
    out = {
        "alert": ["", False],
        "mrsim": [no_update, no_update, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [processor],
    }
    return expand_output(out)
