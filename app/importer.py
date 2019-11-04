# -*- coding: utf-8 -*-
import base64
import json
import os
import time
from urllib.request import urlopen

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from csdmpy.dependent_variables.download import get_absolute_url_path
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from .app import app
from .custom_widgets import custom_button
from .custom_widgets import label_with_help_button


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# The following are a set of widgets used to load data from file. =====================
# Method 1. From pre-defined set of examples. -----------------------------------------
# Load a list of pre-defined examples from the example_link.json file.
with open("examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)


# populate the list as a dropdown menu.
select_examples_dropdown = [
    html.Div(
        [
            dbc.Label("Select an example isotopomer file.", className="formtext"),
            dcc.Dropdown(
                id="mrsimulator-examples-dropbox",
                options=mrsimulator_examples,
                value=None,
                searchable=False,
                clearable=True,
                placeholder="Select an example ... ",
            ),
        ],
        className="d-flex flex-column p-2",
    ),
    dcc.Store(id="mrsimulator-examples", storage_type="memory"),
]


# This function track the timestamp whenever the above dropdown is triggered.
@app.callback(
    Output("mrsimulator-examples", "data"),
    [Input("mrsimulator-examples-dropbox", "value")],
)
def example_timestamp(value):
    return time.time()


# The example dropdown is wrapped in a collapsible widget. This collapsible widget
# is activate from the navigation menubar.
example_drawer = dbc.Collapse(
    [
        html.Div(
            dbc.Button(
                html.I(className="fas fa-times"),
                id="example-panel-hide-button",
                color="dark",
                size="sm",
            ),
            className="d-flex justify-content-end",
        ),
        html.Div(select_examples_dropdown),
    ],
    className="drawer-card",
    id="example-drawer-collapse",
)

# =====================================================================================


def upload_data(prepend_id, message_for_URL, message_for_upload):
    """User uploaded files.
    Args:
        prepend_id: Prepends to the designated it.
    """
    # Method 2. From URL address ------------------------------------------------------
    data_from_url = [
        label_with_help_button(*message_for_URL, id=f"upload-{prepend_id}-url-help"),
        dbc.InputGroup(
            [
                dbc.Input(
                    type="url",
                    id=f"upload-{prepend_id}-url",
                    value="",
                    placeholder="Paste URL ...",
                    className="form-control",
                ),
                dbc.Button(
                    "Submit",
                    id=f"upload-{prepend_id}-url-submit",
                    className="append-last",
                ),
            ]
        ),
    ]

    # Method 3. From a local file (Drag and drop). ------------------------------------
    # Using the dcc upload method.
    upload_local_file_widget = [
        label_with_help_button(
            *message_for_upload, id=f"upload-{prepend_id}-local-help"
        ),
        dcc.Upload(
            id=f"upload-{prepend_id}-local",
            children=html.Div(
                [
                    "Drag and drop, or ",
                    html.A(
                        [html.I(className="fas fa-upload"), " select"],
                        className="formtext",
                        href="#",
                    ),
                ],
                className="formtext",
            ),
            style={
                "lineHeight": "40px",
                "borderWidth": ".85px",
                "borderStyle": "dashed",
                "borderRadius": "7px",
                "textAlign": "center",
                "color": "silver",
            },
            # Allow multiple files to be uploaded
            multiple=False,
            className="control-upload",
        ),
        dcc.Store(id=f"upload-{prepend_id}-local-timestamp", storage_type="memory"),
    ]

    # This function tracks the timestamp whenever the above upload-a-file method
    # is triggered.
    @app.callback(
        Output(f"upload-{prepend_id}-local-timestamp", "data"),
        [Input(f"upload-{prepend_id}-local", "contents")],
    )
    def upload_isotopomer_timestamp(value):
        return time.time()

    # Layout for the url and upload-a-file input methods. Each input method is wrapped
    # in a collapsible widget which is activated with the following buttons

    # presetting the fields for generating buttons
    fields = [
        {
            "text": "Local",
            "icon": "fas fa-hdd",
            "id": f"upload-{prepend_id}-local-button",
            "tooltip": "Upload a local isotopomers file",
            "active": False,
            "collapsable": upload_local_file_widget,
        },
        {
            "text": "URL",
            "icon": "fas fa-server",
            "id": f"upload-{prepend_id}-url-button",
            "tooltip": "Get isotopomers file from url",
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
                icon=item["icon"],
                id=item["id"],
                tooltip=item["tooltip"],
                active=item["active"],
                style={"borderRadius": 0},
                outline=True,
            )
        )

    # Now wrapping for url and upload-a-file input layouts in a collapsible widget
    input_layout_0 = []
    for item in fields:
        id_ = item["id"]
        input_layout_0.append(dbc.Collapse(item["collapsable"], id=f"{id_}-collapse"))

    # layout for the input panel. The two buttons are packed as vertical button group,
    # followed by the two collapsible widgets.
    input_layout = html.Div(
        [
            html.Div(
                dbc.Button(
                    html.I(className="fas fa-times"),
                    id=f"upload-{prepend_id}-panel-hide-button",
                    color="dark",
                    size="sm",
                ),
                className="d-flex justify-content-end",
            ),
            html.Div(
                [
                    dbc.ButtonGroup(
                        input_buttons, vertical=True, className="button no-round"
                    ),
                    dbc.Col(input_layout_0),
                ],
                className="d-flex justify-content-start",
            ),
        ],
        className="drawer-card",
    )

    @app.callback(
        [
            *[
                Output(fields[j]["id"] + "-collapse", "is_open")
                for j in range(len(fields))
            ],
            *[Output(fields[j]["id"], "active") for j in range(len(fields))],
        ],
        [Input(fields[j]["id"], "n_clicks_timestamp") for j in range(len(fields))],
        [
            *[
                State(fields[j]["id"] + "-collapse", "is_open")
                for j in range(len(fields))
            ],
            *[State(fields[j]["id"], "active") for j in range(len(fields))],
        ],
    )
    def toggle_collapsible_input(n1, n2, c1, c2, a1, a2):
        """Toggle collapsible widget form url and upload-a-file button fields."""
        if n1 == n2 is None:
            return [True, False, True, False]
        max_ = max(i for i in [n1, n2] if i is not None)
        if max_ == n1:
            if not c1:
                return [not c1, False, not a1, False]
            return [c1, False, a1, False]
        if max_ == n2:
            if not c2:
                return [False, not c2, False, not a2]
            return [False, c2, False, a2]

    # The input drawers are further wrapper as a collapsible. This collapsible widget
    # is activate from the navigation menu.
    drawer = dbc.Collapse(input_layout, id=f"upload-{prepend_id}-master-collapse")

    return drawer


isotopomer_import_layout = upload_data(
    prepend_id="isotopomer",
    message_for_URL=["Enter URL of an isotopomers file.", ""],
    message_for_upload=["Upload an isotopomers file.", ""],
)

spectrum_import_layout = upload_data(
    prepend_id="spectrum",
    message_for_URL=[
        "Enter URL of a CSDM compliant NMR data file.",
        "The data should be a NMR spectrum.",
    ],
    message_for_upload=[
        "Upload a CSDM compliant NMR data file.",
        "The data should be a NMR spectrum.",
    ],
)


# method
# Import or update the isotopomers.
@app.callback(
    [
        Output("local-metadata", "data"),
        Output("filename_dataset", "children"),
        Output("data_description", "children"),
        Output("data_citation", "children"),
    ],
    [
        Input("upload-isotopomer-local-timestamp", "modified_timestamp"),
        Input("upload-isotopomer-url-submit", "n_clicks_timestamp"),
        Input("mrsimulator-examples", "modified_timestamp"),
        # Input("json-file-editor", "n_blur_timestamp"),
    ],
    [
        State("upload-isotopomer-local", "contents"),
        State("upload-isotopomer-url", "value"),
        State("upload-isotopomer-local", "filename"),
        State("mrsimulator-examples-dropbox", "value"),
        # State("json-file-editor", "value"),
        State("filename_dataset", "children"),
        State("data_description", "children"),
    ],
)
def update_isotopomers(
    t_upload,
    t_url,
    t_example,
    # time_of_editor_trigger,
    isotopomer_upload_content,
    isotopomer_url,
    isotopomer_filename,
    example_url,
    # editor_value,
    data_title,
    data_info,
):
    """Update the local isotopomers when a new file is imported."""
    print(t_upload, t_url, t_example)  # , t_editor)
    # calculate
    if t_upload is None and t_example is None and t_url is None:  # == t_editor
        print("---prevented isotopomers update---")
        raise PreventUpdate

    # calculate the latest trigger from timestamps
    max_ = max(i for i in [t_upload, t_url, t_example] if i is not None)
    print(max_)

    # The following section applies to when the isotopomers update is triggered from
    # set of pre-defined examples.
    if max_ == t_example:
        path = os.path.split(__file__)[0]
        if example_url in ["", None]:
            print("---prevented isotopomers update---")
            raise PreventUpdate
        response = urlopen(get_absolute_url_path(example_url, path))
        data = json.loads(response.read())
        return [data, data["name"], data["description"], data["citation"]]

    if max_ == t_url:
        if isotopomer_url in ["", None]:
            print("---prevented isotopomers update---")
            raise PreventUpdate
        response = urlopen(isotopomer_url)
        data = json.loads(response.read())
        return [data, data["name"], data["description"], data["citation"]]

    # The following section applies to when the isotopomers update is triggered from
    # a user uploaded file.
    if max_ == t_upload:
        if isotopomer_upload_content is None:
            print("---prevented isotopomers update---")
            raise PreventUpdate
        data = parse_contents(isotopomer_upload_content, isotopomer_filename)

    # The following section applies to when the isotopomers update is triggered when
    # user edits the loaded isotopomer file.
    # if max_ == time_of_editor_trigger:
    #     if editor_value in ["", None]:
    #         print("---prevented isotopomers update---")
    #         raise PreventUpdate
    #     data = {}
    #     data["name"] = data_title
    #     data["description"] = data_info
    #     data["isotopomers"] = json.loads(editor_value)

    print("---update isotopomers---")
    return [data, data["name"], data["description"], data["citation"]]


def parse_contents(contents, filename):
    """Parse contents from the isotopomers file."""
    default_data = {"isotopomers": [], "name": "", "description": "", "citation": ""}
    if filename is None:
        return default_data
    try:
        if "json" in filename:
            content_string = contents.split(",")[1]
            decoded = base64.b64decode(content_string)
            data = json.loads(str(decoded, encoding="UTF-8"))

            if "name" not in data.keys():
                data["name"] = filename

            if "description" not in data.keys():
                data["description"] = ""

            if "citation" not in data.keys():
                data["citation"] = ""

            return data

        else:
            return default_data

    except Exception:
        return default_data


# Upload a CSDM compliant NMR data file.
@app.callback(
    Output("local-csdm-data", "data"),
    [Input("upload-spectrum-local-timestamp", "modified_timestamp")],
    [
        State("upload-spectrum-local", "contents"),
        State("upload-spectrum-local", "filename"),
    ],
)
def update_csdm_file(time_of_upload_trigger, csdm_upload_content, csdm_filename):
    """Update a local CSDM file."""
    if csdm_upload_content is None:
        print("---prevented spectrum update---")
        raise PreventUpdate

    content_string = csdm_upload_content.split(",")[1]
    decoded = base64.b64decode(content_string)
    data = json.loads(str(decoded, encoding="UTF-8"))
    # data = cp.parse_dict(data)
    # for datum in data.dependent_variables:
    #     datum.components = datum.components/datum.components.max().
    print("---update spectrum---")
    return data
