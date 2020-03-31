# -*- coding: utf-8 -*-
import base64
import json
import os
from urllib.request import urlopen

import csdmpy as cp
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from csdmpy.dependent_variables.download import get_absolute_url_path
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Isotopomer

from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import label_with_help_button
from app.isotopomer.draft import get_all_isotopomer_dropdown_options

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# The following are a set of widgets used to load data from file. =====================
# Method 1. From pre-defined set of examples. -----------------------------------------
# Load a list of pre-defined examples from the example_link.json file.
with open("examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)


# =====================================================================================


def upload_data(prepend_id, message_for_URL, message_for_upload):
    """User uploaded files.
    Args:
        prepend_id: Prepends to the designated it.
    """

    if prepend_id == "isotopomer":
        options = mrsimulator_examples
    else:
        options = []

    # Method 1: A dropdown menu list with example isotopomers.
    # -------------------------------------------------------------------------
    select_examples_dropdown = html.Div(
        [
            dbc.Label(f"Select an example {prepend_id}.", className="formtext"),
            dcc.Dropdown(
                id=f"example-{prepend_id}-dropbox",
                options=options,
                searchable=False,
                clearable=True,
                placeholder="Select an example ... ",
                style={"zIndex": "10"},
            ),
        ],
        className="d-flex flex-column grow",
    )

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

    # Method 3. From a local file (Drag and drop). ------------------------------------
    # Using the dcc upload method.
    upload_local_file_widget = html.Div(
        [
            label_with_help_button(
                *message_for_upload, id=f"upload-{prepend_id}-local-help"
            ),
            dcc.Upload(
                id=f"upload-{prepend_id}-local",
                children=html.Div(
                    [
                        "Drag and drop, or ",
                        html.A(
                            [html.I(className="fas fa-upload"), " select"], href="#"
                        ),
                    ],
                    className="formtext",
                ),
                style={
                    "lineHeight": "55px",
                    "borderWidth": ".85px",
                    "borderStyle": "dashed",
                    "borderRadius": "7px",
                    "textAlign": "center",
                    "color": "silver",
                },
                # Allow multiple files to be uploaded
                multiple=False,
            ),
        ],
        className="d-flex flex-column pb-1",
    )

    # Layout for the url and upload-a-file input methods. Each input method is wrapped
    # in a collapsible widget which is activated with the following buttons

    # presetting the fields for generating buttons
    fields = [
        {
            "text": "Example",
            "icon_classname": "fac fa-isotopomers",
            "id": f"example-{prepend_id}-button",
            "tooltip": "Select an example.",
            "active": False,
            "collapsable": select_examples_dropdown,
        },
        {
            "text": "Local",
            "icon_classname": "fas fa-hdd",
            "id": f"upload-{prepend_id}-local-button",
            "tooltip": "Upload a local JSON file containing isotopomers.",
            "active": False,
            "collapsable": upload_local_file_widget,
        },
        {
            "text": "URL",
            "icon_classname": "fas fa-at",
            "id": f"upload-{prepend_id}-url-button",
            "tooltip": "Retrieve isotopomers from a remote JSON file.",
            "active": False,
            "collapsable": data_from_url,
        },
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

    # layout for the input panel. The two buttons are packed as vertical button group,
    # followed by the two collapsible widgets.
    # if prepend_id == "isotopomer":
    #     addon = [select_examples_dropdown]
    # else:
    #     addon = []
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

    @app.callback(
        [
            *[
                Output(fields[j]["id"] + "-collapse", "is_open")
                for j in range(len(fields))
            ],
            *[Output(fields[j]["id"], "active") for j in range(len(fields))],
        ],
        [Input(fields[j]["id"], "n_clicks") for j in range(len(fields))],
        [
            *[
                State(fields[j]["id"] + "-collapse", "is_open")
                for j in range(len(fields))
            ],
            *[State(fields[j]["id"], "active") for j in range(len(fields))],
        ],
    )
    def toggle_collapsible_input(n1, n2, n3, c1, c2, c3, a1, a2, a3):
        """Toggle collapsible widget form url and upload-a-file button fields."""
        if n1 is n2 is n3 is None:
            return [False, True, False, False, True, False]

        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == fields[0]["id"]:
            if not c1:
                return [not c1, False, False, not a1, False, False]
            return [c1, False, False, a1, False, False]
        if button_id == fields[1]["id"]:
            if not c2:
                return [False, not c2, False, False, not a2, False]
            return [False, c2, False, False, a2, False]
        if button_id == fields[2]["id"]:
            if not c3:
                return [False, False, not c3, False, False, not a3]
            return [False, False, c3, False, False, a3]

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
        Output("filename_dataset", "children"),
        Output("data_description", "children"),
        Output("local-isotopomers-data", "data"),
        Output("config", "data"),
        Output("isotope_id-0", "options"),
        Output("isotope_id-0", "value"),
        Output("isotopomer-dropdown", "options"),
        Output("isotopomer-read-only", "children"),
    ],
    [
        Input("upload-isotopomer-local", "contents"),
        Input("upload-isotopomer-url-submit", "n_clicks"),
        Input("example-isotopomer-dropbox", "value"),
        Input("upload-from-graph", "contents"),
        Input("json-file-editor", "n_blur_timestamp"),
        Input("new-json", "modified_timestamp"),
        Input("add-isotopomer-button", "n_clicks"),
        Input("duplicate-isotopomer-button", "n_clicks"),
        Input("trash-isotopomer-button", "n_clicks"),
    ],
    [
        State("upload-isotopomer-url", "value"),
        State("upload-isotopomer-local", "filename"),
        State("json-file-editor", "value"),
        State("local-isotopomers-data", "data"),
        State("filename_dataset", "children"),
        State("data_description", "children"),
        State("upload-from-graph", "filename"),
        State("local-isotopomer-index-map", "data"),
        State("isotopomer-dropdown", "value"),
        State("new-json", "data"),
        State("isotope_id-0", "value"),
    ],
)
def update_isotopomers(
    isotopomer_upload_content,
    n_click,
    example,
    from_graph_content,
    time_of_editor_trigger,
    time_of_new_json_data_trigger,
    new_isotopomer_button,
    duplicate_isotopomer_button,
    trash_isotopomer_button,
    # states
    isotopomer_url,
    isotopomer_filename,
    editor_value,
    existing_isotopomers_data,
    data_title,
    data_info,
    from_graph_filename,
    index_map,
    isotopomer_dropdown_value,
    new_json_data,
    old_isotope,
):
    """Update the local isotopomers when a new file is imported."""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("trigger", trigger_id)

    # the following config is true for all cases when isotopomer data is modified
    # using the app.
    config = {"is_new_data": False, "length_changed": False}
    no_updates = [no_update, no_update, no_update, no_update]

    # Modify isotopomer
    # The following section applies to when the isotopomers update is triggered from
    # the GUI fields. This is a very common trigger, so we place it at the start.
    if trigger_id == "new-json":
        if new_json_data in ["", None]:
            raise PreventUpdate
        if existing_isotopomers_data is None:
            raise PreventUpdate
        data = existing_isotopomers_data
        data["isotopomers"][isotopomer_dropdown_value] = new_json_data
        config["index_last_modified"] = isotopomer_dropdown_value
        dropdown_options = update_dropdown_options(data, old_isotope, config)
        return [*no_updates, data, config, *dropdown_options]

    # Add a new isotopomer
    # The following section applies to when the a new isotopomers is added from
    # add-isotopomer-button.
    if trigger_id == "add-isotopomer-button":
        data_len = (
            len(existing_isotopomers_data["isotopomers"])
            if existing_isotopomers_data is not None
            else 0
        )
        new_isotopomer = {
            "name": f"Isotopomer-{data_len}",
            "description": "Add description ...",
            "abundance": 1,
            "sites": [{"isotope": "1H", "isotropic_chemical_shift": 0}],
        }
        data = (
            existing_isotopomers_data
            if existing_isotopomers_data is not None
            else {"name": "", "description": "", "isotopomers": []}
        )
        data["isotopomers"] += [new_isotopomer]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in new_isotopomer["sites"]]
        config["index_last_modified"] = data_len
        dropdown_options = update_dropdown_options(data, old_isotope, config)
        return [*no_updates, data, config, *dropdown_options]

    # Copy an existing isotopomer
    # The following section applies to when a request to duplicate the isotopomers is
    # initiated using the duplicate-isotopomer-button.
    if trigger_id == "duplicate-isotopomer-button":
        if existing_isotopomers_data is None:
            raise PreventUpdate
        data = existing_isotopomers_data
        # the index to copy is given by isotopomer_dropdown_value
        isotopomer_to_copy = data["isotopomers"][isotopomer_dropdown_value].copy()
        data["isotopomers"] += [isotopomer_to_copy]
        config["length_changed"] = True
        config["added"] = [site["isotope"] for site in isotopomer_to_copy["sites"]]
        config["index_last_modified"] = len(data["isotopomers"]) - 1
        dropdown_options = update_dropdown_options(data, old_isotope, config)
        return [*no_updates, data, config, *dropdown_options]

    # Delete an isotopomer
    # The following section applies to when a request to remove an isotopomers is
    # initiated using the trash-isotopomer-button.
    if trigger_id == "trash-isotopomer-button":
        if isotopomer_dropdown_value is None:
            raise PreventUpdate
        if existing_isotopomers_data is None:
            raise PreventUpdate
        data = existing_isotopomers_data
        # the index to remove is given by isotopomer_dropdown_value
        config["removed"] = [
            site["isotope"]
            for site in data["isotopomers"][isotopomer_dropdown_value]["sites"]
        ]

        del data["isotopomers"][isotopomer_dropdown_value]
        new_length = len(data["isotopomers"]) - 1
        config["length_changed"] = True
        index = (
            isotopomer_dropdown_value
            if isotopomer_dropdown_value < new_length
            else new_length
        )
        index = None if new_length < 0 else index

        config["index_last_modified"] = index
        dropdown_options = update_dropdown_options(data, old_isotope, config)
        return [*no_updates, data, config, *dropdown_options]

    # Modify isotopomer directly from json input
    # The following section applies to when the isotopomers update is triggered when
    # user edits the loaded isotopomer file.
    if trigger_id == "json-file-editor":
        if editor_value in ["", None]:
            raise PreventUpdate
        if existing_isotopomers_data is None:
            raise PreventUpdate
        isotopomers = json.loads(editor_value)
        data = existing_isotopomers_data
        data["isotopomers"][isotopomer_dropdown_value] = isotopomers
        config["index_last_modified"] = isotopomer_dropdown_value
        dropdown_options = update_dropdown_options(data, old_isotope, config)
        return [*no_updates, data, config, *dropdown_options]

    if_error_occurred = [
        True,
        no_update,
        no_update,
        existing_isotopomers_data,
        *no_updates,
    ]

    # Load a sample from pre-defined examples
    # The following section applies to when the isotopomers update is triggered from
    # set of pre-defined examples.
    if trigger_id == "example-isotopomer-dropbox":
        path = os.path.split(__file__)[0]
        if example in ["", None]:
            raise PreventUpdate
        response = urlopen(get_absolute_url_path(example, path))
        data = json.loads(response.read())
        return assemble_data(data, old_isotope)

    # Request and load a sample from URL
    # The following section applies to when the isotopomers update is triggered from
    # url-submit.
    if trigger_id == "upload-isotopomer-url-submit":
        if isotopomer_url in ["", None]:
            raise PreventUpdate
        response = urlopen(isotopomer_url)
        try:
            data = json.loads(response.read())
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]
        return assemble_data(data, old_isotope)

    # Load a sample from drag and drop
    # The following section applies to when the isotopomers update is triggered from
    # a user uploaded file.
    if trigger_id == "upload-isotopomer-local":
        if isotopomer_upload_content is None:
            raise PreventUpdate
        try:
            data = parse_contents(isotopomer_upload_content, isotopomer_filename)
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]
        return assemble_data(data, old_isotope)

    # Load a sample from drag and drop on the graph reqion
    # The following section applies to when the isotopomers update is triggered from
    # a user drag and drop on the graph.
    if trigger_id == "upload-from-graph":
        if from_graph_content is None:
            raise PreventUpdate
        if from_graph_filename.split(".")[1] != "json":
            raise PreventUpdate
        try:
            data = parse_contents(from_graph_content, from_graph_filename)
        except Exception:
            message = "Error reading isotopomers."
            return [message, *if_error_occurred]

        return assemble_data(data, old_isotope)


def filter_dict(dict1):
    dict_new = {}
    for key, val in dict1.items():
        # print(key, val)
        if val is not None:
            dict_new[key] = val
        if isinstance(val, dict):
            dict_new[key] = filter_dict(val)
        if isinstance(val, list):
            dict_new[key] = [filter_dict(item) for item in val]
        if key == "property_units":
            dict_new.pop("property_units")
    return dict_new


def assemble_data(data, old_isotope):
    a = [Isotopomer.parse_dict_with_units(item).dict() for item in data["isotopomers"]]
    data["isotopomers"] = [filter_dict(item) for item in a]

    if "name" not in data:
        data["name"] = ""
    if "description" not in data:
        data["description"] = ""

    config = {"is_new_data": True, "index_last_modified": 0, "length_changed": False}

    dropdown_options = update_dropdown_options(data, old_isotope, config)
    return [
        "",
        False,
        data["name"],
        data["description"],
        data,
        config,
        *dropdown_options,
    ]


def parse_contents(contents, filename):
    """Parse contents from the isotopomers file."""
    default_data = {
        "isotopomers": [],
        "name": "",
        "description": "",
    }  # , "citation": ""}
    if filename is None:
        return default_data
    # try:
    if "json" in filename:
        content_string = contents.split(",")[1]
        decoded = base64.b64decode(content_string)
        data = json.loads(str(decoded, encoding="UTF-8"))

        if "name" not in data.keys():
            data["name"] = filename

        if "description" not in data.keys():
            data["description"] = "Add a description ... "

        return data

    else:
        raise Exception("File not recognized.")

    # except Exception:
    #     return default_data


def update_dropdown_options(local_isotopomer_data, old_isotope, config):
    if local_isotopomer_data is None:
        raise PreventUpdate
    if local_isotopomer_data["isotopomers"] == []:
        return [[], None, [], "inactive"]

    # extracting a list of unique isotopes from the list of isotopes
    isotopes = set(
        [
            site["isotope"]
            for item in local_isotopomer_data["isotopomers"]
            for site in item["sites"]
        ]
    )
    # Output isotope_id-0 -> options
    # set up a list of options for the isotope dropdown menu
    isotope_dropdown_options = [
        {"label": site_iso, "value": site_iso} for site_iso in isotopes
    ]

    # Output isotope_id-0 -> value
    # select an isotope from the list of options. If the previously selected isotope
    # is in the new option list, use the previous isotope, else select the isotope at
    # index zero of the options list.
    isotope = (
        old_isotope if old_isotope in isotopes else isotope_dropdown_options[0]["value"]
    )

    # Output isotopomer-dropdown -> options
    # Update isotopomer dropdown options base on local isotopomers data
    isotopomer_dropdown_options = get_all_isotopomer_dropdown_options(
        local_isotopomer_data["isotopomers"]
    )

    return [
        isotope_dropdown_options,
        isotope,
        isotopomer_dropdown_options,
        json.dumps(local_isotopomer_data, indent=2),
    ]


# Upload a CSDM compliant NMR data file.
@app.callback(
    [
        Output("alert-message-spectrum", "children"),
        Output("alert-message-spectrum", "is_open"),
        Output("local-exp-external-data", "data"),
    ],
    [
        Input("upload-spectrum-local", "contents"),
        Input("upload-from-graph", "contents"),
    ],
    [
        State("upload-spectrum-local", "filename"),
        State("upload-from-graph", "filename"),
    ],
)
def update_exp_external_file(csdm_upload_content, csdm_upload_content_graph, *args):
    """Update a local CSDM file."""
    ctx = dash.callback_context
    if csdm_upload_content is None and csdm_upload_content_graph is None:
        raise PreventUpdate

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    states = dash.callback_context.states

    filename = states[f"{trigger_id}.filename"]
    file_extension = filename.split(".")[1]
    if file_extension not in ["csdf", "json"]:
        return [f"Expecting a .csdf file, found .{file_extension}.", True, no_update]
    if file_extension != "csdf":
        raise PreventUpdate

    if trigger_id == "upload-spectrum-local":
        content_string = csdm_upload_content
    if trigger_id == "upload-from-graph":
        content_string = csdm_upload_content_graph

    content_string = content_string.split(",")[1]
    decoded = base64.b64decode(content_string)
    success, data, error_message = load_json(decoded)
    if success:
        return ["", False, data]
    else:
        return [f"Invalid JSON file. {error_message}", True, no_update]


def load_json(content):
    """Load a JSON file. Return a list with members
        - Success: True if file is read correctly,
        - Data: File content is success, otherwise an empty string,
        - message: An error message when JSON file load fails, else an empty string.
    """
    content = str(content, encoding="UTF-8")
    try:
        data = cp.loads(content).to_dict()
        return True, data, ""
    except Exception as e:
        return False, "", e
