# -*- coding: utf-8 -*-
from dash import no_update

from app.sims import home as home_UI
from app.sims import method as method_UI
from app.sims import post_simulation as post_sim_UI
from app.sims import spin_system as spin_system_UI
from app.sims.sidebar import N_ACTIVE_CONFIGS


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
        "mrsim": [no_update, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * N_ACTIVE_CONFIGS,
        "processor": [processor],
    }
    return expand_output(out)


def assemble_data(data):
    # data["trigger"] = {"simulation": True, "method_index": None}

    fields = {
        "integration_density": 70,
        "integration_volume": "Octant",
        "number_of_sidebands": 64,
        "isotropic_interpolation": "linear",
        # "number_of_gamma_angles": 1,
    }
    mrsim_config = [
        data["simulator"]["config"].get(key, value) for key, value in fields.items()
    ]
    # mrsim_config[-1] = no_update

    spin_system_overview = spin_system_UI.refresh(data["simulator"]["spin_systems"])
    method_overview = method_UI.refresh(data["simulator"]["methods"])
    home_overview = home_UI.refresh(data)
    post_sim_overview = (
        post_sim_UI.refresh(data) if data["simulator"]["methods"] != [] else []
    )

    out = {
        "alert": ["", False],
        "mrsim": [data, no_update],
        "children": [spin_system_overview, method_overview, home_overview],
        "mrsim_config": mrsim_config,
        "processor": [post_sim_overview],
    }
    return expand_output(out)


def on_fail_message(message):
    """Message to display on failure

    Args:
        ste message: The fail message.
    """
    out = {
        "alert": [message, True],
        "mrsim": [no_update, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * N_ACTIVE_CONFIGS,
        "processor": [no_update],
    }
    return expand_output(out)
