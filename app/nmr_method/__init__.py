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

METHOD_LIST = {
    "BlochDecaySpectrum": mt.BlochDecaySpectrum().reduced_dict(),
    "BlochDecayCTSpectrum": mt.BlochDecayCentralTransitionSpectrum().reduced_dict(),
    "MQVAS": mt.MQVAS(spectral_dimensions=[{}, {}]).reduced_dict(),
    "Custom2D": mt.Custom2D(spectral_dimensions=[{}, {}]).reduced_dict(),
}


METHOD_OPTIONS = [
    {"label": "Bloch Decay Spectrum", "value": "BlochDecaySpectrum"},
    {
        "label": "Bloch Decay Central Transition Spectrum",
        "value": "BlochDecayCTSpectrum",
    },
    {"label": "Multi-quantum variable-angle spinning", "value": "MQVAS"},
    {"label": "Custom 2D method", "value": "Custom2D"},
]

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# nmr_method parameters
def generate_parameters(n_dimensions):
    """Create a spectral dimension interface."""

    # flux_density = custom_input_group(
    #     prepend_label="Magnetic flux density (H₀)",
    #     append_label="T",
    #     value=9.4,
    #     id=f"magnetic_flux_density-0",
    #     min=0.0,
    #     debounce=True,
    # )

    # # rotor frequency
    # rotor_frequency = custom_input_group(
    #     prepend_label="Rotor frequency (𝜈ᵣ)",
    #     append_label="kHz",
    #     value=0.0,
    #     id=f"rotor_frequency-0",
    #     min=0.0,
    #     debounce=True,
    #     # list=["0", "54.7356", "30", "60", "90"],
    # )

    # create environment => widgets for
    # 1) magnetic flux density,
    # 2) rotor frequency, and
    # 3) rotor angle
    # environment_ = custom_card(text="Environment", children=environment(0, 0))

    # create spectral dimension => widgets for
    # 1) number of points,
    # 2) spectral width,
    # 3) reference offset, and
    # 4) origin offset
    spectral_dimension_ui_ = [
        custom_card(
            text=f"Spectral dimension - {i}",
            children=spectral_dimension_ui(i),
            # id=f"spec-dim-{i}",
        )
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

# method-title
method_title = html.Div(html.Label(id="method-title"), className="spin-system-title")

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
        dbc.Tab(
            label="Metadata",
            children=[method_description],
            className="tab-scroll method",
        ),
        dbc.Tab(
            label="Signal Processing",
            children=[post_simulation(1)],
            className="tab-scroll method",
        ),
    ],
    id="dimension-tabs",
)

# channels
channel = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Channel", addon_type="prepend"),
        dbc.Select(options=isotope_options_list, value="1H", id="channel"),
    ],
    className="container",
)

# method editor
method_editor = html.Div(
    [dbc.Card([method_title, channel, method_contents]), submit_button],
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
    [html.I(className="fas fa-cube"), html.H5("Methods", className="hide-label-sm")]
)

# method modal list
method_list_dropdown = dbc.Modal(
    [
        dbc.ModalHeader("Select a method"),
        dbc.ModalBody(
            [
                dcc.Dropdown(
                    id="method-type", options=METHOD_OPTIONS, value="BlochDecaySpectrum"
                )
            ]
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

# # edit in modal

# columns = [
#     {"id": "spectral_dimension", "name": "Spectral_dimension"},
#     {"id": "magnetic_flux_density", "name": "Magnetic flux density"},
#     {"id": "rotor_frequency", "name": "Rotor frequency"},
#     {"id": "rotor_angle", "name": "Rotor angle"},
# ]

# edit_in_modal = dbc.Modal(
#     [
#         dbc.ModalHeader("Edit Method"),
#         dbc.ModalBody(
#             dash_table.DataTable(
#                 id="table-editing-simple", columns=columns, editable=True,
#             )
#         ),
#     ],
#     id="method_edit_modal",
#     is_open=False,
# )

# dimension layout
dimension_body = html.Div(
    className="my-card hide-window",
    children=[
        html.Div([method_header, search_method], className="card-header"),
        method_slide,
        method_list_dropdown,
        # edit_in_modal,
    ],
    id="method-body",
)


# callback code section =======================================================


# @app.callback(
#     Output("new-method", "data"),
#     [
#         Input("apply-method-changes", "n_clicks_timestamp"),
#         Input("add-method-button", "n_clicks_timestamp"),
#         Input("duplicate-method-button", "n_clicks_timestamp"),
#     ],
#     [
#         State("channel", "value"),
#         State("count-0", "value"),
#         State("spectral_width-0", "value"),
#         State("reference_offset-0", "value"),
#         State("magnetic_flux_density-0", "value"),
#         State("rotor_frequency-0", "value"),
#         State("rotor_angle-0", "value"),
#         State("local-mrsim-data", "data"),
#     ],
# )
# def get_method_dict(*args):
#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     existing_data = ctx.states["local-mrsim-data.data"]
#     data = (
#         existing_data
#         if existing_data is not None
#         else {"name": "", "description": "", "spin-systems": [], "methods": []}
#     )
#     method_length = len(data["methods"])

#     data = {}
#     if trigger_id == "add-method-button":
#         data["data"] = BlochDecayFT(
#             dimensions=[{"count": 2048, "spectral_width": 25000}], channel="1H"
#         ).dict()
#         data["data"]["channel"] = data["data"]["channel"]["symbol"]
#         data["operation"] = "add"
#         data["index"] = method_length + 1

#     if trigger_id == "apply-method-changes":
#         states = ctx.states

#         count = states["count-0.value"]
#         spectral_width = states["spectral_width-0.value"]
#         reference_offset = states["reference_offset-0.value"]
#         magnetic_flux_density = states["magnetic_flux_density-0.value"]
#         rotor_frequency = states["rotor_frequency-0.value"]
#         rotor_angle = states["rotor_angle-0.value"]
#         channel = states["channel.value"]

#         data["data"] = BlochDecayFT(
#             dimensions=[
#                 {
#                     "count": count,
#                     "spectral_width": spectral_width * 1e3,
#                     "reference_offset": reference_offset * 1e3,
#                 }
#             ],
#             channel=channel,
#             magnetic_flux_density=magnetic_flux_density,
#             rotor_frequency=rotor_frequency * 1e3,
#             rotor_angle=rotor_angle * np.pi / 180,
#         ).dict()
#         data["data"]["channel"] = data["data"]["channel"]["symbol"]
#         data["operation"] = "modify"
#         data["index"] = method_length
#     return data


@app.callback(
    Output("method-from-template", "data"),
    [Input("close-method-selection", "n_clicks")],
    [State("method-type", "value")],
    prevent_initial_call=True,
)
def get_method_json(n, value):
    if n is None:
        raise PreventUpdate
    print(METHOD_LIST[value])
    return {
        "method": METHOD_LIST[value],
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
