# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.sims.graph import generate_graph_instance
from app.sims.spin_system.site import isotope_options_list

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

input_plot = dbc.Card(
    [
        dbc.CardHeader([html.H4("Input"), transpose_button]),
        dbc.CardBody(html.Div([graph])),  # , radio])),
    ]
)


def dim_parameters(i, label):
    label = dbc.Label(label)
    count = custom_input_group(
        prepend_label="Count",
        append_label="",
        value=25,
        id=f"INV-dimension-{i}-count",
        min=0,
        debounce=True,
    )
    increment = custom_input_group(
        prepend_label="Increment",
        append_label="Hz",
        value=370,
        id=f"INV-dimension-{i}-increment",
        min=1e-9,
        debounce=True,
    )
    return dbc.Col([label, count, increment], md=6)


def supersampling():
    return custom_input_group(
        prepend_label="Supersampling",
        append_label="Hz",
        value=1,
        id="INV-supersampling",
        min=0,
        debounce=True,
    )


def inverse_dimensions():
    label = html.H5("Inverse dimension grid")
    dim_x = dim_parameters(0, "x")
    dim_y = dim_parameters(1, "y")
    content = dbc.Row([dim_x, dim_y])
    return dbc.CardBody([label, content, supersampling()])


# Kernel
def kernel_type():
    label = dbc.InputGroupAddon("Type", addon_type="prepend")
    kernel_options = [
        {"label": "MAF", "value": "MAF"},
        {"label": "Sideband correlation", "value": "sideband-correlation"},
    ]
    selection = dbc.Select(
        options=kernel_options, value="sideband-correlation", id="INV-kernel-type"
    )
    return dbc.InputGroup([label, selection], className="input-form")


def channel():
    label = dbc.InputGroupAddon("Channel", addon_type="prepend")
    selection = dbc.Select(
        options=isotope_options_list, value="29Si", id="INV-kernel-channel"
    )
    return dbc.InputGroup([label, selection], className="input-form")


def magnetic_flux_density():
    return custom_input_group(
        prepend_label="Magnetic flux density B₀)",
        append_label="T",
        value=9.4,
        id="INV-kernel-flux",
        min=0.0,
        debounce=True,
    )


def rotor_angle():
    return custom_input_group(
        prepend_label="Rotor angle (θᵣ)",
        append_label="deg",
        value=54.735,
        id="INV-kernel-rotor_angle",
        max=90,
        min=0,
        debounce=True,
    )


# custom_input_group(
#     prepend_label="Rotor frequency (𝜈ᵣ)",
#     append_label="Hz",
#     value=800,
#     id="INV-kernel-rotor_frequency",
#     min=0.0,
#     debounce=True,
# ),
# custom_input_group(
#     prepend_label="Number of sidebands",
#     append_label="",
#     value=16,
#     id="INV-kernel-number_of_sidebands",
#     debounce=True,
# ),


def kernel():
    return dbc.CardBody(
        [kernel_type(), channel(), magnetic_flux_density(), rotor_angle()]
    )


def inversion():
    return dbc.Card(
        [
            # dbc.CardHeader(html.H4("Parameters")),
            custom_input_group(
                prepend_label="l1 weight λ",
                append_label="",
                value=1e-7,
                id="INV-l1",
                min=0,
                debounce=True,
            ),
            custom_input_group(
                prepend_label="l2 weight α",
                append_label="",
                value=1e-6,
                id="INV-l2",
                min=0,
                debounce=True,
            ),
            dbc.Button("Invert", id="INV-solve"),
        ]
    )


def input_panel_1():
    label = dbc.CardHeader(html.H4("Parameters"))
    boby = html.Div([kernel(), inverse_dimensions()])
    button = dbc.Button("Generate kernel", id="INV-generate-kernel")
    inv = inversion()
    tab1 = dbc.Tab(label="Kernel", children=[boby, button])
    tab2 = dbc.Tab(label="Inversion parameters", children=inv)

    return dbc.Card([label, dbc.Tabs([tab1, tab2])])


def output_graph():
    graph_output = generate_graph_instance(id_="INV-output")
    graph_output.config["scrollZoom"] = True

    label = dbc.CardHeader(html.H4("Output"))
    body = dcc.Loading(dbc.CardBody(graph_output), type="dot")
    return dbc.Card([label, body])


def ui():
    graph1 = dbc.Col(input_plot)
    panel = dbc.Col(input_panel_1(), md=4, sm=12)
    graph2 = dbc.Col(output_graph(), md=4, sm=12)
    row = dbc.Row([graph1, panel, graph2])

    return dbc.Card(dbc.CardBody(row))


input_layer = ui()
