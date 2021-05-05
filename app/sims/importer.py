# -*- coding: utf-8 -*-
import base64
import json

import mrsimulator as mrsim
import numpy as np
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import ALL
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from lmfit import Minimizer
from lmfit import Parameters
from lmfit.printfuncs import fitreport_html_table
from mrsimulator.utils import get_spectral_dimensions
from mrsimulator.utils.spectral_fitting import LMFIT_min_function
from mrsimulator.utils.spectral_fitting import update_mrsim_obj_from_params

from . import home as home_UI
from . import io as sim_IO
from . import method as method_UI
from . import post_simulation as post_sim_UI
from . import spin_system as spin_system_UI
from . import utils as sim_utils
from app import app
from app.utils import load_csdm

# from lmfit import fit_report

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


# method
# Import or update the spin-systems.
@app.callback(
    [
        Output("alert-message-import", "children"),
        Output("alert-message-import", "is_open"),
        Output("local-mrsim-data", "data"),
        Output("config", "data"),
        Output("spin-system-read-only", "children"),
        Output("method-read-only", "children"),
        Output("info-read-only", "children"),
        Output("integration_density", "value"),
        Output("integration_volume", "value"),
        Output("number_of_sidebands", "value"),
        Output("decompose", "n_click"),
        Output("post_sim_child", "children"),
    ],
    [
        # main page->drag and drop
        Input("upload-spin-system-local", "contents"),
        # from file->open
        Input("open-mrsimulator-file", "contents"),
        # spin-system->import+add
        # Input("upload-and-add-spin-system-button", "contents"),
        # method->add measurement
        Input("import-measurement-for-method", "contents"),
        Input("add-measurement-for-method", "contents"),
        Input("upload-measurement-from-graph", "contents"),
        # method->remove measurement
        Input("remove-measurement-from-method", "n_clicks"),
        # url search input
        Input("url-search", "href"),
        # when spin-system is modified
        Input("new-spin-system", "modified_timestamp"),
        # when method is modified
        Input("new-method", "modified_timestamp"),
        # spin-system->clear
        Input("confirm-clear-spin-system", "submit_n_clicks"),
        # method->clear
        Input("confirm-clear-methods", "submit_n_clicks"),
        # decompose into spin systems
        Input("decompose", "active"),
        # integration and sideband settings
        Input("close_setting", "n_clicks"),
        Input("save_info_modal", "n_clicks"),
        # post simulation triggers
        Input("submit-signal-processor-button", "n_clicks"),
        Input("add-post_sim-scalar", "n_clicks"),
        Input("add-post_sim-constant_offset", "n_clicks"),
        Input("add-post_sim-convolution", "n_clicks"),
        Input("select-method", "value"),
        # Input("new-method", "modified_timestamp"),
        Input("trigger-fit", "data"),
        Input("trigger-sim", "data"),
        Input({"type": "remove-post_sim-functions", "index": ALL}, "n_clicks"),
    ],
    [
        # State("upload-spin-system-url", "value"),
        State("local-mrsim-data", "data"),
        State("new-spin-system", "data"),
        State("new-method", "data"),
        State("select-method", "value"),
        State("decompose", "n_clicks"),
        State("integration_density", "value"),
        State("integration_volume", "value"),
        State("number_of_sidebands", "value"),
        State("info-name-edit", "value"),
        State("info-description-edit", "value"),
        # post_sim states
        State({"function": "apodization", "args": "type", "index": ALL}, "value"),
        State({"function": "apodization", "args": "FWHM", "index": ALL}, "value"),
        State({"function": "apodization", "args": "dim_index", "index": ALL}, "value"),
        State({"function": "apodization", "args": "dv_index", "index": ALL}, "value"),
        State({"function": "scale", "args": "factor", "index": ALL}, "value"),
        State({"function": "constant_offset", "args": "offset", "index": ALL}, "value"),
        State("post_sim_child", "children"),
        State("select-method", "options"),
        State("params-data", "data"),
    ],
    prevent_initial_call=True,
)
def update_simulator(*args):
    """Update the local spin-systems when a new file is imported."""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("trigger_id", trigger_id)
    if trigger_id.startswith("{"):
        py_dict = json.loads(trigger_id)
        index, trigger_id = py_dict["index"], py_dict["type"]
        return CALLBACKS[trigger_id](index)

    return CALLBACKS[trigger_id]()


def prep_valid_data_for_simulation(valid_data):
    """Generates output for callback when data is valid.

    Args:
        valid_data: mrsimulator dict.
    """
    out = {
        "alert": ["", False],
        "mrsim": [valid_data, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return sim_utils.expand_output(out)


def on_decompose_click():
    """Toggle mrsim.config.decompose_spectrum between `spin_system` and `none`"""
    existing_data = ctx.states["local-mrsim-data.data"]
    print(ctx.inputs["decompose.active"], ctx.states["decompose.n_clicks"])
    decompose = "spin_system" if ctx.inputs["decompose.active"] else "none"
    existing_data["trigger"] = {"simulate": True, "method_index": None}
    existing_data["config"]["decompose_spectrum"] = decompose
    return prep_valid_data_for_simulation(existing_data)


def on_mrsim_config_change():
    """Update the mrsim.config dict. Only includes density, volume, and #sidebands"""
    existing_data = ctx.states["local-mrsim-data.data"]
    fields = ["integration_density", "integration_volume", "number_of_sidebands"]

    # if existing_data is not None:
    print(existing_data["config"])
    existing_data["trigger"] = {"simulate": True, "method_index": None}

    for item in fields:
        existing_data["config"][item] = ctx.states[f"{item}.value"]

    return prep_valid_data_for_simulation(existing_data)


def clear(attribute):
    """Clear the list of attributes.

    Args:
        attribute: Enumeration literals---`spin_systems` or `methods`
    """
    existing_data = ctx.states["local-mrsim-data.data"]
    existing_data[attribute] = []
    existing_data["trigger"] = {"simulate": True, "method_index": None}
    if "signal_processors" in existing_data:
        for proc in existing_data["signal_processors"]:
            proc["operations"] = []
    return sim_utils.assemble_data(existing_data)


def clear_spin_systems():
    """Clean all spin systems in the mrsim file."""
    return clear("spin_systems")


def clear_methods():
    """Clean all methods in the mrsim file."""
    return clear("methods")


def save_info_modal():
    """Save the title and description of mrsim data."""
    existing_data = ctx.states["local-mrsim-data.data"]
    existing_data["name"] = ctx.states["info-name-edit.value"]
    existing_data["description"] = ctx.states["info-description-edit.value"]
    existing_data["trigger"] = {"simulate": False, "method_index": None}
    # Update home overview with the title and description
    home_overview = home_UI.refresh(existing_data)
    out = {
        "alert": ["", False],
        "mrsim": [existing_data, no_update],
        "children": [no_update, no_update, home_overview],
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return sim_utils.expand_output(out)


def on_method_update():
    """Update method attribute."""

    def generate_outputs(existing_data, n=None):
        home_overview = home_UI.refresh(existing_data)
        method_overview = method_UI.refresh(existing_data["methods"])

        out = {
            "alert": ["", False],
            "mrsim": [existing_data, no_update],
            "children": [no_update, method_overview, home_overview],
            "mrsim_config": [no_update] * 4,
            "processor": [[]] if len(existing_data["methods"]) == n else [no_update],
        }
        return sim_utils.expand_output(out)

    existing_data = ctx.states["local-mrsim-data.data"]
    new_method = ctx.states["new-method.data"]
    if new_method is None:
        raise PreventUpdate

    existing_data["trigger"] = {"simulate": False}
    index = new_method["index"]
    method_data = new_method["data"]
    print("method_data type", new_method["operation"])

    # Add a new method
    if new_method["operation"] == "add":
        existing_data["methods"] += [method_data]
        existing_data["trigger"]["method_index"] = [-1]
        if "signal_processors" not in existing_data:
            existing_data["signal_processors"] = []
        existing_data["signal_processors"] += [{"operations": []}]
        return generate_outputs(existing_data, n=1)

    # Modify a method
    if new_method["operation"] == "modify":
        existing_data["methods"][index].update(method_data)
        existing_data["methods"][index]["simulation"] = None
        existing_data["trigger"]["method_index"] = [index]
        return generate_outputs(existing_data)

    # Duplicate an existing method
    if new_method["operation"] == "duplicate":
        existing_data["methods"] += [method_data]
        existing_data["signal_processors"] += [{"operations": []}]
        existing_data["trigger"] = {"simulate": False, "method_index": None}
        return generate_outputs(existing_data)

    # Delete a method
    if new_method["operation"] == "delete":
        del existing_data["methods"][index]
        del existing_data["signal_processors"][index]
        existing_data["trigger"] = {"simulate": False, "method_index": None}
        return generate_outputs(existing_data, n=0)


def on_spin_system_change():
    """Update spin system attribute."""

    def generate_outputs(existing_data):
        home_overview = home_UI.refresh(existing_data)
        spin_system_overview = spin_system_UI.refresh(existing_data["spin_systems"])

        out = {
            "alert": ["", False],
            "mrsim": [existing_data, no_update],
            "children": [spin_system_overview, no_update, home_overview],
            "mrsim_config": [no_update] * 4,
            "processor": [no_update],
        }
        return sim_utils.expand_output(out)

    existing_data = ctx.states["local-mrsim-data.data"]
    new_spin_system = ctx.states["new-spin-system.data"]

    if new_spin_system is None:
        raise PreventUpdate

    existing_data["trigger"] = {"simulation": True, "method_index": None}
    index = new_spin_system["index"]
    spin_system_data = new_spin_system["data"]
    print("new_spin_system type", new_spin_system["operation"])

    # Add a new spin system
    if new_spin_system["operation"] == "add":
        existing_data["spin_systems"] += [spin_system_data]
        return generate_outputs(existing_data)

    # Modify a spin-system
    if new_spin_system["operation"] == "modify":
        existing_data["spin_systems"][index] = spin_system_data
        return generate_outputs(existing_data)

    # Duplicate an existing spin-system
    if new_spin_system["operation"] == "duplicate":
        existing_data["spin_systems"] += [spin_system_data]
        return generate_outputs(existing_data)

    # Delete a spin-system
    if new_spin_system["operation"] == "delete":
        del existing_data["spin_systems"][index]
        return generate_outputs(existing_data)


def add_measurement_to_a_method():
    """Add a measurement to the selected method."""
    existing_data = ctx.states["local-mrsim-data.data"]
    existing_data["trigger"] = {
        "simulation": False,
        "internal_processor": False,
    }

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    contents = ctx.inputs[f"{trigger_id}.contents"]
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    success, exp_data, error_message = load_csdm(decoded)

    if not success:
        e = f"Error reading file. {error_message}"
        return [e, True, no_update, *([no_update] * 9)]

    index = ctx.states["select-method.value"]
    method = existing_data["methods"][index]
    method["experiment"] = exp_data.to_dict()
    spectral_dim = method["spectral_dimensions"]

    mrsim_spectral_dims = get_spectral_dimensions(exp_data, units=True)

    for i, dim in enumerate(mrsim_spectral_dims):
        spectral_dim[i].update(dim)

    method_overview = method_UI.refresh(existing_data["methods"])

    post_sim_overview = no_update
    if existing_data["signal_processors"][index] in [None, {"operations": []}]:
        vector = exp_data.y[0].components[0].real
        amp = vector.sum()
        existing_data["signal_processors"][index]["operations"] = [
            {"dim_index": [0], "function": "IFFT"},
            {
                "dim_index": [0],
                "FWHM": "200 Hz",
                "function": "apodization",
                "type": "Exponential",
            },
            {"dim_index": [0], "function": "FFT"},
            {"factor": amp / 30, "function": "Scale"},
        ]
        post_sim_overview = post_sim_UI.refresh(existing_data)

    out = {
        "alert": ["", False],
        "mrsim": [existing_data, no_update],
        "children": [no_update, method_overview, no_update],
        "mrsim_config": [no_update] * 4,
        "processor": [post_sim_overview],
    }
    return sim_utils.expand_output(out)


def remove_measurement_from_a_method():
    """Remove measurement from the selected method."""
    existing_data = ctx.states["local-mrsim-data.data"]
    existing_data["trigger"] = {
        "simulation": False,
        "internal_processor": False,
    }
    index = ctx.states["select-method.value"]
    method = existing_data["methods"][index]
    method["experiment"] = None
    return prep_valid_data_for_simulation(existing_data)


def simulate_test():
    print("The Simulate Spectrum button has been clicked")
    mrsim_data = ctx.states["local-mrsim-data.data"]
    params_data = ctx.states["params-data.data"]

    if mrsim_data is None:
        raise PreventUpdate

    if len(mrsim_data["methods"]) == 0 or len(mrsim_data["spin_systems"]) == 0:
        raise PreventUpdate

    sim, processor, saved_params = mrsim.parse(mrsim_data)
    params = Parameters().loads(params_data)

    update_mrsim_obj_from_params(params, sim, processor)
    new_mrsim_data = mrsim.dict(sim, processor, saved_params)

    out = {
        "alert": ["", False],
        "mrsim": [new_mrsim_data, no_update],
        "children": [no_update, no_update, no_update],
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return sim_utils.expand_output(out)


def least_squares_fit():
    mrsim_data = ctx.states["local-mrsim-data.data"]
    params_data = ctx.states["params-data.data"]

    if mrsim_data is None:
        raise PreventUpdate

    if len(mrsim_data["methods"]) == 0 or len(mrsim_data["spin_systems"]) == 0:
        raise PreventUpdate

    # try:
    sim, processor, _ = mrsim.parse(mrsim_data)

    check_for_exp = np.asarray([mth.experiment is None for mth in sim.methods])
    check_for_exp = np.where(check_for_exp == 1)[0]
    if check_for_exp.size != 0:
        return sim_utils.on_fail_message(
            "LeastSquaresAnalysisError: Please attach measurement(s) for method(s) at "
            f"index(es) {check_for_exp} before performing the least-squares analysis."
        )

    for mth in sim.methods:
        mth.experiment = mth.experiment.real

    # Optimize the script by pre-setting the transition pathways for each spin system
    # from the method.
    for sys in sim.spin_systems:
        sys.transition_pathways = sim.methods[0].get_transition_pathways(sys)

    # noise standard deviation
    sigma = []
    for mth in sim.methods:
        csdm_application = mth.experiment.dependent_variables[0].application
        sigma.append(csdm_application["com.github.DeepanshS.mrsimulator"]["sigma"])

    print("sigma", sigma)

    decompose = sim.config.decompose_spectrum[:]
    sim.config.decompose_spectrum = "spin_system"

    params = Parameters().loads(params_data)

    minner = Minimizer(LMFIT_min_function, params, fcn_args=(sim, processor, sigma))
    result = minner.minimize()
    # print(fit_report(result))

    sim.config.decompose_spectrum = decompose
    for sys in sim.spin_systems:
        sys.transition_pathways = None

    fit_data = mrsim.dict(sim, processor, result.params)
    fit_data["report"] = fitreport_html_table(result)

    print("IMPORTER")
    print(result.params.dumps())

    spin_system_overview = spin_system_UI.refresh(fit_data["spin_systems"])
    method_overview = method_UI.refresh(fit_data["methods"])
    home_overview = home_UI.refresh(fit_data)
    post_sim_overview = (
        post_sim_UI.refresh(fit_data) if fit_data["methods"] != [] else []
    )
    out = {
        "alert": ["", False],
        "mrsim": [fit_data, no_update],
        "children": [spin_system_overview, method_overview, home_overview],
        "mrsim_config": [no_update] * 4,
        "processor": [post_sim_overview],
    }
    return sim_utils.expand_output(out)


CALLBACKS = {
    "save_info_modal": save_info_modal,
    "decompose": on_decompose_click,
    "close_setting": on_mrsim_config_change,
    "new-spin-system": on_spin_system_change,
    "new-method": on_method_update,
    "url-search": sim_IO.import_file_from_url,
    "upload-spin-system-local": sim_IO.import_mrsim_file,
    "open-mrsimulator-file": sim_IO.import_mrsim_file,
    "confirm-clear-spin-system": clear_spin_systems,
    "confirm-clear-methods": clear_methods,
    "import-measurement-for-method": add_measurement_to_a_method,
    "add-measurement-for-method": add_measurement_to_a_method,
    "upload-measurement-from-graph": add_measurement_to_a_method,
    "remove-measurement-from-method": remove_measurement_from_a_method,
    "submit-signal-processor-button": post_sim_UI.on_submit_signal_processor_button,
    "add-post_sim-scalar": post_sim_UI.CALLBACKS["scalar"],
    "add-post_sim-constant_offset": post_sim_UI.CALLBACKS["constant_offset"],
    "add-post_sim-convolution": post_sim_UI.CALLBACKS["convolution"],
    "remove-post_sim-functions": post_sim_UI.on_remove_post_sim_function,
    "select-method": post_sim_UI.on_method_select,
    "trigger-sim": simulate_test,
    "trigger-fit": least_squares_fit,
}


# convert client-side function
@app.callback(
    Output("select-method", "options"),
    [Input("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
def update_list_of_methods(data):
    if data is None:
        raise PreventUpdate
    if data["methods"] is None:
        raise PreventUpdate
    options = [
        {"label": f'Method-{i} (Channel-{", ".join(k["channels"])})', "value": i}
        for i, k in enumerate(data["methods"])
    ]
    return options


# @app.callback(
#     Output("select-method", "value"),
#     Input("select-method", "options"),
#     State("select-method", "value"),
# )
# def update_method_index(options, val):
#     if len(options) >= val:
#         return len(options) - 1
#     raise PreventUpdate

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="onReload"),
    Output("temp2", "children"),
    [Input("local-mrsim-data", "data")],
    prevent_initial_call=True,
)
