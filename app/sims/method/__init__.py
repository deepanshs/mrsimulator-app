# -*- coding: utf-8 -*-
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ALL
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from . import fields as mrfields
from . import post_simulation_widgets as ps
from .modal import METHOD_DIMENSIONS
from .modal import METHOD_LIST
from .modal import method_selection_modal
from app import app
from app.custom_widgets import custom_button

# from .post_simulation_widgets import gaussian_linebroadening_widget

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["srivastava.89@osu.edu"]


def hidden_method_select_element():
    """The element is used for update plots based on method selection."""
    select_method = dcc.Dropdown(id="select-method", value=0)
    return html.Div(select_method, style={"display": "none"})


def post_simulation_ui(n_dimensions):
    # create line broadening => widgets for
    # 1) apodization function and
    # 2) apodization factor,
    # gaussian = ps.Gaussian(0, n_dimensions)
    # lorentz = ps.Lorentzian(0, n_dimensions)
    return html.Div(
        [
            html.Div(ps.tools()),
            html.Div(
                [ps.appodization_ui(0)],
                id="post_sim_child",
                className="method-scroll",
            ),
        ]
    )


def dimension_tabs_ui():
    """Supports two dimensions."""
    return [mrfields.spectral_dimension_ui(i) for i in range(2)]


def method_property_tab_ui():
    return dbc.Tab(
        label="Properties",
        children=[mrfields.global_environment(), *dimension_tabs_ui()],
        id="dim-tab",
        className="tab-scroll method",
    )


def signal_processing_tab_ui():
    return dbc.Tab(
        label="Signal Processing",
        children=post_simulation_ui(1),
        className="tab-scroll method",
    )


app.clientside_callback(
    """
    function(val) {
        console.log(val);
        if (val === 'tab-0') {
            return [{'display': 'none'}, {'display': 'block'}];
        }
        if (val === 'tab-1') {
            return [{'display': 'block'}, {'display': 'none'}];
        }
    }
    """,
    [Output("signal-processor-div", "style"), Output("apply-method-div", "style")],
    [Input("method-tabs", "active_tab")],
    prevent_initial_call=True,
)


def display():
    comment = html.H5("Load methods or start creating")
    icon = html.I(className="fas fa-cube fa-4x")
    sub_text = html.H6("Add a method")
    title = html.Span([icon, sub_text], id="open-edit_method")
    return html.Div([comment, title], className="blank-display")


def scrollable():
    default = display()
    app.clientside_callback(
        """
        function(n) {
            document.getElementById("add-method-button").click();
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
        (
            "Click to attach a measurement file to the selected method. "
            "Alternatively, drag and drop the file onto the Simulation area."
        ),
        target="import-measurement-for-method",
    )
    clip_btn = html.Button([icon, tooltip], className="icon-button")
    upload = dcc.Upload(clip_btn, id="import-measurement-for-method")

    # title
    title = html.Div([label, upload], className="ui_title")

    # submit method button
    submit = custom_button(text="Submit Method", id="apply-method-changes")
    submit = html.Div(
        submit,
        id="apply-method-div",
        style={"display": "block"},
        className="submit-button",
    )

    # submit proceeing button
    submit_pro = custom_button(text="Submit Processor", id="signal-processor-button")
    submit_pro = html.Div(
        submit_pro,
        id="signal-processor-div",
        style={"display": "none"},
        className="submit-button",
    )

    # tabs
    tabs = dbc.Tabs(
        [method_property_tab_ui(), signal_processing_tab_ui()], id="method-tabs"
    )

    # method layout
    return html.Div(
        [html.Div([title, tabs]), submit, submit_pro],
        id="method-editor-content",
        className="slider2",
    )


def ui():
    head = header()
    body = html.Div(
        [scrollable(), layout(), tools(), hidden_method_select_element()],
        id="met-slide",
        className="slide-offset",
    )

    return html.Div(
        className="left-card",
        children=html.Div([head, body, method_selection_modal]),
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
    if output == []:
        return display()
    return html.Div(
        [html.Ul(output, className="list-group")], className="scrollable-list"
    )


method_body = ui()


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
    d0 = {"count": 512, "spectral_width": 25000}
    return {
        "method": METHOD_LIST[value](
            channels=[isotope],
            spectral_dimensions=[d0] * METHOD_DIMENSIONS[value],
        ).reduced_dict(),
        "time": int(datetime.now().timestamp() * 1000),
    }


app.clientside_callback(
    ClientsideFunction(namespace="method", function_name="onMethodsLoad"),
    Output("temp4", "children"),
    [Input("method-read-only", "children")],
    [State("config", "data")],
    prevent_initial_call=True,
)

app.clientside_callback(
    """
    function(n) {
        window.method.setIndex(n);
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
        let index = window.method.getIndex();
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
    ClientsideFunction(namespace="method", function_name="updateMethodJson"),
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
