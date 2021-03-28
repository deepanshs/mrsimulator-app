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


DEFAULT_SAMPLE = {"name": "Title", "description": "Sample description"}


def edit_sample_info_button_ui():
    return custom_button(
        icon_classname="fas fa-pencil-alt",
        tooltip="Edit",
        id="title-home-button",
        className="icon-button",
        module="html",
    )


def download_session_ui():
    session_link = html.A(id="download-session-link", style={"display": "none"})
    session_button = custom_button(
        icon_classname="fas fa-file-download fa-lg",
        tooltip="Download Session",
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
    return html.Ul(
        [
            html.Li(html.Span(html.I(className="fas fa-plus-circle fa-lg"))),
            html.Li(html.Span(html.I(className="fas fa-clone fa-lg"))),
            html.Li(html.Span(html.I(className="fas fa-minus-circle fa-lg"))),
        ],
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

    icon = html.Span(html.I(className="fas fa-pencil-alt"), **{"data-edit-sys": ""})
    for i, spin_system in enumerate(mrsim["spin_systems"]):
        name = "" if "name" not in spin_system else spin_system["name"]
        abd = np.around(spin_system["abundance"], decimals=3)
        n_site = len(spin_system["sites"])
        isotopes = "-".join(set([item["isotope"] for item in spin_system["sites"]]))
        pack = [i, name, abd, n_site, isotopes, icon]
        sys_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return sys_row


def method_overview_data(mrsim: dict):
    mth_header = ["", "Name", "Channels", "B0 / T", "vr / kHz", ""]
    method_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in mth_header]))]

    if "methods" not in mrsim:
        return method_row

    icon = html.Span(html.I(className="fas fa-pencil-alt"), **{"data-edit-mth": ""})
    for i, method in enumerate(mrsim["methods"]):
        name = "" if "name" not in method.keys() else method["name"]
        channels = "-".join(method["channels"])
        location = method["spectral_dimensions"][0]["events"][0]
        Bo = location["magnetic_flux_density"]
        vr = location["rotor_frequency"] / 1e3
        pack = [i, name, channels, Bo, vr, icon]
        method_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return method_row


def refresh_page(mrsim):
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


def refresh_home(json_data):
    return refresh_page(json_data)


default_home_page = html.Div(
    className="left-card active",
    children=dcc.Upload(
        dcc.Loading(html.Div(refresh_home(DEFAULT_SAMPLE), id="info-read-only")),
        id="upload-spin-system-local",
        disable_click=True,
        multiple=False,
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
        },
    ),
    id="info-body",
)
