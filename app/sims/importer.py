# -*- coding: utf-8 -*-
import base64
import json
import os
from urllib.request import urlopen

import csdmpy as cp
from csdmpy.dependent_variables.download import get_absolute_url_path
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import ALL
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import parse
from mrsimulator.utils import get_spectral_dimensions

from . import home as home_UI
from . import method as method_UI
from . import post_simulation as post_sim_UI
from . import spin_system as spin_system_UI
from .post_simulation import setup_processor
from .utils import expand_output
from app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

PATH = os.path.split(__file__)[0]


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
        # method->remove measurement
        Input("remove-measurement-from-method", "n_clicks"),
        # graph->drag and drop
        Input("upload-from-graph", "contents"),
        Input("url-search", "href"),
        # examples
        Input("selected-example", "value"),
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
        Input("signal-processor-button", "n_clicks"),
        Input("add-post_sim-scalar", "n_clicks"),
        Input("add-post_sim-convolutions", "n_clicks"),
        Input("select-method", "value"),
        # Input("new-method", "modified_timestamp"),
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
        State("post_sim_child", "children"),
        State("select-method", "options"),
    ],
    prevent_initial_call=True,
)
def update_simulator(*args):
    """Update the local spin-systems when a new file is imported."""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return CALLBACKS[trigger_id]()


def on_fail_message(message):
    """Message to display on failure

    Args:
        ste message: The fail message.
    """
    out = {
        "alert": [message, True],
        "mrsim": [no_update, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return expand_output(out)


def prep_valid_data_for_simulation(valid_data):
    """Generates output for callback when data is valid.

    Args:
        valid_data: mrsimulator dict
    """
    out = {
        "alert": ["", False],
        "mrsim": [valid_data, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return expand_output(out)


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
    for proc in existing_data["signal_processors"]:
        proc["operations"] = []
    return assemble_data(existing_data)


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
    return expand_output(out)


def on_method_change():
    """Update method attribute."""
    existing_data = ctx.states["local-mrsim-data.data"]
    new_method = ctx.states["new-method.data"]
    default = [no_update for _ in range(12)]
    if new_method is None:
        raise PreventUpdate

    existing_data["trigger"] = {"simulate": False}
    index = new_method["index"]
    method_data = new_method["data"]
    print("method_data type", new_method["operation"])

    # Add a new method
    if new_method["operation"] == "add":
        existing_data["methods"] += [method_data]
        methods_info = method_UI.refresh(existing_data["methods"])
        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        default[2], default[5] = existing_data, methods_info
        existing_data["trigger"]["method_index"] = [-1]

        if "signal_processors" not in existing_data:
            existing_data["signal_processors"] = []
        existing_data["signal_processors"] += [{"operations": []}]

        if len(existing_data["methods"]) == 1:
            default[-1] = []
        return default

    # Modify a method
    if new_method["operation"] == "modify":
        existing_data["methods"][index].update(method_data)
        # if "experiment" in existing_data["methods"][index]:
        #     method_data["experiment"] = existing_data["methods"][index]["experiment"]
        # existing_data["methods"][index] = method_data
        existing_data["methods"][index]["simulation"] = None
        methods_info = method_UI.refresh(existing_data["methods"])
        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        default[2], default[5] = existing_data, methods_info
        existing_data["trigger"]["method_index"] = [index]
        return default

    # Duplicate a method
    if new_method["operation"] == "duplicate":
        existing_data["methods"] += [method_data]
        existing_data["signal_processors"] += [{"operations": []}]
        methods_info = method_UI.refresh(existing_data["methods"])
        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        default[2], default[5] = existing_data, methods_info
        existing_data["trigger"] = {"simulate": False, "method_index": None}
        return default

    # Delete a method
    if new_method["operation"] == "delete":
        if index is None:
            raise PreventUpdate
        del existing_data["methods"][index]
        del existing_data["signal_processors"][index]
        existing_data["trigger"] = {"simulate": False, "method_index": None}
        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        methods_info = method_UI.refresh(existing_data["methods"])
        default[2], default[5] = existing_data, methods_info
        return default


def on_spin_system_change():
    """Update spin system attribute."""
    existing_data = ctx.states["local-mrsim-data.data"]
    new_spin_system = ctx.states["new-spin-system.data"]
    # config = {"is_new_data": False, "length_changed": False}
    config = no_update
    default = [no_update for _ in range(12)]

    if new_spin_system is None:
        raise PreventUpdate

    existing_data["trigger"] = {"simulation": True, "method_index": None}
    index = new_spin_system["index"]
    spin_system_data = new_spin_system["data"]
    print("new_spin_system type", new_spin_system["operation"])

    # Modify spin-system
    # The following section applies to when the spin-systems update is triggered from
    # the GUI fields. This is a very common trigger, so we place it at the start.
    if new_spin_system["operation"] == "modify":
        existing_data["spin_systems"][index] = spin_system_data
        # config["index_last_modified"] = index

        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(existing_data["spin_systems"])
        default[2], default[3], default[4] = existing_data, config, spin_systems_info
        return default

    # Add a new spin system
    # The following section applies to when the a new spin-systems is added from
    # add-spin-system-button.
    if new_spin_system["operation"] == "add":
        existing_data["spin_systems"] += [spin_system_data]
        # config["length_changed"] = True
        # config["added"] = [site["isotope"] for site in spin_system_data["sites"]]
        # config["index_last_modified"] = index

        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(existing_data["spin_systems"])
        default[2], default[3], default[4] = existing_data, config, spin_systems_info
        return default

    # Copy an existing spin-system
    # The following section applies to when a request to duplicate the spin-systems
    # is initiated using the duplicate-spin-system-button.
    if new_spin_system["operation"] == "duplicate":
        existing_data["spin_systems"] += [spin_system_data]
        # config["length_changed"] = True
        # config["added"] = [site["isotope"] for site in spin_system_data["sites"]]
        # config["index_last_modified"] = index

        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(existing_data["spin_systems"])
        default[2], default[3], default[4] = existing_data, config, spin_systems_info
        return default

    # Delete an spin-system
    # The following section applies to when a request to remove an spin-systems is
    # initiated using the remove-spin-system-button.
    if new_spin_system["operation"] == "delete":
        if index is None:
            raise PreventUpdate

        # the index to remove is given by spin_system_index
        # config["removed"] = [
        #     site["isotope"] for site in existing_data["spin_systems"][index]["sites"]
        # ]
        del existing_data["spin_systems"][index]
        # config["index_last_modified"] = index

        info_updates = home_UI.refresh(existing_data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(existing_data["spin_systems"])
        default[2], default[3], default[4] = existing_data, config, spin_systems_info
        return default


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

    mrsim_spectral_dims = get_spectral_dimensions(exp_data)

    for i, dim in enumerate(mrsim_spectral_dims):
        spectral_dim[i].update(dim)

    method_overview = method_UI.refresh(existing_data["methods"])

    out = {
        "alert": ["", False],
        "mrsim": [existing_data, no_update],
        "children": [no_update, method_overview, no_update],
        "mrsim_config": [no_update] * 4,
        "processor": [no_update],
    }
    return expand_output(out)


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


def load_file_from_url(url):
    """Load the selected data from url."""
    response = urlopen(url)
    contents = json.loads(response.read())
    return parse_file_contents(contents, url.endswith(".mrsys"))


def load_selected_example():
    """Load the selected example."""
    example = ctx.inputs["selected-example.value"]
    if example in ["", None]:
        raise PreventUpdate
    return load_file_from_url(get_absolute_url_path(example, PATH))


def import_from_url():
    """Import .mrsim file from url."""
    url_search = ctx.inputs["url-search.href"]
    print("url_search", url_search)
    if url_search in [None, ""]:
        raise PreventUpdate
    return load_file_from_url(url_search[3:])


def load_local_file(contents):
    """Parse contents from the spin-systems file."""
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    contents = json.loads(str(decoded, encoding="UTF-8"))
    return parse_file_contents(contents, isinstance(contents, list))


def import_mrsim_file():
    """Import .mrsim file from local file system."""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    contents = ctx.inputs[f"{trigger_id}.contents"]
    if contents is None:
        raise PreventUpdate
    return load_local_file(contents)


def parse_file_contents(content, spin_sys=False):
    content = {"spin_systems": content} if spin_sys else content

    # try:
    data = fix_missing_keys(content)
    return assemble_data(parse_data(data))
    # except Exception as e:
    #     message = f"FileReadError: {e}"
    #     return on_fail_message(message)


def fix_missing_keys(json_data):
    """Fill in missing data fields with default values."""
    default_data = {
        "name": "Sample",
        "description": "Add a description ...",
        "spin_systems": [],
        "methods": [],
        "config": {},
    }
    default_data.update(json_data)
    # data_keys = json_data.keys()
    # for k in default_data.keys():
    #     if k not in data_keys:
    #         json_data[k] = default_data[k]
    return default_data


def parse_data(data):
    """Parse units from the data and return a Simulator dict."""
    sim, signal_processors, params = parse(data, parse_units=True)
    for item in sim.methods:
        item.simulation = None

    sim = sim.json(include_methods=True, include_version=True)

    sim["signal_processors"] = [{"operations": []} for _ in sim["methods"]]
    if signal_processors is not None:
        for i, item in enumerate(signal_processors):
            sim["signal_processors"][i] = item.json()

    sim["params"] = None
    if params is not None:
        sim["params"] = params.dumps()

    return sim


def assemble_data(data):
    data["trigger"] = {"simulation": True, "method_index": None}

    fields = [
        "integration_density",
        "integration_volume",
        "number_of_sidebands",
        "decompose_spectrum",
    ]
    mrsim_config = [data["config"][item] for item in fields]
    mrsim_config[-1] = no_update

    spin_system_overview = spin_system_UI.refresh(data["spin_systems"])
    method_overview = method_UI.refresh(data["methods"])
    home_overview = home_UI.refresh(data)

    post_sim_view = post_sim_UI.refresh(data) if data["methods"] != [] else []
    out = {
        "alert": ["", False],
        "mrsim": [data, no_update],
        "children": [spin_system_overview, method_overview, home_overview],
        "mrsim_config": mrsim_config,
        "processor": [post_sim_view],
    }
    return expand_output(out)


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


def load_csdm(content):
    """Load a JSON file. Return a list with members
    - Success: True if file is read correctly,
    - Data: File content is success, otherwise an empty string,
    - message: An error message when JSON file load fails, else an empty string.
    """
    content = str(content, encoding="UTF-8")
    try:
        data = cp.loads(content)
        return True, data, ""
    except Exception as e:
        return False, "", e


CALLBACKS = {
    "save_info_modal": save_info_modal,
    "decompose": on_decompose_click,
    "close_setting": on_mrsim_config_change,
    "new-spin-system": on_spin_system_change,
    "new-method": on_method_change,
    "selected-example": load_selected_example,
    "url-search": import_from_url,
    "confirm-clear-spin-system": clear_spin_systems,
    "confirm-clear-methods": clear_methods,
    "upload-spin-system-local": import_mrsim_file,
    "open-mrsimulator-file": import_mrsim_file,
    "import-measurement-for-method": add_measurement_to_a_method,
    "upload-from-graph": add_measurement_to_a_method,
    "remove-measurement-from-method": remove_measurement_from_a_method,
    "signal-processor-button": setup_processor,
    "add-post_sim-scalar": setup_processor,
    "add-post_sim-convolutions": setup_processor,
    "select-method": setup_processor,
}
