# -*- coding: utf-8 -*-
import base64
import json
import os
from urllib.request import urlopen

import csdmpy as cp
from csdmpy.dependent_variables.download import get_absolute_url_path
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Simulator
from mrsimulator.utils import get_spectral_dimensions

from . import home as home_UI
from . import nmr_method as methods_UI
from . import spin_system as spin_system_UI
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
    ],
    prevent_initial_call=True,
)
def update_simulator(*args):
    """Update the local spin-systems when a new file is imported."""
    # if not ctx.triggered:
    #     raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("trigger-id", trigger_id)

    # existing_data = ctx.states["local-mrsim-data.data"]
    return CALLBACKS[trigger_id]()

    # if trigger_id == "save_info_modal":
    #     return save_info_modal()

    # # when decompose is triggered, return the updated existing data
    # if trigger_id == "decompose":
    #     return update_decompose()

    # if trigger_id == "close_setting":
    #     return update_sim_config()

    # # Add a new spin system object
    # if trigger_id == "new-spin-system":
    #     return modified_spin_system()

    # # Add a new method object
    # if trigger_id == "new-method":
    #     return modified_method()

    # # Load an example from pre-defined examples
    # if trigger_id == "selected-example":
    #     return example_selection()

    # # Request load file from url
    # if trigger_id == "url-search":
    #     return import_from_url()

    # # clear all spin systems
    # if trigger_id == "confirm-clear-spin-system":
    #     return clear("spin_systems", existing_data)

    # # clear all methods
    # if trigger_id == "confirm-clear-methods":
    #     return clear("methods", existing_data)

    # # Request load file from local file system
    # if trigger_id in ["upload-spin-system-local", "open-mrsimulator-file"]:
    #     return import_mrsim_file()

    # # Request load experiment from local file system
    # if trigger_id in ["import-measurement-for-method", "upload-from-graph"]:
    #     return import_measurement_for_method()

    # # Request remove experiment from the selected method
    # if trigger_id == "remove-measurement-from-method":
    #     return remove_measurement_from_method()


def update_decompose():
    existing_data = ctx.states["local-mrsim-data.data"]
    print(ctx.inputs["decompose.active"], ctx.states["decompose.n_clicks"])
    decompose = "spin_system" if ctx.inputs["decompose.active"] else "none"
    if existing_data is not None:
        existing_data["trigger"] = True
        existing_data["config"]["decompose_spectrum"] = decompose

    return ["", False, existing_data, *([no_update] * 8)]


def update_sim_config():
    existing_data = ctx.states["local-mrsim-data.data"]
    fields = ["integration_density", "integration_volume", "number_of_sidebands"]

    if existing_data is not None:
        print(existing_data["config"])
        existing_data["trigger"] = True
        for item in fields:
            existing_data["config"][item] = ctx.states[f"{item}.value"]

    return ["", False, existing_data, *([no_update] * 8)]


def clear(attribute):
    """Clear the list of spin-systems or methods

    Args:
        attribute: Enumeration with literals---`spin_systems` or `methods`
        existing_data: The existing simulator data and metadata.
    """
    existing_data = ctx.states["local-mrsim-data.data"]
    if existing_data is None:
        raise PreventUpdate
    existing_data[attribute] = []
    return assemble_data(existing_data)


def clear_spin_systems():
    return clear("spin_systems")


def clear_methods():
    return clear("methods")


# def update_existing_data(ctx):
#     existing_data = ctx.states["local-mrsim-data.data"]
#     decompose = "spin_system" if ctx.states["decompose.active"] else "none"
#     density = ctx.states["integration_density.value"]
#     volume = ctx.states["integration_volume.value"]
#     n_ssb = ctx.states["number_of_sidebands.value"]
#     if existing_data is not None:
#         existing_data["trigger"] = True
#         if "config" in existing_data:
#             existing_data["config"]["decompose_spectrum"] = decompose
#             existing_data["config"]["integration_density"] = density
#             existing_data["config"]["integration_volume"] = volume
#             existing_data["config"]["number_of_sidebands"] = n_ssb


def save_info_modal():
    existing_data = ctx.states["local-mrsim-data.data"]
    if existing_data is not None:
        existing_data["name"] = ctx.states["info-name-edit.value"]
        existing_data["description"] = ctx.states["info-description-edit.value"]
    else:
        existing_data = {
            "name": ctx.states["info-name-edit.value"],
            "description": ctx.states["info-description-edit.value"],
            "spin_systems": [],
            "methods": [],
        }

    existing_data["trigger"] = False

    home_overview = home_UI.refresh(existing_data)
    return [
        "",
        False,
        existing_data,
        *([no_update] * 3),
        home_overview,
        *([no_update] * 4),
    ]


def import_from_url():
    existing_data = ctx.states["local-mrsim-data.data"]
    url_search = ctx.inputs["url-search.href"]
    decompose = "spin_system" if ctx.inputs["decompose.active"] else "none"
    print("url_search", url_search)
    # print("url-search.href", url_search)
    if url_search in [None, ""]:
        raise PreventUpdate
    return load_from_url(url_search[3:], existing_data, decompose)


def import_mrsim_file():
    existing_data = ctx.states["local-mrsim-data.data"]
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    contents = ctx.inputs[f"{trigger_id}.contents"]
    if contents is None:
        raise PreventUpdate
    try:
        content = {}
        content_json = parse_contents(contents)
        if isinstance(content_json, list):
            content["spin_systems"] = content_json
        else:
            content = content_json
        data = fix_missing_keys(content)
    except Exception:
        message = "Error reading spin-systems."
        return [message, True, existing_data, *([no_update * 8])]
    return assemble_data(parse_data(data))


def import_measurement_for_method():
    existing_data = ctx.states["local-mrsim-data.data"]
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    contents = ctx.inputs[f"{trigger_id}.contents"]
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    success, exp_data, error_message = load_csdm(decoded)

    if not success:
        e = f"Error reading file. {error_message}"
        return [e, True, no_update, *([no_update] * 8)]

    index = ctx.states["select-method.value"]
    method = existing_data["methods"][index]
    method["experiment"] = exp_data.to_dict()
    spectral_dim = method["spectral_dimensions"]

    mrsim_spectral_dims = get_spectral_dimensions(exp_data)

    for i, dim in enumerate(mrsim_spectral_dims):
        spectral_dim[i].update(dim)

    method_overview = methods_UI.refresh(existing_data["methods"])
    return [
        "",
        False,
        existing_data,
        *([no_update] * 2),
        method_overview,
        *([no_update] * 5),
    ]


def remove_measurement_from_method():
    existing_data = ctx.states["local-mrsim-data.data"]
    index = ctx.states["select-method.value"]
    method = existing_data["methods"][index]
    method["experiment"] = None
    return ["", False, existing_data, *([no_update] * 8)]


def modified_method():
    existing_data = ctx.states["local-mrsim-data.data"]
    new_method = ctx.states["new-method.data"]
    default = [no_update for _ in range(11)]
    if new_method is None:
        raise PreventUpdate

    index = new_method["index"]
    data = (
        existing_data
        if existing_data is not None
        else {"name": "", "description": "", "spin_systems": [], "methods": []}
    )
    method_data = new_method["data"]
    print("method_data type", new_method["operation"])
    # Add a new method
    if new_method["operation"] == "add":
        data["methods"] += [method_data]
        methods_info = methods_UI.refresh(data["methods"])
        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        default[2], default[5] = data, methods_info
        return default

    # Modify a method
    if new_method["operation"] == "modify":
        if "experiment" in data["methods"][index]:
            method_data["experiment"] = data["methods"][index]["experiment"]
        data["methods"][index] = method_data
        methods_info = methods_UI.refresh(data["methods"])
        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        default[2], default[5] = data, methods_info
        return default

    # Duplicate a method
    if new_method["operation"] == "duplicate":
        data["methods"] += [method_data]
        methods_info = methods_UI.refresh(data["methods"])
        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        default[2], default[5] = data, methods_info
        return default

    # Delete a method
    if new_method["operation"] == "delete":
        if index is None:
            raise PreventUpdate
        del data["methods"][index]
        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        methods_info = methods_UI.refresh(data["methods"])
        default[2], default[5] = data, methods_info
        return default


def modified_spin_system():
    """Update the local spin-system data when an update is triggered."""
    existing_data = ctx.states["local-mrsim-data.data"]
    new_spin_system = ctx.states["new-spin-system.data"]
    config = {"is_new_data": False, "length_changed": False}
    default = [no_update for _ in range(11)]

    if new_spin_system is None:
        raise PreventUpdate
    index = new_spin_system["index"]
    data = (
        existing_data
        if existing_data is not None
        else {"name": "", "description": "", "spin_systems": [], "methods": []}
    )
    spin_system_data = new_spin_system["data"]
    print("new_spin_system type", new_spin_system["operation"])
    # Modify spin-system
    # The following section applies to when the spin-systems update is triggered from
    # the GUI fields. This is a very common trigger, so we place it at the start.
    if new_spin_system["operation"] == "modify":
        data["spin_systems"][index] = spin_system_data
        config["index_last_modified"] = index

        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(data["spin_systems"])
        default[2], default[3], default[4] = data, config, spin_systems_info
        return default

    # Add a new spin system
    # The following section applies to when the a new spin-systems is added from
    # add-spin-system-button.
    if new_spin_system["operation"] == "add":
        data["spin_systems"] += [spin_system_data]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in spin_system_data["sites"]]
        config["index_last_modified"] = index

        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(data["spin_systems"])
        default[2], default[3], default[4] = data, config, spin_systems_info
        return default

    # Copy an existing spin-system
    # The following section applies to when a request to duplicate the spin-systems
    # is initiated using the duplicate-spin-system-button.
    if new_spin_system["operation"] == "duplicate":
        data["spin_systems"] += [spin_system_data]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in spin_system_data["sites"]]
        config["index_last_modified"] = index

        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(data["spin_systems"])
        default[2], default[3], default[4] = data, config, spin_systems_info
        return default

    # Delete an spin-system
    # The following section applies to when a request to remove an spin-systems is
    # initiated using the remove-spin-system-button.
    if new_spin_system["operation"] == "delete":
        if index is None:
            raise PreventUpdate

        # the index to remove is given by spin_system_index
        config["removed"] = [
            site["isotope"] for site in data["spin_systems"][index]["sites"]
        ]
        del data["spin_systems"][index]
        config["index_last_modified"] = index

        info_updates = home_UI.refresh(data)
        default[6] = info_updates
        spin_systems_info = spin_system_UI.refresh(data["spin_systems"])
        default[2], default[3], default[4] = data, config, spin_systems_info
        return default


def example_selection():
    """Load the selected example."""
    decompose = "spin_system" if ctx.inputs["decompose.active"] else "none"
    example = ctx.inputs["selected-example.value"]
    existing_data = ctx.states["local-mrsim-data.data"]
    if example in ["", None]:
        raise PreventUpdate
    return load_from_url(get_absolute_url_path(example, PATH), existing_data, decompose)


def load_from_url(url, existing_data, decompose):
    """Load the selected data from url."""
    response = urlopen(url)

    content = json.loads(response.read())
    if url.endswith(".mrsys"):
        content = {"spin_systems": content}
    # try:
    data = fix_missing_keys(content)
    return assemble_data(parse_data(data))
    # except Exception as e:
    #     no_updates = [no_update] * 7
    #     if_error_occurred = [True, existing_data, *no_updates]
    #     message = f"FileReadError: {e}"
    #     return [message, *if_error_occurred]


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


def parse_contents(contents):
    """Parse contents from the spin-systems file."""
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    data = json.loads(str(decoded, encoding="UTF-8"))
    return data


def parse_data(data):
    """Parse units from the data and return a Simulator dict."""
    return Simulator.parse_dict_with_units(data).reduced_dict()
    # data_keys = data.keys()
    # if parse_spin_system:
    #     if "spin_systems" in data_keys:
    #         try:
    #             a = [
    #                 SpinSystem.parse_dict_with_units(_).dict()
    #                 for _ in data["spin_systems"]
    #             ]
    #         except Exception:
    #             a = [_ for _ in data["spin_systems"]]
    #         data["spin_systems"] = [filter_dict(_) for _ in a]

    # if parse_method:
    #     if "methods" in data_keys:
    #         try:
    #             a = [Method.parse_dict_with_units(_).dict() for _ in data["methods"]]
    #         except Exception:
    #             a = [_ for _ in data["methods"]]
    #         # sim = [_["simulation"] for _ in a]
    #         # exp = [_["experiment"] for _ in a]
    #         data["methods"] = [filter_dict(_) for _ in a]
    # return data


def assemble_data(data):
    config = {"is_new_data": True, "index_last_modified": 0, "length_changed": False}

    # pack = [no_update] * 3
    # if "config" in data.keys():
    #     if data["config"] != {}:
    fields = [
        "integration_density",
        "integration_volume",
        "number_of_sidebands",
        "decompose_spectrum",
    ]
    pack = [data["config"][item] for item in fields]

    # print("pack and input", pack[-1], ctx.inputs["decompose.active"])
    # check1 = pack[-1] == "spin_system" and ctx.inputs["decompose.active"]
    # check2 = pack[-1] == "none" and not ctx.inputs["decompose.active"]
    # check = check1 or check2
    # clicks = ctx.states["decompose.n_clicks"]
    # if clicks is None:
    #     pack[-1] = no_update
    # else:
    #     pack[-1] = no_update if check else clicks + 1
    pack[-1] = no_update
    return [
        "",
        False,
        data,
        config,
        spin_system_UI.refresh(data["spin_systems"]),
        methods_UI.refresh(data["methods"]),
        home_UI.refresh(data),
        *pack,
    ]


def filter_dict(dict1):
    dict_new = {}
    for key, val in dict1.items():
        if key in ["simulation", "property_units"] or val is None:
            continue

        if key == "isotope":
            dict_new[key] = val["symbol"]
            continue

        if key == "channels":
            dict_new[key] = [item["symbol"] for item in val]
            continue

        if key in ["experiment"]:
            dict_new[key] = val
            continue

        dict_new[key] = val
        if isinstance(val, dict):
            dict_new[key] = filter_dict(val)
        if isinstance(val, list):
            dict_new[key] = [filter_dict(_) if isinstance(_, dict) else _ for _ in val]

    return dict_new


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


# # Upload a CSDM compliant NMR data file.
# @app.callback(
#     [
#         Output("alert-message-spectrum", "children"),
#         Output("alert-message-spectrum", "is_open"),
#         Output("local-exp-external-data", "data"),
#     ],
#     [
#         # Input("upload-spectrum-local", "contents"),
#         Input("upload-from-graph", "contents"),
#         # Input("import-measurement-for-method", "contents"),
#     ],
#     [
#         # State("upload-spectrum-local", "filename"),
#         State("upload-from-graph", "filename"),
#         # State("import-measurement-for-method", "filename"),
#         State("local-exp-external-data", "data"),
#     ],
# )
# def update_exp_external_file(*args):
#     """Update a local CSDM file."""

#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     content = ctx.inputs[f"{trigger_id}.contents"]
#     if content is None:
#         raise PreventUpdate

#     states = ctx.states

#     filename = states[f"{trigger_id}.filename"]
#     file_extension = filename.split(".")[1]
#     if file_extension not in ["csdf", "json"]:
#         return [f"Expecting a .csdf file, found .{file_extension}.", True, no_update]
#     if file_extension != "csdf":
#         raise PreventUpdate

#     # if trigger_id == "upload-spectrum-local":
#     #     content_string = csdm_upload_content
#     # if trigger_id == "upload-from-graph":
#     #     content_string = csdm_upload_content_graph

#     content = content.split(",")[1]
#     decoded = base64.b64decode(content)
#     success, data, error_message = load_csdm(decoded)
#     if success:
#         existing_data = states["local-exp-external-data.data"]
#         if existing_data is None:
#             existing_data = {}
#         existing_data["0"] = data.to_dict()
#         return ["", False, existing_data]
#     else:
#         return [f"Invalid JSON file. {error_message}", True, no_update]


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
    "decompose": update_decompose,
    "close_setting": update_sim_config,
    "new-spin-system": modified_spin_system,
    "new-method": modified_method,
    "selected-example": example_selection,
    "url-search": import_from_url,
    "confirm-clear-spin-system": clear_spin_systems,
    "confirm-clear-methods": clear_methods,
    "upload-spin-system-local": import_mrsim_file,
    "open-mrsimulator-file": import_mrsim_file,
    "import-measurement-for-method": import_measurement_for_method,
    "upload-from-graph": import_measurement_for_method,
    "remove-measurement-from-method": remove_measurement_from_method,
}
