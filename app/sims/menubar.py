# -*- coding: utf-8 -*-
import json

import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.exceptions import PreventUpdate

from .modal.about import about_modals
from app import app
from app import year


className = "d-flex align-items-center justify-items-center"
TARGET = ["add", "duplicate", "remove"]


def menu_item(icon, text, id=None):
    if id is not None:
        return html.Div(
            [html.I(className=icon), html.Div(text, className="pl-2")],
            className=className,
            id=id,
        )
    return html.Div(
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


def file_menu():
    """File menu items
    1. New Document
    2. Open mrsimulator file (.mrsim)
    """
    file_items = [
        html.A(menu_item("fas fa-file", "New Document"), href="/", target="_blank"),
        dcc.Upload(
            menu_item(icon="fas fa-folder-open", text="Open..."),
            id="open-mrsimulator-file",
            accept=".mrsim",
        ),
        # import_remove_data,
    ]
    return create_submenu(html.Span(html.I(className="fas fa-bars fa-lg")), file_items)


def spin_system_menu():
    """Spin system menu items
    1. Add a new spin system
    2. Duplicate selected spin system
    3. Remove selected spin system
    ----------------------------------
    4. Clear spin systems
    """
    message_sys = "You are about to delete all spin systems. Do you want to continue?"
    spin_system_items = [
        menu_item("fas fa-plus-circle", "Add a new spin system", id="add_sys"),
        menu_item("fas fa-clone", "Duplicate selection", id="duplicate_sys"),
        menu_item("fas fa-minus-circle", "Remove selection", id="remove_sys"),
        html.Hr(),
        html.Div("Clear all spin systems", id="clear-spin-systems"),
        dcc.ConfirmDialog(id="confirm-clear-spin-system", message=message_sys),
    ]

    # Callbacks for the add, dublicate, and remove spin systems
    [
        app.clientside_callback(
            f"""
            function() {{
                $('#{t}-spin-system-button')[0].click();
                throw window.dash_clientside.PreventUpdate;
            }}
            """,
            Output(f"{t}-spin-system-button", "n_clicks"),
            [Input(f"{t}_sys", "n_clicks")],
            prevent_initial_call=True,
        )
        for t in TARGET
    ]

    # Callbacks for the clear all spin systems
    app.clientside_callback(
        """
        function(n) {
            if (n == null) throw window.dash_clientside.PreventUpdate;
            return true;
        }
        """,
        Output("confirm-clear-spin-system", "displayed"),
        [Input("clear-spin-systems", "n_clicks")],
        prevent_initial_call=True,
    )

    return create_submenu("Spin System", spin_system_items)


def method_menu():
    """Method menu items
    1. Add a new method
    2. Duplicate selected method
    3. Remove selected method
    ------------------------------
    4. Clear methods
    """
    message_method = "You are about to delete all methods. Do you want to continue?"
    method_items = [
        menu_item("fas fa-plus-circle", "Add a new method", id="add_method"),
        menu_item("fas fa-clone", "Duplicate selection", id="duplicate_method"),
        menu_item("fas fa-minus-circle", "Remove selection", id="remove_method"),
        html.Hr(),
        menu_item(
            "fas fa-times-circle",
            "Remove measurement from selection",
            id="remove-measurement-from-method",
        ),
        html.Hr(),
        html.Div("Clear all methods", id="clear-methods"),
        dcc.ConfirmDialog(id="confirm-clear-methods", message=message_method),
    ]

    # Callbacks for the add, dublicate, and remove methods
    [
        app.clientside_callback(
            f"""
            function() {{
                $('#{t}-method-button')[0].click();
                throw window.dash_clientside.PreventUpdate;
            }}
            """,
            Output(f"{t}-method-button", "n_clicks"),
            [Input(f"{t}_method", "n_clicks")],
            prevent_initial_call=True,
        )
        for t in TARGET
    ]

    # Callbacks for the clear all methods
    app.clientside_callback(
        """
        function(n) {
            if (n == null) throw window.dash_clientside.PreventUpdate;
            return true;
        }
        """,
        Output("confirm-clear-methods", "displayed"),
        [Input("clear-methods", "n_clicks")],
        prevent_initial_call=True,
    )

    return create_submenu("Method", method_items)


def example_menu():
    """Example menu contains a list of examples."""
    with open("app/examples/example_link.json", "r") as f:
        mrsimulator_examples = json.load(f)
    example_length = len(mrsimulator_examples)

    # example_input serves as a temp input whose value is file location of the
    # selected example.
    example_items = [dcc.Input(id="selected-example", style={"display": "none"})]
    example_items += [
        html.Div(item["label"], id=f"example-{i}")
        for i, item in enumerate(mrsimulator_examples)
    ]

    @app.callback(
        Output("selected-example", "value"),
        [Input(f"example-{i}", "n_clicks") for i in range(example_length)],
        prevent_initial_call=True,
    )
    def example_callback(*args):
        if not ctx.triggered:
            raise PreventUpdate
        trigger_index = int(ctx.triggered[0]["prop_id"].split(".")[0].split("-")[1])
        print("example index", trigger_index)
        print(mrsimulator_examples[trigger_index]["value"])
        return mrsimulator_examples[trigger_index]["value"]

    return create_submenu("Examples", example_items)


# View menu ----------------------------------------------------------------- #
# - Info            |
# - Spin Systems    |
# - Methods         |
# --------------------------------------------------------------------------- #
# view_items = [
#     div_icon_text_display("fas fa-info-circle", "Info", id="menu_info"),
#     div_icon_text_display("fac fa-spin-systems", "Spin Systems", id="menu_sys"),
#     div_icon_text_display("fas fa-cube", "Methods", id="menu_method"),
# ]
# view_menu = create_submenu("View", view_items)

# target = ["info", "spin-systems", "methods"]
# source = ["menu_info", "menu_sys", "menu_method"]

# for t, s in zip(target, source):
#     fn = f"$('#view-{t}')[0].click();"
#     app.clientside_callback(
#         "function(){" + fn + "throw window.dash_clientside.PreventUpdate;}",
#         Output(f"view-{t}", "n_clicks"),
#         [Input(s, "n_clicks")],
#         prevent_initial_call=True,
#     )


def help_menu():
    """Help menu items
    1. Documentation
    2. Github
    3. Report
    4. Contributors
    5. About
    """
    help_items = [
        html.H6(f"Mrsimulator-app 2019-{year}"),
        html.A(
            menu_item("fas fa-book-open", "Documentation"),
            href="https://mrsimulator.readthedocs.io/en/stable/",
            target="_blank",
        ),
        html.A(
            menu_item("fab fa-github", "Github"),
            href="https://github.com/DeepanshS/mrsimulator",
            className="",
            target="_blank",
        ),
        menu_item("fas fa-flag", "Report", id="modal-Report-button"),
        menu_item("fas fa-users", "Contributors", id="modal-Contributors-button"),
        menu_item("fas fa-info-circle", "About", id="modal-About-button"),
        about_modals,
    ]

    return create_submenu("Help", help_items)


def layout():
    return [file_menu(), spin_system_menu(), method_menu(), example_menu(), help_menu()]


def ui():
    return html.Div(
        html.Ul(layout(), className="menu"), className="master-toolbar nav-composite"
    )


master_menubar = ui()
