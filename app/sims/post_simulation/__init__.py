# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.exceptions import PreventUpdate

from . import convolution as Convolution
from . import scale as Scale
from app.sims.utils import expand_output


def tools():
    """Add, duplicate, or remove methods"""
    # new = html.Button("add", id="add-post_sim-button")
    new = dbc.DropdownMenu(
        label="Add",
        children=[
            dbc.DropdownMenuItem("Amplitude Scalar", id="add-post_sim-scalar"),
            dbc.DropdownMenuItem("Convolutions", id="add-post_sim-convolutions"),
        ],
    )
    duplicate = html.Button("duplicate", id="duplicate-post_sim-button")
    remove = html.Button("remove", id="remove-post_sim-button")

    return html.Div(children=[new, duplicate, remove])


def refresh(data):
    method_index = ctx.inputs["select-method.value"]

    obj = []
    mth = data["methods"]
    sys = data["spin_systems"]
    post = data["signal_processors"]

    method_index = method_index if len(mth) > method_index else 0
    n_dim, n_dv = len(mth[method_index]["spectral_dimensions"]), len(sys)
    print("py_dict", post[method_index])

    for i, item in enumerate(post[method_index]["operations"]):
        if item["function"] == "apodization":
            obj.append(Convolution.ui(i, item, n_dim, n_dv))
        if item["function"] == "Scale":
            obj.append(Scale.ui(i, item))
    return obj


def cycle_over_all():
    operations = []
    keys = ctx.states.keys()
    keys = [item for item in keys if '"function":' in item]

    dict_ = {}
    for k in keys:
        info = eval(k.split(".")[0])
        fn = info["function"]
        index = info["index"]
        if fn not in dict_:
            dict_[fn] = []
        dict_[fn].append(index)

    for k, v in dict_.items():
        for index in set(v):
            if k == "apodization":
                operations.append(Convolution.get_apodization_dict(index))
            if k == "scale":
                operations.append(Scale.get_scale_dict(index))
    return operations


def generate_signal_processor_dict(n_dims):
    dims = [i for i in range(n_dims)]
    operations = [{"dim_index": dims, "function": "IFFT"}]
    operations += cycle_over_all()
    operations += [{"dim_index": dims, "function": "FFT"}]
    processor = {"operations": operations}
    return processor


def setup_processor(*args):
    method_index = ctx.inputs["select-method.value"]
    method_options = ctx.states["select-method.options"]
    existing_data = ctx.states["local-mrsim-data.data"]
    existing_process_data = existing_data["signal_processors"]
    if method_index is None:
        raise PreventUpdate

    print("method_options", method_options)
    method_options = [1] or method_options
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if existing_process_data is None:
        existing_process_data = [{"operations": []} for _ in method_options]

    if trigger_id == "signal-processor-button":

        n_dims = len(existing_data["methods"][method_index]["spectral_dimensions"])
        processor = generate_signal_processor_dict(n_dims)
        existing_process_data[method_index] = processor
        print("existing_process_data", existing_process_data)

        out = {
            "alert": ["", False],
            "mrsim": [existing_data, no_update],
            "children": [no_update] * 3,
            "mrsim_config": [no_update] * 4,
            "processor": [no_update],
        }

        return expand_output(out)

    # if method_index not in data:
    #     data[method_index] = {"operations": []}
    if trigger_id == "select-method":
        print("existing_process_data", existing_process_data)
        out = {
            "alert": ["", False],
            "mrsim": [no_update, no_update],
            "children": [no_update] * 3,
            "mrsim_config": [no_update] * 4,
            "processor": [refresh(existing_data)],
        }
        return expand_output(out)

    if trigger_id == "add-post_sim-convolutions":
        return Convolution.refresh()

    if trigger_id == "add-post_sim-scalar":
        return Scale.refresh()
