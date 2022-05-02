# -*- coding: utf-8 -*-
"""The home page consists of
- File overview
- Method overview
- Spin system overview
"""
import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app
from app.custom_widgets import custom_button
from app.sims.home.modal import modal


DEFAULT_MRSIM_DATA = {
    "simulator": {
        "name": "",
        "description": "",
        "spin_systems": [],
        "methods": [],
        "config": {},
    },
    "signal_processors": [],
    "application": {},
}


def edit_sample_info_button_ui():
    """Pencil button to toggle tile and description modal window"""
    return custom_button(
        icon_classname="fas fa-pencil-alt",
        tooltip="Click to edit title and description.",
        id="title-home-button",
        className="icon-button",
        module="html",
    )


def download_session_ui():
    """Download the current session as .mrsim files"""
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
        Input("download-session-button", "n_clicks"),
        State("local-simulator-data", "data"),
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


# pre-define the components to avoid defining multiple components with same id.
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
    """Method info header"""
    return html.Div(
        [html.H5("Method Overview"), preset["tools"]], **{"data-table-header-mth": ""}
    )


def spin_system_header():
    """Spin system info header"""
    return html.Div(
        [html.H5("Spin system Overview"), preset["tools"]],
        **{"data-table-header-sys": ""},
    )


def sample_overview_layout(title, description):
    """Update sample info layout"""
    return [sample_header(title), dbc.Card(dbc.CardBody(description))]


def method_overview_layout(mrsim: dict):
    """Update method info layout"""
    method_table = get_method_overview_table(mrsim)
    return [method_header(), method_table]


def spin_system_overview_layout(mrsim: dict):
    """Update spin system info layout"""
    spin_system_table = get_spin_system_overview_table(mrsim)
    return [spin_system_header(), spin_system_table]


def get_method_overview_table(mrsim: dict):
    """Update method info table data"""
    # number of methods
    n_methods = 0 if "methods" not in mrsim else len(mrsim["simulator"]["methods"])
    mth_brief = html.Div([f"Number of methods: {n_methods}"])

    # method table rows
    method_row = method_overview_data(mrsim)
    mth_table = html.Table(method_row, id="method-table", **{"data-table-mth": ""})

    return html.Div([mth_brief, mth_table])


def get_spin_system_overview_table(mrsim: dict):
    """Update spin system info table data"""
    # number of spin systems
    sim = mrsim["simulator"]
    n_sys = 0 if "spin_systems" not in sim else len(sim["spin_systems"])
    sys_brief = html.Div([f"Number of spin systems: {n_sys}"])

    # spin system table rows
    sys_row = system_overview_data(mrsim)
    sys_table = html.Table(sys_row, id="system-table", **{"data-table-sys": ""})

    return html.Div([sys_brief, sys_table])


def system_overview_data(mrsim: dict):
    """Update spin system overview data"""
    sys_header = ["", "Name", "%", "# Sites", "Isotopes", ""]
    sys_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in sys_header]))]

    if "spin_systems" not in mrsim["simulator"]:
        return sys_row

    icon = html.I(className="fas fa-pencil-alt", title="Edit spin system")
    icon_span = html.Span(icon, **{"data-edit-sys": ""})
    for i, spin_system in enumerate(mrsim["simulator"]["spin_systems"]):
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
    """Update method over data"""
    mth_header = ["", "Name", "Channels", "B0 / T", "vr / kHz", ""]
    method_row = [html.Thead(html.Tr([html.Th(html.B(item)) for item in mth_header]))]

    if "methods" not in mrsim["simulator"]:
        return method_row

    icon = html.I(className="fas fa-pencil-alt", title="Edit method")
    icon_span = html.Span(icon, **{"data-edit-mth": ""})
    for i, method in enumerate(mrsim["simulator"]["methods"]):
        name = f"Method-{i}" if "name" not in method.keys() else method["name"]
        channels = "-".join(method["channels"])

        # magnetic flux density
        b_0 = method["magnetic_flux_density"]
        b_0 = "" if b_0 is None else b_0.split(" ")[0]

        # rotor frequency
        v_r = method["rotor_frequency"]
        v_r = "" if v_r is None else float(v_r.split(" ")[0]) / 1e3

        pack = [i, name, channels, b_0, v_r, icon_span]
        method_row += [html.Thead(html.Tr([html.Td(item) for item in pack]))]

    return method_row


def refresh(mrsim):
    """Refresh and update the info ui"""
    sim = mrsim["simulator"]

    title = sim["name"] if "name" in sim else ""
    title = title if title != "" else "Title"

    description = sim["description"] if "description" in sim else ""
    description = description if description != "" else "Sample description"

    sample_overview = sample_overview_layout(title, description)
    method_overview = method_overview_layout(mrsim)
    system_overview = spin_system_overview_layout(mrsim)
    return html.Div(
        [*sample_overview, *method_overview, *system_overview],
        **{"data-home-table": ""},
    )


def user_interface():
    """Generate info user interface"""
    page = refresh(DEFAULT_MRSIM_DATA)
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


home_body = user_interface()
