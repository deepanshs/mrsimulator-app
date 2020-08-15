# -*- coding: utf-8 -*-
import json

import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from .app import app
from .modal.about import about_modals
from .modal.advance_settings import advance_settings
from .modal.download import download_modal
from app.app import year


className = "d-flex align-items-center justify-items-center"


def div_icon_text_display(icon, text, id=None):
    if id is not None:
        return html.Div(
            [html.I(className=icon), html.Div(text, className="pl-2")],
            className=className,
            id=id,
        )
    return html.Div(
        [html.I(className=icon), html.Div(text, className="pl-2")], className=className
    )


def label_icon_text_display(icon, text, id=None):
    if id is not None:
        return html.Label(
            [html.I(className=icon), html.Div(text, className="pl-2")],
            className=className,
            id=id,
        )
    return html.Label(
        [html.I(className=icon), html.Div(text, className="pl-2")], className=className
    )


# Advanced settings ----------------------------------------------------------------- #
advance_setting_button = html.Div(
    label_icon_text_display(icon="fas fa-cog", text="Setting", id="advance_setting"),
    className="default-button",
)

# File menu ----------------------------------------------------------------- #
# - New             |
# - Open            |
# - Download        |
# --------------------------------------------------------------------------- #
mrsimulator_new = html.A(
    div_icon_text_display("fas fa-file", "New"), href="/", target="_blank"
)
mrsimulator_open = dcc.Upload(
    div_icon_text_display(icon="fas fa-folder-open", text="Open..."),
    id="open-mrsimulator-file",
    accept=".mrsim",
)
# open_recent = html.Div(
#     [
#         div_icon_text_display(icon="fas fa-folder-open", text="Open Recent"),
#         html.Ul([html.Li("Item-1")], id="open-recent-id"),
#     ]
# )

# app.clientside_callback(
#     """
#     function (data) {
#         console.log('data_py', data);
#         if (data == null){
#             throw window.dash_clientside.PreventUpdate;
#         }
#         let len = data.open_recent.length;
#         if (len === 0) {
#             return [];
#         }
#         let li, li_array = [];
#         for(let i=0; i<len; i++){
#             li = document.createElement("li");
#             li.value = data.open_recent[i].path;
#             li_array.push(li);
#         }
#         return li_array;
#     }
#     """,
#     Output("open-recent-id", "children"),
#     [Input("user-config", "data")],
# )

mrsimulator_download = div_icon_text_display(
    icon="fas fa-download", text="Download", id="download-button"
)
file_menu = html.Div(
    [
        html.Label("File"),
        html.Ul(
            [
                html.Li(mrsimulator_new),
                html.Li(mrsimulator_open),
                # html.Li(open_recent),
                html.Li(mrsimulator_download),
            ]
        ),
    ],
    className="file-menu",
)

# Example menu ----------------------------------------------------- #
# Load a list of pre-defined examples from the example_link.json file.
with open("examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)
example_length = len(mrsimulator_examples)

# example_input serves as a temp input whose value is file location of the
# selected example.
example_input = dcc.Input(id="selected-example", style={"display": "none"})
example_menu = html.Div(
    [
        example_input,
        html.Label("Examples"),
        html.Ul(
            [
                html.Li(item["label"], id=f"example-{i}")
                for i, item in enumerate(mrsimulator_examples)
            ]
        ),
    ],
    className="example-menu",
)


@app.callback(
    Output("selected-example", "value"),
    [Input(f"example-{i}", "n_clicks") for i in range(example_length)],
    prevent_initial_call=True,
)
def example_callback(*args):
    if not ctx.triggered:
        raise PreventUpdate
    trigger_index = int(ctx.triggered[0]["prop_id"].split(".")[0].split("-")[1])
    print(trigger_index)
    return mrsimulator_examples[trigger_index]["value"]


# View menu ----------------------------------------------------------------- #
# - Info            |
# - Spin Systems     |
# - Methods         |
# --------------------------------------------------------------------------- #
view_menu = html.Div(
    [
        html.Label("View"),
        html.Ul(
            [
                html.Li(div_icon_text_display("fas fa-info-circle", "Info")),
                html.Li(div_icon_text_display("fac fa-spin-systems", "Spin Systems")),
                html.Li(div_icon_text_display("fas fa-cube", "Methods")),
            ]
        ),
    ],
    className="view-menu",
)

# Spin system menu ----------------------------------------------------------- #
# - Add a new spin system            |
# - Duplicate selected spin system   |
# - Remove selected spin system      |
# - -------------------------------- |
# - Import and add spin systems      |
# - -------------------=------------ |
# - Clear spin systems               |
# --------------------------------------------------------------------------- #
message_topomer = "You are about to delete all spin systems. Do you want to continue?"
spin_system_menu = html.Div(
    [
        html.Label("Spin System"),
        html.Ul(
            [
                html.Li(
                    div_icon_text_display("fas fa-plus-circle", "Add a new spin system")
                ),
                html.Li(
                    div_icon_text_display(
                        "fas fa-clone", "Duplicate selected spin system"
                    )
                ),
                html.Li(
                    div_icon_text_display(
                        "fas fa-minus-circle", "Remove selected spin system"
                    )
                ),
                html.Hr(),
                html.Li(
                    dcc.Upload(
                        div_icon_text_display(
                            "fas fa-hdd", "Import and add spin systems"
                        ),
                        id="upload-and-add-spin-system-button",
                    )
                ),
                html.Hr(),
                html.Li(html.Div("Clear spin systems"), id="clear-spin-systems"),
                dcc.ConfirmDialog(
                    id="confirm-clear-spin-system", message=message_topomer
                ),
            ]
        ),
    ],
    className="spin-system-menu",
)

app.clientside_callback(
    """
    function(n){
        if (n == null){
            throw window.dash_clientside.PreventUpdate;
        }
        return true;
    }
    """,
    Output("confirm-clear-spin-system", "displayed"),
    [Input("clear-spin-systems", "n_clicks")],
    prevent_initial_call=True,
)


# Method menu --------------------------------------------------------------- #
# - Add a new method                        |
# - Duplicate selected method               |
# - Remove selected method                  |
# - --------------------------------------- |
# - Add measurement to the selected method  |
# - Export simulation from selected method  |
# - --------------------------------------- |
# - Clear methods                           |
# --------------------------------------------------------------------------- #
message_method = "You are about to delete all methods. Do you want to continue?"
method_menu = html.Div(
    [
        html.Label("Method"),
        html.Ul(
            [
                html.Li(
                    div_icon_text_display("fas fa-plus-circle", "Add a new method")
                ),
                html.Li(
                    div_icon_text_display("fas fa-clone", "Duplicate selected method")
                ),
                html.Li(
                    div_icon_text_display(
                        "fas fa-minus-circle", "Remove selected method"
                    )
                ),
                html.Hr(),
                html.Li(
                    dcc.Upload(
                        div_icon_text_display(
                            "fas fa-file-import",
                            "Add a measurement to the selected method",
                        ),
                        id="import-measurement-for-method",
                    )
                ),
                html.Li(
                    div_icon_text_display(
                        "fas fa-file-export",
                        "Export simulation from the selected method",
                    ),
                    id="export-simulation-from-method",
                ),
                html.Hr(),
                html.Li(html.Div("Clear methods"), id="clear-methods"),
                dcc.ConfirmDialog(id="confirm-clear-methods", message=message_method),
            ]
        ),
    ],
    className="method-menu",
)

app.clientside_callback(
    """
    function(n){
        if (n == null){
            throw window.dash_clientside.PreventUpdate;
        }
        return true;
    }
    """,
    Output("confirm-clear-methods", "displayed"),
    [Input("clear-methods", "n_clicks")],
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(
        namespace="method", function_name="export_simulation_from_selected_method"
    ),
    Output("export-simulation-from-method-link", "href"),
    [Input("export-simulation-from-method", "n_clicks")],
    [State("local-processed-data", "data"), State("decompose", "active")],
    prevent_initial_call=True,
)

# Help menu ----------------------------------------------------------------- #
# - Documentation       |
# - Github              |
# - Report              |
# - Contributors        |
# - About               |
# --------------------------------------------------------------------------- #
documentation_link = html.A(
    div_icon_text_display("fas fa-book-open", "Documentation"),
    href="https://mrsimulator.readthedocs.io/en/stable/",
    target="_blank",
)

github_link = html.A(
    div_icon_text_display("fab fa-github", "Github"),
    href="https://github.com/DeepanshS/mrsimulator",
    className="",
    target="_blank",
)

help_menu = html.Div(
    [
        html.Label("Help"),
        html.Ul(
            [
                html.H6(f"Mrsimulator-app 2019-{year}"),
                html.Li(documentation_link),
                html.Li(github_link),
                html.Li(
                    div_icon_text_display("fas fa-flag", "Report"),
                    id="modal-Report-button",
                ),
                html.Li("Contributors", id="modal-Contributors-button"),
                html.Li("About", id="modal-About-button"),
            ]
        ),
        about_modals,
    ],
    className="help-menu",
)

# Master menu ------------------------------------------------------ #
master_menubar = html.Div(
    [
        html.Div(
            [
                file_menu,
                spin_system_menu,
                method_menu,
                example_menu,
                view_menu,
                help_menu,
            ],
            className="top-toolbar-left",
        ),
        html.Div(
            [advance_settings, download_modal, advance_setting_button],
            className="top-toolbar-right",
        ),
    ],
    className="master-toolbar",
)

# master_menubar = html.Div(
#     [
#         dbc.NavbarBrand(
#             html.Img(
#                 src="/assets/mrsimulator-logo-dark.svg",
#                 height="50rem",
#                 alt="Mrsimulator",
#             )
#         ),
#         menubar,
#     ],
#     className="d-flex",
# )
