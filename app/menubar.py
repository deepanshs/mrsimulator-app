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


def div_icon_text_display_with_submenu(icon, text, id=None):
    return html.Div(
        [
            div_icon_text_display(icon=icon, text=text, id=id),
            div_icon_text_display(icon="fas fa-caret-right 2x", text=""),
        ],
        style={"display": "flex", "align-items": "space-between", "width": "100%"},
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


def create_submenu(title, items):
    parse_items = [
        html.Li(item, className="menu-item") if not isinstance(item, html.Hr) else item
        for item in items
    ]
    return html.Li(
        [html.Label(title), html.Ul(parse_items, className="sub-menu")],
        className="menu-item has-sub-menu",
    )


# File menu ----------------------------------------------------------------- #
# - New             |
# - Open            |
# - Download        |
# --------------------------------------------------------------------------- #
import_items = [
    dcc.Upload(
        "Measurement for the selected method",
        id="import-measurement-for-method",
    ),
    dcc.Upload("Spin systems", id="upload-and-add-spin-system-button"),
]
import_remove_data = create_submenu(
    div_icon_text_display_with_submenu(
        "fas fa-file-import",
        "Import",
    ),
    import_items,
)

export_items = [
    html.Div("Simulation from the selected method", id="export-simulation-from-method")
]
export_data = create_submenu(
    div_icon_text_display_with_submenu(
        "fas fa-file-export",
        "Export",
    ),
    export_items,
)

file_items = [
    html.A(div_icon_text_display("fas fa-file", "New"), href="/", target="_blank"),
    dcc.Upload(
        div_icon_text_display(icon="fas fa-folder-open", text="Open..."),
        id="open-mrsimulator-file",
        accept=".mrsim",
    ),
    div_icon_text_display(
        icon="fas fa-download", text="Download", id="download-button"
    ),
    html.Hr(),
    import_remove_data,
    export_data,
]
file_menu = create_submenu("File", file_items)

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


# Spin system menu ----------------------------------------------------------- #
# - Add a new spin system            |
# - Duplicate selected spin system   |
# - Remove selected spin system      |
# - -------------------------------- |
# - Clear spin systems               |
# ---------------------------------------------------------------------------- #
message_sys = "You are about to delete all spin systems. Do you want to continue?"
spin_system_items = [
    div_icon_text_display("fas fa-plus-circle", "Add a new spin system", id="add_sys"),
    div_icon_text_display("fas fa-clone", "Duplicate selection", id="copy_sys"),
    div_icon_text_display("fas fa-minus-circle", "Remove selection", id="del_sys"),
    html.Hr(),
    html.Div("Clear all spin systems", id="clear-spin-systems"),
    dcc.ConfirmDialog(id="confirm-clear-spin-system", message=message_sys),
]
spin_system_menu = create_submenu("Spin System", spin_system_items)

target = ["add", "duplicate", "remove"]
source = ["add", "copy", "del"]

for t, s in zip(target, source):
    fn = f"$('#{t}-spin-system-button')[0].click();"
    app.clientside_callback(
        "function(){" + fn + "throw window.dash_clientside.PreventUpdate;}",
        Output(f"{t}-spin-system-button", "n_clicks"),
        [Input(f"{s}_sys", "n_clicks")],
        prevent_initial_call=True,
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
# - Clear methods                           |
# --------------------------------------------------------------------------- #
message_method = "You are about to delete all methods. Do you want to continue?"
method_items = [
    div_icon_text_display("fas fa-plus-circle", "Add a new method", id="add_method"),
    div_icon_text_display("fas fa-clone", "Duplicate selection", id="copy_method"),
    div_icon_text_display("fas fa-minus-circle", "Remove selection", id="del_method"),
    html.Hr(),
    div_icon_text_display(
        "fas fa-times-circle",
        "Remove measurement from selected method",
        id="remove-measurement-from-method",
    ),
    html.Hr(),
    html.Div("Clear all methods", id="clear-methods"),
    dcc.ConfirmDialog(id="confirm-clear-methods", message=message_method),
]
method_menu = create_submenu("Method", method_items)

for t, s in zip(target, source):
    fn = f"$('#{t}-method-button')[0].click();"
    app.clientside_callback(
        "function(){" + fn + "throw window.dash_clientside.PreventUpdate;}",
        Output(f"{t}-method-button", "n_clicks"),
        [Input(f"{s}_method", "n_clicks")],
        prevent_initial_call=True,
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
    [State("local-processed-data", "data")],
    prevent_initial_call=True,
)


# Example menu -------------------------------------------------------------- #
# - List of examples  |
# - ...
# - ...
# --------------------------------------------------------------------------- #
# Load a list of pre-defined examples from the example_link.json file.
with open("examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)
example_length = len(mrsimulator_examples)

# example_input serves as a temp input whose value is file location of the
# selected example.
example_items = [dcc.Input(id="selected-example", style={"display": "none"})]
example_items += [
    html.Div(item["label"], id=f"example-{i}")
    for i, item in enumerate(mrsimulator_examples)
]
example_menu = create_submenu("Examples", example_items)


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
# - Spin Systems    |
# - Methods         |
# --------------------------------------------------------------------------- #
view_items = [
    div_icon_text_display("fas fa-info-circle", "Info", id="menu_info"),
    div_icon_text_display("fac fa-spin-systems", "Spin Systems", id="menu_sys"),
    div_icon_text_display("fas fa-cube", "Methods", id="menu_method"),
]
view_menu = create_submenu("View", view_items)

target = ["info", "spin-systems", "methods"]
source = ["menu_info", "menu_sys", "menu_method"]

for t, s in zip(target, source):
    fn = f"$('#view-{t}')[0].click();"
    app.clientside_callback(
        "function(){" + fn + "throw window.dash_clientside.PreventUpdate;}",
        Output(f"view-{t}", "n_clicks"),
        [Input(s, "n_clicks")],
        prevent_initial_call=True,
    )


# Help menu ----------------------------------------------------------------- #
# - Documentation       |
# - Github              |
# - Report              |
# - Contributors        |
# - About               |
# --------------------------------------------------------------------------- #
help_items = [
    html.H6(f"Mrsimulator-app 2019-{year}"),
    html.A(
        div_icon_text_display("fas fa-book-open", "Documentation"),
        href="https://mrsimulator.readthedocs.io/en/stable/",
        target="_blank",
    ),
    html.A(
        div_icon_text_display("fab fa-github", "Github"),
        href="https://github.com/DeepanshS/mrsimulator",
        className="",
        target="_blank",
    ),
    div_icon_text_display("fas fa-flag", "Report", id="modal-Report-button"),
    html.Div("Contributors", id="modal-Contributors-button"),
    html.Div("About", id="modal-About-button"),
]
help_menu = create_submenu("Help", help_items)


# Advanced settings ----------------------------------------------------------------- #
advance_setting_button = html.A(
    label_icon_text_display(icon="fas fa-cog", text="Setting", id="advance_setting"),
    className="default-button",
)

# Master menu ------------------------------------------------------ #
master_menubar = html.Div(
    [
        html.Ul(
            [
                file_menu,
                spin_system_menu,
                method_menu,
                example_menu,
                view_menu,
                help_menu,
            ],
            className="menu",
        ),
        html.Div(
            [advance_settings, download_modal, advance_setting_button],
            className="right-menu",
        ),
        about_modals,
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
