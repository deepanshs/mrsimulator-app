# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .site import editor as site_editor
from app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group

__author__ = ["Deepansh J. Srivastava", "Maxwell C. Venetos"]
__email__ = ["srivastava.89@osu.edu", "venetos.5@buckeyemail.osu.edu"]


def site_tab_ui():
    return dbc.Tab(label="Site", children=site_editor(), className="tab-scroll")


def metadata_tab_ui():
    # name
    name = custom_input_group(
        prepend_label="Name",
        input_type="text",
        placeholder="Add name",
        value="Spin system Name",
        id="spin-system-name",
        debounce=True,
    )

    # description
    label = html.Label("Description")
    textarea = dbc.Textarea(
        placeholder="Add a description ... ",
        id="spin-system-description",
        debounce=True,
        style={"height": "12rem"},
    )
    description = html.Div([label, textarea])

    # metadata
    metadata = html.Div([name, description], className="scroll-cards container")
    return dcc.Tab(label="Metadata", children=metadata, className="tab-scroll")


def default_display():
    title = html.H5("Load spin systems or start creating")
    icon = html.Span(
        [
            html.I(className="fac fa-spin-systems fa-4x"),
            html.H6("Add a spin system"),
        ],
        id="open-edit_spin_system",
    )
    return html.Div([title, icon], className="blank-display")


def scrollable():
    default = default_display()
    app.clientside_callback(
        """
        function(n) {
            $('#add-spin-system-button')[0].click();
            throw window.dash_clientside.PreventUpdate;
        }
        """,
        Output("open-edit_spin_system", "children"),
        [Input("open-edit_spin_system", "n_clicks")],
        prevent_initial_call=True,
    )
    read_only_content = html.Div(default, id="spin-system-read-only")
    return html.Div(read_only_content, className="slider1")


def tools():
    new = html.Button(id="add-spin-system-button")
    duplicate = html.Button(id="duplicate-spin-system-button")
    remove = html.Button(id="remove-spin-system-button")

    return html.Div([new, duplicate, remove], style={"display": "none"})


def header():
    title = html.Div(
        [
            html.I(className="fac fa-spin-systems fa-lg"),
            html.H4("Spin Systems", className="hide-label-sm"),
        ]
    )
    search = dcc.Input(
        value="",
        id="search-spin-system",
        placeholder="Search spin systems",
        type="search",
    )

    # callback for filter the scrollable list based on search.
    app.clientside_callback(
        ClientsideFunction(namespace="spin_system", function_name="searchSpinSystems"),
        Output("search-spin-system", "value"),
        [Input("search-spin-system", "value")],
    )

    return html.Div([title, search], className="card-header")


def layout():
    # abundance
    abundance = html.Div(
        custom_input_group(
            append_label="%",
            prepend_label="Abundance",
            placeholder="Spin system abundance",
            id="spin-system-abundance",
            debounce=True,
            max=100,
            min=0,
        ),
        className="container",
    )

    # title
    label = html.Label(id="spin-system-title")
    title = html.Div(label, className="ui_title")

    # submit button
    submit = custom_button(
        text="Submit Spin System", id="apply-spin-system-changes", color="primary"
    )
    submit = html.Div(submit, className="submit-button")

    # tabs
    tabs = dbc.Tabs([site_tab_ui(), metadata_tab_ui()])

    # spin-system layout
    return html.Div(
        [html.Div([title, abundance, tabs]), submit],
        id="spin-system-editor-content",
        className="slider2",
    )


def ui():
    head = header()
    body = html.Div(
        [scrollable(), layout(), tools()], id="iso-slide", className="slide-offset"
    )

    return html.Div(
        className="left-card",
        children=html.Div([head, body]),
        id="spin_systems-body",
    )


def generate_sidepanel(spin_system, index):
    """Generate scrollable side panel listing for spin systems"""
    title = html.B(f"Spin system {index}", className="")

    # spin system name
    name = "" if "name" not in spin_system else spin_system["name"]
    name = html.Div(f"Name: {name}", className="")

    # spin system abundance
    abundance = np.around(spin_system["abundance"], decimals=3)
    abundance = html.Div(f"Abundance: {abundance} %", className="")

    # number of sites
    n_sites = len(spin_system["sites"])
    n_sites = html.Div(f"Sites: {n_sites}")

    a_tag = html.A([title, name, abundance, n_sites])

    # The H6(index) only shows for smaller screen sizes.
    return html.Li(
        [html.H6(index), html.Div(a_tag)],
        # draggable="true",
        className="list-group-item",
    )


def refresh(systems):
    """Return a html for rendering the display in the read-only spin-system section."""
    output = [generate_sidepanel(sys, i) for i, sys in enumerate(systems)]
    if output == []:
        return default_display()
    return html.Div([html.Ul(output, className="list-group")], className="display-form")


spin_system_body = ui()

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_spin_system_json"),
    Output("new-spin-system", "data"),
    [
        Input("apply-spin-system-changes", "n_clicks"),
        Input("add-spin-system-button", "n_clicks"),
        Input("duplicate-spin-system-button", "n_clicks"),
        Input("remove-spin-system-button", "n_clicks"),
        # Input("spin-system-name", "value"),
        # Input("spin-system-description", "value"),
        # Input("spin-system-abundance", "value"),
        # Input("isotope", "value"),
        # Input("isotropic_chemical_shift", "value"),
        # Input("shielding_symmetric-zeta", "value"),
        # Input("shielding_symmetric-eta", "value"),
        # Input("shielding_symmetric-alpha", "value"),
        # Input("shielding_symmetric-beta", "value"),
        # Input("shielding_symmetric-gamma", "value"),
        # Input("quadrupolar-Cq", "value"),
        # Input("quadrupolar-eta", "value"),
        # Input("quadrupolar-alpha", "value"),
        # Input("quadrupolar-beta", "value"),
        # Input("quadrupolar-gamma", "value"),
    ],
    # [State('live-update', 'value')]
    prevent_initial_call=True,
)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_spin_systems_load"),
    Output("temp2", "children"),
    [Input("spin-system-read-only", "children")],
    [State("config", "data")],
    prevent_initial_call=True,
)
