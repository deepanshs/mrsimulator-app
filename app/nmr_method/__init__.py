# -*- coding: utf-8 -*-
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import mrsimulator.methods as mt
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from .toolbar import search_method
from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_card
from app.nmr_method.post_simulation_widgets import gaussian_linebroadening_widget
from app.nmr_method.simulation_widgets import property_setup
from app.nmr_method.simulation_widgets import spectral_dimension_ui
from app.spin_system import isotope_options_list

# from app.custom_widgets import custom_input_group

METHOD_LIST = [
    mt.BlochDecaySpectrum,
    mt.BlochDecayCentralTransitionSpectrum,
    # mt.ThreeQ_VAS,
]
DIM_INDEX = [1, 1, 2]
# "Custom2D": mt.Custom2D(spectral_dimensions=[{}, {}]).reduced_dict(),


METHOD_OPTIONS = [
    {"label": "Bloch Decay Spectrum", "value": 0},
    {"label": "Bloch Decay Central Transition Spectrum", "value": 1},
    # {"label": "Triple-quantum variable-angle spinning", "value": 2},
    # {"label": "Custom 2D method", "value": "Custom2D"},
]

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# nmr_method parameters
def generate_parameters(n_dimensions):
    """Create a spectral dimension interface."""

    # create spectral dimension => widgets for
    # 1) number of points,
    # 2) spectral width,
    # 3) reference offset, and
    spectral_dimension_ui_ = [
        custom_card(text=f"Spectral dimension - {i}", children=spectral_dimension_ui(i))
        for i in range(n_dimensions)
    ]

    return html.Div(spectral_dimension_ui_)


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


submit_button = html.Div(
    custom_button(text="Submit Method", id="apply-method-changes", color="primary"),
    className="submit-button",
)

edit_button = html.Div(
    custom_button(text="Edit Method", id="edit-method", color="primary"),
    className="submit-button",
)

# update-dataset
btn = dbc.Button(
    [
        html.Span(
            html.I(className="fas fa-paperclip fa-lg"),
            className="d-flex align-items-center",
        ),
        dbc.Tooltip(
            "Attach a measurement to the selected method",
            target="import-measurement-for-method",
        ),
    ],
    className="icon-button",
)
upload = dcc.Upload(btn, id="import-measurement-for-method")

# method-title
method_title = html.Div(
    [html.Label(id="method-title"), upload], className="spin-system-title"
)

# method metadata
method_description = html.Div(
    [
        html.Label("Description"),
        dbc.Textarea(
            value="",
            placeholder="Add a description ... ",
            id="method-description",
            style={"height": "12rem"},
        ),
    ],
    className="container",
)


dimensions_tab = dbc.Tabs(
    [
        dbc.Tab(label="0", children=property_setup(0), id="dim-0"),
        dbc.Tab(label="1", children=property_setup(1), id="dim-1"),
    ],
    # vertical=True,
    className="vertical-tabs",
)
# method contents
method_contents = dbc.Tabs(
    children=[
        dbc.Tab(label="Dimensions", children=dimensions_tab, id="dim-tab"),
        # dbc.Tab(
        #     label="Metadata",
        #     children=[method_description],
        #     className="tab-scroll method",
        # ),
        dbc.Tab(
            label="Signal Processing",
            children=[post_simulation(1)],
            className="tab-scroll method",
        ),
    ],
    id="dimension-tabs",
)

# channels
# channel = dbc.InputGroup(
#     [
#         dbc.InputGroupAddon("Channel", addon_type="prepend"),
#         dbc.Select(options=isotope_options_list, value="1H", id="channel"),
#     ],
#     className="container",
# )

# method editor
method_editor = html.Form(
    [html.Div([method_title, method_contents]), submit_button],
    id="method-editor-content",
)

# method read only section
method_read_only = html.Div(id="method-read-only")

# slides
method_slide_1 = html.Div(method_read_only, className="slider1")
method_slide_2 = html.Div(method_editor, className="slider2")
method_slide = html.Div(
    [method_slide_1, method_slide_2], id="met-slide", className="met-slide-offset"
)

method_header = html.Div(
    [
        html.I(className="fas fa-cube fa-lg"),
        html.H4("Methods", className="hide-label-sm"),
    ]
)

# B0 = custom_input_group(
#     prepend_label="Magnetic flux density (H₀)",
#     append_label="T",
#     value=9.4,
#     id="modal-magnetic_flux_density",
#     min=0.0,
# )
# vr = custom_input_group(
#     prepend_label="Rotor frequency (𝜈ᵣ)",
#     append_label="kHz",
#     value=0.0,
#     id="modal-rotor_frequency",
#     min=0.0,
# )
# rt = custom_input_group(
#     prepend_label="Rotor angle (θᵣ)",
#     append_label="deg",
#     value=54.735,
#     id="modal-rotor_angle",
#     max=90,
#     min=0,
# )
# count = custom_input_group(
#     prepend_label="Number of points",
#     append_label="",
#     value=1024,
#     id="modal-count",
#     min=8,
# )
# sw = custom_input_group(
#     prepend_label="Spectral width",
#     append_label="kHz",
#     value=25,
#     id="modal-spectral_width",
#     min=0.1,
# )
# rf = custom_input_group(
#     prepend_label="Reference offset",
#     append_label="kHz",
#     value=0,
#     id="modal-reference_offset",
# )
# method modal list
method_list_dropdown = dbc.Modal(
    [
        dbc.ModalHeader("Select a method"),
        dbc.ModalBody(
            [dcc.Dropdown(id="method-type", options=METHOD_OPTIONS, value=0)]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Channel", addon_type="prepend"),
                dbc.Select(options=isotope_options_list, value="1H", id="channel"),
                # B0,
                # vr,
                # rt,
                # count,
                # sw,
                # rf,
            ],
            className="container",
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Select",
                id="close-method-selection",
                color="dark",
                className="ml-auto",
                outline=True,
            )
        ),
    ],
    is_open=False,
    id="method-modal",
)


# dimension layout
dimension_body = html.Div(
    className="left-card",
    children=[
        html.Div([method_header, search_method], className="card-header"),
        method_slide,
        method_list_dropdown,
    ],
    id="method-body",
)


# callback code section =======================================================
@app.callback(
    Output("method-from-template", "data"),
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
    dims = [{"count": 512, "spectral_width": 25000, "reference_offset": 0}]
    return {
        "method": METHOD_LIST[value](
            channels=[isotope],
            # magnetic_flux_density=B0,
            # rotor_angle=rt * 3.14159265 / 180,
            # rotor_frequency=vr * 1e3,
            spectral_dimensions=dims,
        ).reduced_dict(),
        "time": int(datetime.now().timestamp() * 1000),
    }


@app.callback(
    Output("method-modal", "is_open"),
    [
        Input("add-method-button", "n_clicks"),
        Input("close-method-selection", "n_clicks"),
    ],
    [State("method-modal", "is_open")],
    prevent_initial_call=True,
)
def open_methods_model(n1, n2, state):
    return not state


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_method_json"),
    Output("new-method", "data"),
    [
        Input("apply-method-changes", "n_clicks_timestamp"),
        Input("method-from-template", "modified_timestamp"),
        Input("duplicate-method-button", "n_clicks_timestamp"),
        Input("remove-method-button", "n_clicks_timestamp"),
    ],
    [State("method-from-template", "data")],
    prevent_initial_call=True,
)


# @app.callback(
#     [Output("table-editing-simple", "data"), Output("method_edit_modal", "is_open")],
#     [Input("edit-method", "n_clicks_timestamp")],
#     [State("local-mrsim-data", "data"), State("current-method-index", "data")],
#     prevent_initial_call=True,
# )
# def render_method_table(n, data, i):
#     print("render_ table", n)
#     print(data["methods"][i])
#     table = events_table(data["methods"][i])
#     return table, True
