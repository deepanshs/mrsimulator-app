# -*- coding: utf-8 -*-
import json
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.exceptions import PreventUpdate

from . import baseline as Baseline
from . import convolution as Convolution
from . import scale as Scale
from app.sims.utils import expand_output
from app.sims.utils import update_processor_ui


def tools():
    """Add, duplicate, or remove methods"""
    items = [
        dbc.DropdownMenuItem("Amplitude Scalar", id="add-post_sim-scalar"),
        dbc.DropdownMenuItem("Baseline Offset", id="add-post_sim-baseline"),
        dbc.DropdownMenuItem("Convolutions", id="add-post_sim-convolution"),
    ]
    new = dbc.DropdownMenu(label="Add", children=items)

    return html.Div(children=new)


def refresh(data):
    """Refresh and update the signal processing UI elements.

    Args:
        data: The mrsim json data.
    """
    method_index = ctx.inputs["select-method.value"]

    mth = data["methods"]
    sys = data["spin_systems"]
    post = data["signal_processors"]

    method_index = method_index if len(mth) > method_index else 0
    n_dim, n_dv = len(mth[method_index]["spectral_dimensions"]), len(sys)
    print("py_dict", post[method_index])

    obj, i = [], 0
    for item in post[method_index]["operations"]:
        if item["function"] not in ["FFT", "IFFT"]:
            obj.append(
                FUNCTION_UI_REFRESH[item["function"]](i, item, n_dim=n_dim, n_dv=n_dv)
            )
        i += 1
    return obj


def function_to_id_index_map():
    """Maps signal processing functions to the state element id."""
    keys = ctx.states.keys()
    keys = [item for item in keys if '"function":' in item]
    dict_map = {}
    for k in keys:
        info = json.loads(k.split(".")[0])
        fn, index = info["function"], info["index"]
        if fn not in dict_map:
            dict_map[fn] = []
        dict_map[fn].append(index)
    return dict_map


def generate_signal_processor_dict(n_dims):
    """Iterate over all function and generate a SignalProcessor dict.

    Args:
        n_dims: Number of dimensions supported by the method.
    """
    dict_map = function_to_id_index_map()

    dims = [i for i in range(n_dims)]
    apodize = [{"dim_index": dims, "function": "IFFT"}]
    other = []
    [
        [apodize.append(FUNCTION_DICT[k](index)) for index in set(v)]
        if k == "apodization"
        else [other.append(FUNCTION_DICT[k](index)) for index in set(v)]
        for k, v in dict_map.items()
    ]
    apodize += [{"dim_index": dims, "function": "FFT"}]
    return {"operations": apodize + other}


def setup():
    method_index = ctx.inputs["select-method.value"]
    existing_data = ctx.states["local-mrsim-data.data"]

    if method_index is None:
        raise PreventUpdate

    mth_options = ctx.states["select-method.options"]
    print("method_options", mth_options)
    mth_options = [1] or mth_options

    if existing_data["signal_processors"] is None:
        existing_data["signal_processors"] = [{"operations": []} for _ in mth_options]
    return existing_data, method_index


def on_method_select():
    existing_data, _ = setup()
    processor = refresh(existing_data)
    return update_processor_ui(processor)


def on_remove_post_sim_function(index):
    """Remove the signal processing object at index `index`.

    Args:
        index: The index of the object to remove.
    """
    post_sim_obj = ctx.states["post_sim_child.children"]

    for i, item in enumerate(post_sim_obj):
        sub_item = item["props"]["children"][0]
        sub_sub_item = sub_item["props"]["children"]["props"]["children"][1]
        if sub_sub_item["props"]["id"]["index"] == index:
            index = i
            break

    del post_sim_obj[index]
    return update_processor_ui(post_sim_obj)


def on_submit_signal_processor_button():
    existing_data, method_index = setup()
    existing_process_data = existing_data["signal_processors"]

    n_dims = len(existing_data["methods"][method_index]["spectral_dimensions"])
    processor = generate_signal_processor_dict(n_dims)
    existing_process_data[method_index] = processor
    print("submit process_data", existing_process_data)

    out = {
        "alert": ["", False],
        "mrsim": [existing_data, no_update, int(datetime.now().timestamp() * 1000)],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }

    return expand_output(out)


CALLBACKS = {
    "scalar": Scale.refresh,
    "baseline": Baseline.refresh,
    "convolution": Convolution.refresh,
}

FUNCTION_DICT = {
    "scale": Scale.get_dict,
    "baseline": Baseline.get_dict,
    "apodization": Convolution.get_dict,
}

FUNCTION_UI_REFRESH = {
    "Scale": Scale.ui,
    "baseline": Baseline.ui,
    "apodization": Convolution.ui,
}
