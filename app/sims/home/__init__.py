# -*- coding: utf-8 -*-
"""The home page consists of
- File overview
- Method overview
- Spin system overview
"""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .modal import modal
from app import app
from app.custom_widgets import custom_button


def edit_sample_info_button_ui():
    return custom_button(
        icon_classname="fas fa-pencil-alt",
        tooltip="Click to edit title and description.",
        id="title-home-button",
        className="icon-button",
        module="html",
    )


def download_session_ui():
    """Download session"""
    session_link = html.A(id="download-session-link", style={"display": "none"})
    session_button = custom_button(
        icon_classname="fas fa-file-download fa-lg",
        tooltip="Click to download the session",
        id="download-session-button",
        className="icon-button",
        module="html",
    )

    # callback for downloading session
    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="downloadSession"),
        Output("download-session-link", "href"),
        [Input("download-session-button", "n_clicks")],
        [State("local-simulator-data", "data")],
        prevent_initial_call=True,
    )
    return html.Div([session_link, session_button])


def tools():
    """Add, duplicate, and remove tools."""
    add = html.I(className="fas fa-plus-circle fa-lg", title="Add")
    copy = html.I(className="fas fa-clone fa-lg", title="Duplicate")
    remove = html.I(className="fas fa-minus-circle fa-lg", title="Remove")

    return html.Ul(
        [html.Li(html.Span(item)) for item in [add, copy, remove]],
        **{"data-edit-tools": ""},
    )


preset = {
    "edit_sample_info_button": edit_sample_info_button_ui(),
    "download_session": download_session_ui(),
    "tools": tools(),
}


def sample_header(title):
    """Return title and description div"""
    head = [
        html.H4([title, preset["edit_sample_info_button"]]),
        preset["download_session"],
        modal,
    ]
    return html.Div(head, style={"display": "flex", "justifyContent": "space-between"})


def method_header():
    return html.Div(
        [html.H5("Method Overview"), preset["tools"]], **{"data-table-header-mth": ""}
    )


def spin_system_header():
    return html.Div(
        [html.H5("Spin system Overview"), preset["tools"]],
        **{"data-table-header-sys": ""},
    )


def sample_overview_layout(title, description):
    return [sample_header(title), dbc.Card(dbc.CardBody(description))]


def method_overview_layout(mrsim: dict):
    method_table = get_method_overview_table(mrsim)
    return [method_header(), method_table]


def spin_system_overview_layout(mrsim: dict):
    spin_system_table = get_spin_system_overview_table(mrsim)
    return [spin_system_header(), spin_system_table]


def get_method_overview_table(mrsim: dict):
    # number of methods
    n_methods = 0 if "methods" not in mrsim else len(mrsim["methods"])
    mth_brief = html.Div([f"Number of methods: {n_methods}"])

    # method table rows
    method_row = method_overview_data(mrsim)
    mth_table = html.Table(method_row, id="method-table", **{"data-table-mth": ""})

    return html.Div([mth_brief, mth_table])


def get_spin_system_overview_table(mrsim: dict):
    # number of spin systems
    n_sys = 0 if "spin_systems" not in mrsim else len(mrsim["spin_systems"])
    sys_brief = html.Div([f"Number of spin systems: {n_sys}"])

    # spin system table rows
    sys_row = system_overview_data(mrsim)
    sys_table = html.Table(sys_row, id="system-table", **{"data-table-sys": ""})

    return html.Div([sys_brief, sys_table])


def system_overview_data(mrsim: dict):
    sys_header = ["", "Name", "%", "# Sites", "Isotopes", ""]
    sys_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in sys_header]))]

    if "spin_systems" not in mrsim:
        return sys_row

    icon = html.I(className="fas fa-pencil-alt", title="Edit spin system")
    icon_span = html.Span(icon, **{"data-edit-sys": ""})
    for i, spin_system in enumerate(mrsim["spin_systems"]):
        name = "" if "name" not in spin_system else spin_system["name"]
        abd = (
            "100"
            if "abundance" not in spin_system
            else np.around(float(spin_system["abundance"].split(" ")[0]), decimals=3)
        )
        n_site = len(spin_system["sites"])
        isotopes = "-".join(set([item["isotope"] for item in spin_system["sites"]]))
        pack = [i, name, abd, n_site, isotopes, icon_span]
        sys_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return sys_row


def method_overview_data(mrsim: dict):
    mth_header = ["", "Name", "Channels", "B0 / T", "vr / kHz", ""]
    method_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in mth_header]))]

    if "methods" not in mrsim:
        return method_row

    icon = html.I(className="fas fa-pencil-alt", title="Edit method")
    icon_span = html.Span(icon, **{"data-edit-mth": ""})
    for i, method in enumerate(mrsim["methods"]):
        name = "" if "name" not in method.keys() else method["name"]
        channels = "-".join(method["channels"])
        Bo = (
            ""
            if method["magnetic_flux_density"] is None
            else method["magnetic_flux_density"].split(" ")[0]
        )
        vr = (
            ""
            if method["rotor_frequency"] is None
            else float(method["rotor_frequency"].split(" ")[0]) / 1e3
        )
        pack = [i, name, channels, Bo, vr, icon_span]
        method_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return method_row


def overview_page(mrsim):
    title = mrsim["name"]
    title = "Sample" if title == "" else title
    description = mrsim["description"]

    sample_overview = sample_overview_layout(title, description)
    method_overview = method_overview_layout(mrsim)
    system_overview = spin_system_overview_layout(mrsim)
    return html.Div(
        [*sample_overview, *method_overview, *system_overview],
        **{"data-home-table": ""},
    )


def refresh(json_data):
    return overview_page(json_data)


def ui():
    page = refresh({"name": "Title", "description": "Sample description"})
    loading = dcc.Loading(html.Div(page, id="info-read-only"))
    upload_mrsim = dcc.Upload(
        loading,
        id="upload-spin-system-local",
        disable_click=True,
        multiple=False,
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
        },
    )

    return html.Div(
        className="left-card active",
        children=upload_mrsim,
        id="info-body",
    )


home_body = ui()
