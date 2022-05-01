# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .modal.about import about_modals
from app import app
from app import year


className = "d-flex align-items-center justify-items-center"
TARGET = ["add", "duplicate", "remove"]


def icon_text(icon, text):
    return html.Div(
        [html.I(className=icon, title=text), html.Div(text, className="pl-2")],
        className=className,
    )


def menu_item(children=None, **kwargs):
    return dbc.DropdownMenuItem(children=children, **kwargs)


def create_submenu(**kwargs):
    return dbc.DropdownMenu(caret=False, in_navbar=True, nav=True, **kwargs)


def file_menu():
    """File menu items
    1. New Document
    2. Open mrsimulator file (.mrsim)
    """
    file_items = [
        menu_item(
            icon_text("fas fa-file", "New Document"),
            href="/simulator",
            external_link=True,
            target="_blank",
        ),
        dcc.Upload(
            menu_item(icon_text("fas fa-folder-open", "Open...")),
            id="open-mrsimulator-file",
            accept=".mrsim",
        ),
        menu_item(
            icon_text("fas fa-file-download fa-lg", "Download Session"),
            id="download-session-menu-button",
        ),
    ]

    # callback for downloading session from menu
    app.clientside_callback(
        """function(n) { return n+1; }""",
        Output("download-session-button", "n_clicks"),
        Input("download-session-menu-button", "n_clicks"),
        State("download-session-button", "n_clicks"),
        prevent_initial_call=True,
    )

    return create_submenu(label="File", children=file_items)


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
        menu_item(
            icon_text("fas fa-plus-circle", "Add a new spin system"), id="add_sys"
        ),
        menu_item(icon_text("fas fa-clone", "Duplicate selection"), id="duplicate_sys"),
        menu_item(
            icon_text("fas fa-minus-circle", "Remove selection"), id="remove_sys"
        ),
        menu_item(divider=True),
        menu_item(icon_text("", "Clear all spin systems"), id="clear-spin-systems"),
        dcc.ConfirmDialog(id="confirm-clear-spin-system", message=message_sys),
    ]

    # Callbacks for the add, duplicate, and remove spin systems
    _ = [
        app.clientside_callback(
            f"""function() {{
                document.getElementById("{t}-spin-system-button").click();
                throw window.dash_clientside.PreventUpdate;
            }}""",
            Output(f"{t}-spin-system-button", "n_clicks"),
            Input(f"{t}_sys", "n_clicks"),
            prevent_initial_call=True,
        )
        for t in TARGET
    ]

    # Callbacks for the clear all spin systems
    app.clientside_callback(
        """function(n) {
            if (n == null) throw window.dash_clientside.PreventUpdate;
            return true;
        }""",
        Output("confirm-clear-spin-system", "displayed"),
        Input("clear-spin-systems", "n_clicks"),
        prevent_initial_call=True,
    )

    return create_submenu(label="Spin System", children=spin_system_items, right=True)


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
        menu_item(icon_text("fas fa-plus-circle", "Add a new method"), id="add_method"),
        menu_item(
            icon_text("fas fa-clone", "Duplicate selection"), id="duplicate_method"
        ),
        menu_item(
            icon_text("fas fa-minus-circle", "Remove selection"), id="remove_method"
        ),
        menu_item(divider=True),
        menu_item("Clear all methods", id="clear-methods"),
        menu_item(divider=True),
        menu_item("Measurement", header=True),
        menu_item(
            dcc.Upload(
                icon_text("fas fa-paperclip", "Add to selection"),
                id="add-measurement-for-method",
            )
        ),
        menu_item(
            icon_text("fas fa-times-circle", "Remove from selection"),
            id="remove-measurement-from-method",
        ),
        dcc.ConfirmDialog(id="confirm-clear-methods", message=message_method),
    ]

    # Callbacks for the add, duplicate, and remove methods
    _ = [
        app.clientside_callback(
            f"""function() {{
                document.getElementById("{t}-method-button").click();
                throw window.dash_clientside.PreventUpdate;
            }}""",
            Output(f"{t}-method-button", "n_clicks"),
            Input(f"{t}_method", "n_clicks"),
            prevent_initial_call=True,
        )
        for t in TARGET
    ]

    # Callbacks for the clear all methods
    app.clientside_callback(
        """function(n) {
            if (n == null) throw window.dash_clientside.PreventUpdate;
            return true;
        }""",
        Output("confirm-clear-methods", "displayed"),
        Input("clear-methods", "n_clicks"),
        prevent_initial_call=True,
    )

    return create_submenu(label="Method", children=method_items, right=False)


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
#     fn = f"document.getElementById("view-{t}").click();"
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
        menu_item(f"Mrsimulator-app 2019-{year}", header=True),
        menu_item(
            icon_text("fas fa-book-open", "Documentation"),
            href="https://mrsimulator.readthedocs.io/en/stable/",
            external_link=True,
            target="_blank",
        ),
        menu_item(
            icon_text("fab fa-github", "Github project"),
            href="https://github.com/DeepanshS/mrsimulator",
            external_link=True,
            target="_blank",
        ),
        menu_item(icon_text("fas fa-flag", "Report"), id="modal-Report-button"),
        menu_item(
            icon_text("fas fa-users", "Contributors"),
            href="https://github.com/DeepanshS/mrsimulator-app/graphs/contributors",
            external_link=True,
            target="_blank",
        ),
        menu_item(
            icon_text("fas fa-comments", "Start a discussion"),
            href="https://github.com/DeepanshS/mrsimulator-app/discussions",
            external_link=True,
            target="_blank",
        ),
        menu_item(icon_text("fas fa-info-circle", "About"), id="modal-about-button"),
        about_modals,
    ]

    return create_submenu(label="Help", children=help_items, right=True)


def layout():
    return [file_menu(), method_menu(), spin_system_menu(), help_menu()]


def ui():
    return html.Div(
        html.Ul(layout(), className="menu"), className="master-toolbar nav-composite"
    )


master_menubar = ui()
