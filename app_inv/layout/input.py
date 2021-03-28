# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.graph import generate_graph_instance
from app.spin_system.site import isotope_options_list

# Section 1
# Input graph and fields

graph = dcc.Upload(
    generate_graph_instance(id_="INV-spectrum"),
    id="INV-upload-from-graph",
    disable_click=True,
    style_active={
        "border": "1px solid rgb(78, 196, 78)",
        "backgroundColor": "rgb(225, 255, 225)",
        "opacity": "0.75",
    },
)

radio = dbc.RadioItems(
    options=[
        {"label": "Data", "value": 0},
        {"label": "Residue", "value": 1},
    ],
    value=0,
    id="INV-input-residue",
)

transpose_button = dbc.Button("T", id="INV-transpose")

set1 = dbc.Card(
    [
        dbc.CardHeader([html.H4("Input"), transpose_button]),
        dbc.CardBody(html.Div([graph, radio])),
    ]
)

dim = [
    html.H5("Inverse dimensions"),
    dbc.Label("x"),
    custom_input_group(
        prepend_label="Count",
        append_label="",
        value=25,
        id="INV-dimension-0-count",
        min=0,
        debounce=True,
    ),
    custom_input_group(
        prepend_label="Increment",
        append_label="Hz",
        value=370,
        id="INV-dimension-0-increment",
        min=1e-9,
        debounce=True,
    ),
    dbc.Label("y"),
    custom_input_group(
        prepend_label="Count",
        append_label="",
        value=25,
        id="INV-dimension-1-count",
        min=0,
        debounce=True,
    ),
    custom_input_group(
        prepend_label="Increment",
        append_label="Hz",
        value=370,
        id="INV-dimension-1-increment",
        min=1e-9,
        debounce=True,
    ),
    custom_input_group(
        prepend_label="Supersampling",
        append_label="Hz",
        value=1,
        id="INV-supersampling",
        min=0,
        debounce=True,
    ),
]
dimensions = dbc.CardBody(dim)

kernel = [
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Type", addon_type="prepend"),
            dbc.Select(
                options=[
                    {"label": "MAF", "value": "MAF"},
                    {"label": "Sideband correlation", "value": "sideband-correlation"},
                ],
                value="sideband-correlation",
                id="INV-kernel-type",
            ),
        ],
        className="input-form",
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Channel", addon_type="prepend"),
            dbc.Select(
                options=isotope_options_list, value="29Si", id="INV-kernel-channel"
            ),
        ],
        className="input-form",
    ),
    custom_input_group(
        prepend_label="Magnetic flux density (H₀)",
        append_label="T",
        value=9.4,
        id="INV-kernel-flux",
        min=0.0,
        debounce=True,
    ),
    # custom_input_group(
    #     prepend_label="Rotor frequency (𝜈ᵣ)",
    #     append_label="Hz",
    #     value=800,
    #     id="INV-kernel-rotor_frequency",
    #     min=0.0,
    #     debounce=True,
    # ),
    custom_input_group(
        prepend_label="Rotor angle (θᵣ)",
        append_label="deg",
        value=54.735,
        id="INV-kernel-rotor_angle",
        max=90,
        min=0,
        debounce=True,
    ),
    # custom_input_group(
    #     prepend_label="Number of sidebands",
    #     append_label="",
    #     value=16,
    #     id="INV-kernel-number_of_sidebands",
    #     debounce=True,
    # ),
]
interaction = dbc.Card(
    [
        dbc.CardHeader(html.H4("Kernel")),
        html.Div([dbc.CardBody(kernel), dimensions]),
        dbc.Button("Generate kernel", id="INV-generate-kernel"),
    ]
)
input_layer = dbc.Card(
    dbc.CardBody(dbc.Row([dbc.Col(set1), dbc.Col(interaction, md=6, sm=12)]))
)
