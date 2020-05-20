# -*- coding: utf-8 -*-
import base64
import json
import os
from urllib.request import urlopen

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_html_components as html
from csdmpy.dependent_variables.download import get_absolute_url_path
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Isotopomer
from mrsimulator import Method

from .app import app
from .custom_widgets import custom_button
from .custom_widgets import label_with_help_button
from .dimension.util import update_method_info
from .info import update_sample_info
from .isotopomer.util import update_isotopomer_info

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


def upload_data(prepend_id, message_for_URL, message_for_upload):
    """User uploaded files.
    Args:
        prepend_id: Prepends to the designated it.
    """

    # Method 2. From URL address
    # -------------------------------------------------------------------------
    data_from_url = html.Div(
        [
            label_with_help_button(
                *message_for_URL, id=f"upload-{prepend_id}-url-help"
            ),
            dbc.InputGroup(
                [
                    dbc.Input(
                        type="url",
                        id=f"upload-{prepend_id}-url",
                        value="",
                        placeholder="Paste URL ...",
                    ),
                    dbc.Button(
                        "Submit",
                        id=f"upload-{prepend_id}-url-submit",
                        className="append-last",
                    ),
                ]
            ),
        ],
        className="d-flex flex-column",
    )

    # presetting the fields for generating buttons
    fields = [
        {
            "text": "URL",
            "icon_classname": "fas fa-at",
            "id": f"upload-{prepend_id}-url-button",
            "tooltip": "Retrieve isotopomers from a remote JSON file.",
            "active": False,
            "collapsable": data_from_url,
        }
    ]

    # Now generating buttons
    input_buttons = []
    for item in fields:
        input_buttons.append(
            custom_button(
                text=item["text"],
                icon_classname=item["icon_classname"],
                id=item["id"],
                tooltip=item["tooltip"],
                active=item["active"],
                outline=True,
                color="light",
            )
        )

    # Now wrapping from-url and upload-a-file input layouts in a collapsible widget
    input_layout_0 = []
    for item in fields:
        id_ = item["id"]
        input_layout_0.append(dbc.Collapse(item["collapsable"], id=f"{id_}-collapse"))

    input_layout = html.Div(
        [
            html.Div(
                dbc.Button(
                    html.I(className="fas fa-times"),
                    id=f"upload-{prepend_id}-panel-hide-button",
                    # color="dark",
                    size="sm",
                    style={"backgroundColor": "transparent", "outline": "none"},
                ),
                className="d-flex justify-content-end",
            ),
            # *addon,
            html.Div(
                [
                    dbc.ButtonGroup(input_buttons, vertical=True, className="button"),
                    dbc.Col(input_layout_0),
                ],
                className="d-flex justify-content-start",
            ),
        ],
        className="navbar-reveal",
    )

    # The input drawers are further wrapper as a collapsible. This collapsible widget
    # is activate from the navigation menu.
    drawer = dbc.Collapse(input_layout, id=f"upload-{prepend_id}-master-collapse")

    return drawer


isotopomer_import_layout = upload_data(
    prepend_id="isotopomer",
    message_for_URL=[
        "Enter URL of a JSON file contaiing isotopomers.",
        (
            "Isotopomers file is a collection of sites and couplings ",
            "used in simulating NMR linshapes.",
        ),
    ],
    message_for_upload=[
        "Upload a JSON file containing isotopomers.",
        (
            "Isotopomers file is a collection of sites and couplings ",
            "used in simulating NMR linshapes.",
        ),
    ],
)

spectrum_import_layout = upload_data(
    prepend_id="spectrum",
    message_for_URL=[
        "Enter URL of a CSDM compliant NMR data file.",
        "Add an NMR spectrum to compare with the simulation.",
    ],
    message_for_upload=[
        "Upload a CSDM compliant NMR data file.",
        "Add an NMR spectrum to compare with the simulation.",
    ],
)


# method
# Import or update the isotopomers.
@app.callback(
    [
        Output("alert-message-isotopomer", "children"),
        Output("alert-message-isotopomer", "is_open"),
        Output("local-isotopomers-data", "data"),
        Output("config", "data"),
        Output("isotopomer-read-only", "children"),
        Output("method-read-only", "children"),
        Output("info-read-only", "children"),
    ],
    [
        Input("upload-isotopomer-local", "contents"),  # drag and drop
        Input("open-mrsimulator-file", "contents"),  # from file->open
        Input("upload-and-add-isotopomer-button", "contents"),  # isotopomer->import+add
        Input("import-measurement-for-method", "contents"),  # method->add measurement
        Input("upload-from-graph", "contents"),  # graph->drag and drop
        Input("upload-isotopomer-url-submit", "n_clicks"),
        Input("selected-example", "value"),  # examples
        Input("new-json", "modified_timestamp"),  # when isotopomer change
        Input("new-method-json", "modified_timestamp"),  # when method change
        Input("confirm-clear-isotopomer", "submit_n_clicks"),  # isotopomer->clear
        Input("confirm-clear-methods", "submit_n_clicks"),  # method->clear
    ],
    [
        State("upload-isotopomer-url", "value"),
        State("local-isotopomers-data", "data"),
        State("new-json", "data"),
        State("new-method-json", "data"),
        State("select-method", "value"),
    ],
    prevent_initial_call=True,
)
def update_isotopomers(*args):
    """Update the local isotopomers when a new file is imported."""
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("trigger", trigger_id)

    existing_data = ctx.states["local-isotopomers-data.data"]

    if trigger_id == "new-json":
        new_json_data = ctx.states["new-json.data"]
        return modified_isotopomer(existing_data, new_json_data)

    if trigger_id == "new-method-json":
        new_method_data = ctx.states["new-method-json.data"]
        return modified_method(existing_data, new_method_data)

    # old_isotope = ctx.states["isotope_id-0.value"]
    no_updates = [no_update, no_update, no_update]
    if_error_occurred = [True, existing_data, *no_updates]

    # Load a sample from pre-defined examples
    # The following section applies to when the isotopomers update is triggered from
    # set of pre-defined examples.
    if trigger_id == "selected-example":
        example = ctx.inputs["selected-example.value"]
        path = os.path.split(__file__)[0]
        if example in ["", None]:
            raise PreventUpdate
        response = urlopen(get_absolute_url_path(example, path))
        data = fix_missing_keys(json.loads(response.read()))
        return assemble_data(parse_data(data))

    # Request and load a sample from URL
    # The following section applies to when the isotopomers update is triggered from
    # url-submit.
    if trigger_id == "upload-isotopomer-url-submit":
        url = ctx.states("upload-isotopomer-url.value")
        if url in ["", None]:
            raise PreventUpdate
        response = urlopen(url)
        try:
            data = fix_missing_keys(json.loads(response.read()))
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]
        return assemble_data(parse_data(data))

    if trigger_id == "confirm-clear-isotopomer":
        if existing_data is None:
            raise PreventUpdate
        existing_data["isotopomers"] = []
        return assemble_data(existing_data)

    if trigger_id == "confirm-clear-methods":
        if existing_data is None:
            raise PreventUpdate
        existing_data["methods"] = []
        return assemble_data(existing_data)

    if trigger_id == "upload-and-add-isotopomer-button":
        contents = ctx.inputs[f"{trigger_id}.contents"]
        if contents is None:
            raise PreventUpdate
        try:
            data = fix_missing_keys(parse_contents(contents))
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]
        data = parse_data(data, parse_method=False)
        existing_data["isotopomers"] += data["isotopomers"]
        return assemble_data(existing_data)

    # Load a sample from drag and drop
    # The following section applies to when the isotopomers update is triggered from
    # a user uploaded file.
    if trigger_id in ["upload-isotopomer-local", "open-mrsimulator-file"]:
        contents = ctx.inputs[f"{trigger_id}.contents"]
        if contents is None:
            raise PreventUpdate
        try:
            data = fix_missing_keys(parse_contents(contents))
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]
        return assemble_data(parse_data(data))

    if trigger_id in ["import-measurement-for-method", "upload-from-graph"]:
        contents = ctx.inputs[f"{trigger_id}.contents"]
        content_string = contents.split(",")[1]
        decoded = base64.b64decode(content_string)
        success, exp_data, error_message = load_csdm(decoded)

        if not success:
            return [
                f"Error reading file. {error_message}",
                True,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            ]

        index = ctx.states["select-method.value"]
        method = existing_data["methods"][index]
        method["experiment"] = exp_data.to_dict()
        spectral_dim = method["spectral_dimensions"]
        for i, dim in enumerate(exp_data.dimensions):
            spectral_dim[i]["count"] = dim.count
            spectral_dim[i]["spectral_width"] = dim.count * dim.increment.to("Hz").value
            spectral_dim[i]["reference_offset"] = dim.coordinates_offset.to("Hz").value
            spectral_dim[i]["origin_offset"] = dim.origin_offset.to("Hz").value

        methods_info = update_method_info(existing_data["methods"])
        return ["", False, existing_data, no_update, no_update, methods_info, no_update]

    # Load a sample from drag and drop on the graph reqion
    # The following section applies to when the isotopomers update is triggered from
    # a user drag and drop on the graph.
    # if trigger_id == "upload-from-graph":
    #     if from_graph_content is None:
    #         raise PreventUpdate
    #     if from_graph_filename.split(".")[1] != "json":
    #         raise PreventUpdate
    #     try:
    #         data = parse_contents(from_graph_content, from_graph_filename)
    #     except Exception:
    #         message = "Error reading isotopomers."
    #         return [message, *if_error_occurred]

    #     return assemble_data(data)


def modified_method(existing_method_data, new_method_data):

    default = [no_update for _ in range(7)]
    if new_method_data is None:
        raise PreventUpdate

    index = new_method_data["index"]
    data = (
        existing_method_data
        if existing_method_data is not None
        else {"name": "", "description": "", "isotopomers": [], "methods": []}
    )
    method_data = new_method_data["data"]

    # Add a new method
    if new_method_data["operation"] == "add":
        data["methods"] += [method_data]
        methods_info = update_method_info(data["methods"])
        default[2], default[5] = data, methods_info
        return default

    # Modify a method
    if new_method_data["operation"] == "modify":
        if "experiment" in data["methods"][index]:
            method_data["experiment"] = data["methods"][index]["experiment"]
        data["methods"][index] = method_data
        methods_info = update_method_info(data["methods"])
        default[2], default[5] = data, methods_info
        return default

    # Duplicate a method
    if new_method_data["operation"] == "duplicate":
        data["methods"] += [method_data]
        methods_info = update_method_info(data["methods"])
        default[2], default[5] = data, methods_info
        return default

    # Delete a method
    if new_method_data["operation"] == "delete":
        if index is None:
            raise PreventUpdate
        del data["methods"][index]
        methods_info = update_method_info(data["methods"])
        default[2], default[5] = data, methods_info
        return default


def modified_isotopomer(existing_data, new_json_data):
    """Update the local isotopomer data when an update is triggered."""
    config = {"is_new_data": False, "length_changed": False}
    default = [no_update for _ in range(7)]

    if new_json_data is None:
        raise PreventUpdate
    index = new_json_data["index"]
    data = (
        existing_data
        if existing_data is not None
        else {"name": "", "description": "", "isotopomers": [], "methods": []}
    )
    isotopomer_data = new_json_data["data"]
    # Modify isotopomer
    # The following section applies to when the isotopomers update is triggered from
    # the GUI fields. This is a very common trigger, so we place it at the start.
    if new_json_data["operation"] == "modify":
        data["isotopomers"][index] = isotopomer_data
        config["index_last_modified"] = index

        isotopomers_info = update_isotopomer_info(data["isotopomers"])
        default[2], default[3], default[4] = data, config, isotopomers_info
        return default

    # Add a new isotopomer
    # The following section applies to when the a new isotopomers is added from
    # add-isotopomer-button.
    if new_json_data["operation"] == "add":
        data["isotopomers"] += [isotopomer_data]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in isotopomer_data["sites"]]
        config["index_last_modified"] = index

        isotopomers_info = update_isotopomer_info(data["isotopomers"])
        default[2], default[3], default[4] = data, config, isotopomers_info
        return default

    # Copy an existing isotopomer
    # The following section applies to when a request to duplicate the isotopomers
    # is initiated using the duplicate-isotopomer-button.
    if new_json_data["operation"] == "duplicate":
        data["isotopomers"] += [isotopomer_data]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in isotopomer_data["sites"]]
        config["index_last_modified"] = index

        isotopomers_info = update_isotopomer_info(data["isotopomers"])
        default[2], default[3], default[4] = data, config, isotopomers_info
        return default

    # Delete an isotopomer
    # The following section applies to when a request to remove an isotopomers is
    # initiated using the remove-isotopomer-button.
    if new_json_data["operation"] == "delete":
        if index is None:
            raise PreventUpdate

        # the index to remove is given by isotopomer_index
        config["removed"] = [
            site["isotope"] for site in data["isotopomers"][index]["sites"]
        ]
        del data["isotopomers"][index]
        config["index_last_modified"] = index

        isotopomers_info = update_isotopomer_info(data["isotopomers"])
        default[2], default[3], default[4] = data, config, isotopomers_info
        return default


def fix_missing_keys(json_data):
    default_data = {
        "name": "",
        "description": "Add a description ...",
        "isotopomers": [],
        "methods": [],
        "config": {},
    }
    data_keys = json_data.keys()
    for k in default_data.keys():
        if k not in data_keys:
            json_data[k] = default_data[k]
    return json_data


def parse_contents(contents):
    """Parse contents from the isotopomers file."""
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    data = json.loads(str(decoded, encoding="UTF-8"))
    return data


def parse_data(data, parse_method=True, parse_isotopomer=True):
    data_keys = data.keys()
    if parse_isotopomer:
        if "isotopomers" in data_keys:
            a = [
                Isotopomer.parse_dict_with_units(_).dict() for _ in data["isotopomers"]
            ]
            data["isotopomers"] = [filter_dict(_) for _ in a]

    if parse_method:
        if "methods" in data_keys:
            a = [Method.parse_dict_with_units(_).dict() for _ in data["methods"]]
            # sim = [_["simulation"] for _ in a]
            # exp = [_["experiment"] for _ in a]
            data["methods"] = [filter_dict(_) for _ in a]
    return data


def assemble_data(data):
    config = {"is_new_data": True, "index_last_modified": 0, "length_changed": False}
    return [
        "",
        False,
        data,
        config,
        update_isotopomer_info(data["isotopomers"]),
        update_method_info(data["methods"]),
        update_sample_info(data),
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


# @app.callback(
#     [Output("isotope_id-0", "options"), Output("isotope_id-0", "value")],
#     [Input("local-isotopomers-data", "modified_timestamp")],
#     [State("local-isotopomers-data", "data"), State("isotope_id-0", "value")],
# )
# def update_dropdown_options(t, local_isotopomer_data, old_isotope):
#     print("update_dropdown_options", old_isotope)
#     if local_isotopomer_data is None:
#         raise PreventUpdate
#     if local_isotopomer_data["isotopomers"] == []:
#         return [[], None]

#     # extracting a list of unique isotopes from the list of isotopes
#     isotopes = set(
#         [
#             site["isotope"]
#             for item in local_isotopomer_data["isotopomers"]
#             for site in item["sites"]
#         ]
#     )
#     # Output isotope_id-0 -> options
#     # set up a list of options for the isotope dropdown menu
#     isotope_dropdown_options = [
#         {"label": site_iso, "value": site_iso} for site_iso in isotopes
#     ]

#     # Output isotope_id-0 -> value
#     # select an isotope from the list of options. If the previously selected isotope
#     # is in the new option list, use the previous isotope, else select the isotope at
#     # index zero of the options list.
#     isotope = (
#         old_isotope if old_isotope in isotopes else isotope_dropdown_options[0]
#               ["value"]
#     )

#     print(local_isotopomer_data["isotopomers"])
#     # Output isotopomer-dropdown -> options
#     # Update isotopomer dropdown options base on local isotopomers data
#     # isotopomer_dropdown_options = get_all_isotopomer_dropdown_options(
#     #     local_isotopomer_data["isotopomers"]
#     # )

#     return [
#         isotope_dropdown_options,
#         isotope,
#         # print_info(local_isotopomer_data),
#     ]


# convert client-side function
@app.callback(
    Output("select-method", "options"),
    [Input("local-isotopomers-data", "data")],
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
