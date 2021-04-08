# -*- coding: utf-8 -*-
def expand_output(out):
    """Plotly callback outputs for `update_simulator` function"""
    return [
        *out["alert"],
        *out["mrsim"],
        *out["children"],
        *out["mrsim_config"],
        *out["processor"],
    ]
