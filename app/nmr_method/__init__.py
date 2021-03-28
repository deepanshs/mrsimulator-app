# -*- coding: utf-8 -*-
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import mrsimulator.methods as mt
from dash.dependencies import ALL
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

import app.nmr_method.fields as mrfields
from app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_card
from app.nmr_method.post_simulation_widgets import gaussian_linebroadening_widget
from app.spin_system.site import isotope_options_list

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]

METHOD_LIST = [
    mt.BlochDecaySpectrum,
    mt.BlochDecayCTSpectrum,
    # mt.ThreeQ_VAS,
]
METHOD_DIMENSIONS = [item.ndim for item in METHOD_LIST]
METHOD_OPTIONS = [
    {"label": "Bloch Decay Spectrum", "value": 0},
    {"label": "Bloch Decay Central Transition Spectrum", "value": 1},
    # {"label": "Triple-quantum variable-angle spinning", "value": 2},
    # {"label": "Custom 2D method", "value": "Custom2D"},
]


def method_select_modal():
    """Modal window for method selection"""
    # title
    head = dbc.ModalHeader("Select a method")

    # method selection
    method_selection = dcc.Dropdown(id="method-type", options=METHOD_OPTIONS, value=0)

    # Channel selection
    ch_label = dbc.InputGroupAddon("Channel", addon_type="prepend")
    ch_selection = dbc.Select(options=isotope_options_list, value="1H", id="channel")
    channel_ui = dbc.InputGroup([ch_label, ch_selection], className="container")

    # select button
    button = dbc.Button(
        "Select",
        id="close-method-selection",
        color="dark",
        className="ml-auto",
        outline=True,
    )

    app.clientside_callback(
        "function(n1, n2, is_open) { return !is_open; }",
        Output("method-modal", "is_open"),
        [
            Input("add-method-button", "n_clicks"),
            Input("close-method-selection", "n_clicks"),
        ],
        [State("method-modal", "is_open")],
        prevent_initial_call=True,
    )

    return dbc.Modal(
        [head, dbc.ModalBody(method_selection), channel_ui, dbc.ModalFooter(button)],
        is_open=False,
        id="method-modal",
    )


def post_simulation(n_dimensions):
    # create line broadening => widgets for
    # 1) apodization function and
    # 2) apodization factor,
    return html.Div(
        [
            custom_card(
                text=f"Line broadening - {i}",
                children=gaussian_linebroadening_widget(i),
            )
            for i in range(n_dimensions)
        ],
        className="method-scroll",
    )


def dimension_tabs_ui():
    return dbc.Tabs(
        [
            dbc.Tab(label="0", children=mrfields.spectral_dimension_ui(0), id="dim-0"),
            dbc.Tab(label="1", children=mrfields.spectral_dimension_ui(1), id="dim-1"),
        ],
        # vertical=True,
        className="vertical-tabs",
    )


def method_property_tab_ui():
    return dbc.Tab(
        label="Properties",
        children=[mrfields.global_environment(), dimension_tabs_ui()],
        id="dim-tab",
        className="tab-scroll method",
    )


def signal_processing_tab_ui():
    return dbc.Tab(
        label="Signal Processing",
        children=post_simulation(1),
        className="tab-scroll method",
    )


def default_display():
    title = html.H5("Load methods or start creating")
    icon = html.Span(
        [
            html.I(className="fas fa-cube fa-4x"),
            html.H6("Add a method"),
        ],
        id="open-edit_method",
    )
    return html.Div([title, icon], className="blank-display")


def scrollable():
    default = default_display()
    app.clientside_callback(
        """
        function(n) {
            $('#add-method-button')[0].click();
            throw window.dash_clientside.PreventUpdate;
        }
        """,
        Output("open-edit_method", "children"),
        [Input("open-edit_method", "n_clicks")],
        prevent_initial_call=True,
    )
    method_read_only = html.Div(default, id="method-read-only")
    return html.Div(method_read_only, className="slider1")


def tools():
    """Add, duplcicate, or remove methods"""
    new = html.Button(id="add-method-button")
    duplicate = html.Button(id="duplicate-method-button")
    remove = html.Button(id="remove-method-button")

    return html.Div(children=[new, duplicate, remove], style={"display": "none"})


def header():
    title = html.Div(
        [
            html.I(className="fas fa-cube fa-lg"),
            html.H4("Methods", className="hide-label-sm"),
        ]
    )
    search = dcc.Input(
        value="", id="search-method", placeholder="Search methods", type="search"
    )
    return html.Div([title, search], className="card-header")


def layout():
    # label
    label = html.Label(id="method-title")

    # upload experiment dataset
    icon = html.I(className="fas fa-paperclip fa-lg")
    tooltip = dbc.Tooltip(
        "Attach a measurement to the selected method",
        target="import-measurement-for-method",
    )
    clip_btn = html.Button([icon, tooltip], className="icon-button")
    upload = dcc.Upload(clip_btn, id="import-measurement-for-method")

    # title
    title = html.Div([label, upload], className="ui_title")

    # submit button
    submit = custom_button(text="Submit Method", id="apply-method-changes")
    submit = html.Div(submit, className="submit-button")

    # tabs
    tabs = dbc.Tabs([method_property_tab_ui(), signal_processing_tab_ui()])

    # method layout
    return html.Div(
        [html.Div([title, tabs]), submit],
        id="method-editor-content",
        className="slider2",
    )


def ui():
    head = header()
    body = html.Div(
        [scrollable(), layout(), tools()], id="met-slide", className="slide-offset"
    )

    return html.Div(
        className="left-card",
        children=html.Div([head, body, method_select_modal()]),
        id="methods-body",
    )


def generate_sidepanel(method, index):
    """Generate scrollable side panel listing for methods"""
    title = html.B(f"Method {index}", className="")

    # method name
    name = method["name"]
    name = f"{name[:15]}..." if len(name) > 15 else name
    name = html.Div(name, className="")

    # method channel(s)
    channels = ", ".join(method["channels"])
    channels = html.Div(f"Channel: {channels}")

    # n dimensions
    n_dim = len(method["spectral_dimensions"])
    n_dim = html.Div(f"Dimensions: {n_dim}")

    a_tag = html.A([title, name, channels, n_dim])

    # The H6(index) only shows for smaller screen sizes.
    return html.Li(
        [html.H6(index), html.Div(a_tag)],
        # draggable="true",
        className="list-group-item",
        id={"type": "select-method-index", "index": index},
    )


def refresh(methods):
    """Return a html for rendering the display in the read-only spin-system section."""
    output = [generate_sidepanel(mth, i) for i, mth in enumerate(methods)]
    return html.Div([html.Ul(output, className="list-group")], className="display-form")


dimension_body = ui()


# callback code section =======================================================
@app.callback(
    Output("add-method-from-template", "data"),
    [Input("close-method-selection", "n_clicks")],
    [
        State("method-type", "value"),
        State("channel", "value"),
        # State("modal-rotor_angle", "value"),
        # State("modal-rotor_frequency", "value"),
        # State("modal-magnetic_flux_density", "value"),
        # State("modal-count", "value"),
        # State("modal-spectral_width", "value"),
        # State("modal-reference_offset", "value"),
    ],
    prevent_initial_call=True,
)
def get_method_json(n, value, isotope):
    if n is None:
        raise PreventUpdate
    print(value)
    d0 = {"count": 512, "spectral_width": 25000}
    return {
        "method": METHOD_LIST[value](
            channels=[isotope],
            spectral_dimensions=[d0] * METHOD_DIMENSIONS[value],
        ).reduced_dict(),
        "time": int(datetime.now().timestamp() * 1000),
    }


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_methods_load"),
    Output("temp4", "children"),
    [Input("method-read-only", "children")],
    [State("config", "data")],
    prevent_initial_call=True,
)

app.clientside_callback(
    """
    function(n) {
        set_method_index(n);
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    Output("temp6", "children"),
    [Input("select-method", "value")],
    prevent_initial_call=True,
)

app.clientside_callback(
    """
    function(n, value) {
        let index = get_method_index();
        if (index == value) throw window.dash_clientside.PreventUpdate;
        return index;
    }
    """,
    Output("select-method", "value"),
    [Input({"type": "select-method-index", "index": ALL}, "n_clicks")],
    [State("select-method", "value")],
    prevent_initial_call=True,
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_method_json"),
    Output("new-method", "data"),
    [
        Input("apply-method-changes", "n_clicks"),
        Input("add-method-from-template", "modified_timestamp"),
        Input("duplicate-method-button", "n_clicks"),
        Input("remove-method-button", "n_clicks"),
        # Input("magnetic_flux_density-0", "value"),
        # Input("rotor_angle-0", "value"),
        # Input("rotor_frequency-0", "value"),
        # *[Input(f"count-{i}", "value") for i in range(2)],
        # *[Input(f"spectral_width-{i}", "value") for i in range(2)],
        # *[Input(f"reference_offset-{i}", "value") for i in range(2)],
    ],
    [State("add-method-from-template", "data")],
    prevent_initial_call=True,
)
