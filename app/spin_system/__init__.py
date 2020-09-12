# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator.spin_system.isotope import ISOTOPE_DATA

from .toolbar import search_spin_system
from .utils import blank_display
from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_card
from app.custom_widgets import custom_input_group

__author__ = ["Deepansh J. Srivastava", "Maxwell C. Venetos"]
__email__ = ["srivastava.89@osu.edu", "venetos.5@buckeyemail.osu.edu"]

isotope_options_list = [{"label": key, "value": key} for key in ISOTOPE_DATA.keys()]

spin_system_prepend_labels = {
    "alpha": "alpha (α)",
    "beta": "beta (β)",
    "gamma": "gamma (γ)",
    "zeta": "Anisotropy (ζ)",
    "eta": "Asymmetry (η)",
    "isotropic_chemical_shift": "Isotropic shift (δ)",
    "Cq": "Coupling constant (Cq)",
}

# euler_angles = ["alpha", "beta", "gamma"]
# base_keys = ["isotope", "isotropic_chemical_shift"]
# shielding_symmertic_keys = [
#     f"shielding_symmetric-{item}" for item in ["zeta", "eta", *euler_angles]
# ]
# quadrupolar_keys = [f"quadrupolar-{item}" for item in ["Cq", "eta", *euler_angles]]
# all_keys = [*base_keys, *shielding_symmertic_keys, *quadrupolar_keys]

default_unit = {
    "isotope": None,
    "isotropic_chemical_shift": "ppm",
    "shielding_symmetric": {
        "zeta": "ppm",
        "eta": "",
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
    "quadrupolar": {
        "Cq": "MHz",
        "eta": "",
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
}


# def custom_fitting_input_group(prepend_label="", append_label="", **kwargs):
#     """
#         A custom dash bootstrap component input-group widget with a prepend-label,
#         followed by an Input box, and an append-label.

#         Args:
#             prepend_label: A string to prepend dash-bootstrap-component Input widget.
#             append_label: A string to append dash-bootstrap-component Input widget.
#             kwargs: additional keyward arguments for dash-bootstrap-component Input.
#     """
#     id_ = kwargs["id"]
#     # custom collapsible into here
#     group = [
#         dbc.Button(
#             prepend_label,
#             className="input-group-prepend",
#             id=f"{id_}-fit-collapse-button",
#         ),
#         dcc.Input(
#             type="number",
#             # pattern="?[0-9]*\\.?[0-9]",
#             n_submit=0,
#             **kwargs,
#         ),
#     ]
#     if append_label != "":
#         return html.Div(
#             [
#                 *group,
#                 html.Div(
#                     html.Span(append_label, className="input-group-text"),
#                     className="input-group-append",
#                 ),
#             ],
#             className="input-group d-flex",
#         )
#     else:
#         return html.Div(group, className="input-group p1 d-flex")


# def custom_input_group_callable(prepend_label="", append_label="", **kwargs):
#     """
#         A custom dash bootstrap component input-group widget with a prepend-label,
#         followed by an Input box, and an append-label.

#         Args:
#             prepend_label: A string to prepend dash-bootstrap-component Input widget.
#             append_label: A string to append dash-bootstrap-component Input widget.
#             kwargs: additional keyward arguments for dash-bootstrap-component Input.
#     """
#     # id_ = kwargs["id"]
#     custom_fitting_input_group(prepend_label, append_label, **kwargs)

#     # @app.callback(
#     #     Output("local-mrsim-data", "data"),
#     #     [Input(f"{id_}", "value")],  # id belongs to the input field
#     #     [State("local-mrsim-data", "data")],
#     # )
#     # def update_spin_systems_data(value, local_spin_system_data):
#     #     key = id_.split("_")[1].replace("%", "."))
#     #     local_spin_system_data[key] = value
#     #     return local_spin_system_data


def feature_orientation_collapsible(key_dict, id_label):
    feature_dict = {k: key_dict[k] for k in list(key_dict)[:2]}
    orientation_dict = {k: key_dict[k] for k in list(key_dict)[2:]}

    # zeta/eta and Cq/eta:
    feature_input_fields = []
    for key, value in feature_dict.items():
        extra_feature = {}
        if key == "eta":
            extra_feature = {"min": 0.0, "max": 1.0}

        feature_input_fields.append(
            custom_input_group(
                prepend_label=spin_system_prepend_labels[key],
                append_label=value,
                id=f"{id_label}-{key}",
                debounce=True,
                **extra_feature,
            )
        )

    orientation_input_fields = []
    for key, value in orientation_dict.items():
        orientation_input_fields.append(
            custom_input_group(
                prepend_label=spin_system_prepend_labels[key],
                append_label=value,
                id=f"{id_label}-{key}",
                debounce=True,
            )
        )
    lst_button = html.Label(
        [
            html.I(className="fas fa-chevron-down"),
            dbc.Tooltip(
                "Show/Hide Euler angles", target=f"{id_label}-orientation-button"
            ),
        ],
        id=f"{id_label}-orientation-button",
    )
    # dbc.Button(
    #     f"Euler Angles",
    #     id=f"{id_label}-orientation-button",
    #     size="sm",
    #     outline=False,
    #     color="info",
    # )

    lst_collapsible = dbc.Collapse(
        custom_card(
            text=html.Div([f"{id_label.replace('_',' ')}", lst_button]),
            children=html.Div(
                [
                    html.Div(feature_input_fields),
                    dbc.Collapse(
                        orientation_input_fields,
                        id=f"{id_label}-orientation-collapse",
                        is_open=False,
                    ),
                ],
                className="container",
            ),
        ),
        id=f"{id_label}-feature-collapse",
        is_open=True,
        # className="sub-spin-system-card",
    )

    @app.callback(
        Output(f"{id_label}-orientation-collapse", "is_open"),
        [Input(f"{id_label}-orientation-button", "n_clicks")],
        [
            State(f"{id_label}-orientation-collapse", "is_open"),
            *[State(f"{id_label}-{key}", "value") for key in feature_dict.keys()],
        ],
        prevent_initial_call=True,
    )
    def toggle_orientation_collapsible(n, is_open, attribute_1, attribute_2):
        # print("toggle_orientation", attribute_1, attribute_2)
        # if attribute_1 is None or attribute_2 is None:
        #     return False
        if n is None:
            raise PreventUpdate

        return not is_open

    return lst_collapsible


isotope_and_shift = html.Div(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Isotope", addon_type="prepend"),
                dbc.Select(options=isotope_options_list, value="1H", id="isotope"),
            ]
        ),
        custom_input_group(
            prepend_label="Isotropic shift (δ)",
            append_label="ppm",
            value="",
            id="isotropic_chemical_shift",
            debounce=True,
        ),
    ],
    className="container scroll-cards",
)


def populate_key_value_from_object(object_dict):
    lst = []
    lst.append(isotope_and_shift)
    for key in object_dict.keys():
        if isinstance(object_dict[key], dict):
            lst.append(feature_orientation_collapsible(object_dict[key], key))

    # elif key == "isotope":
    #     lst.append(
    #         dbc.InputGroup(
    #             [
    #                 dbc.InputGroupAddon("Isotope", addon_type="prepend"),
    #                 dbc.Select(options=isotope_options_list, value=value, id=key),
    #             ]
    #         )
    #     )
    # else:
    #     lst.append(
    #         html.Div(
    #             [
    #                 custom_input_group(
    #                     prepend_label=spin_system_prepend_labels[key],
    #                     append_label=value,
    #                     value="",
    #                     id=key,
    #                     debounce=True,
    #                 ),
    #                 # fitting_collapsible(key, value, identity=key),
    #             ]
    #         )
    #     )
    return html.Div(lst)


lst = populate_key_value_from_object(default_unit)
widgets = dbc.Tab(label="Site", children=lst, className="tab-scroll")

# spin-system abundance
spin_system_abundance_field = html.Div(
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

# metadata
spin_system_name_field = custom_input_group(
    prepend_label="Name",
    input_type="text",
    placeholder="Add name",
    value="Spin system Name",
    id="spin-system-name",
    debounce=True,
)

spin_system_description_field = html.Div(
    [
        html.Label("Description"),
        dbc.Textarea(
            placeholder="Add a description ... ",
            id="spin-system-description",
            debounce=True,
            style={"height": "12rem"},
        ),
    ]
)

metadata = dcc.Tab(
    label="Metadata",
    children=html.Div(
        [spin_system_name_field, spin_system_description_field],
        className="tab-scroll scroll-cards container",
    ),
)


submit_button = html.Div(
    custom_button(
        text="Submit Spin System", id="apply-spin-system-changes", color="primary"
    ),
    className="submit-button",
)

# spin-system-title
spin_system_title = html.Div(
    html.Label(id="spin-system-title"), className="spin-system-title"
)

# spin-system read-only section
# By default, display a custom screen so that the user doesn't see a blank card.
# See blank_dispaly function for details.
spin_system_read_only = html.Div(blank_display, id="spin-system-read-only")


# spin-system section
spin_system_editor = html.Form(
    [
        dbc.Card(
            [
                spin_system_title,
                spin_system_abundance_field,
                dbc.Tabs([widgets, metadata]),
            ]
        ),
        submit_button,
    ],
    id="spin-system-editor-content",
)


# slides
spin_system_slide_1 = html.Div(spin_system_read_only, className="slider1")
spin_system_slide_2 = html.Div(spin_system_editor, className="slider2")
spin_system_slide = html.Div(
    [spin_system_slide_1, spin_system_slide_2],
    id="iso-slide",
    className="iso-slide-offset",
)

spin_system_title = html.Div(
    [
        html.I(className="fac fa-spin-systems"),
        html.H5("Spin Systems", className="hide-label-sm"),
    ]
)

# Spin system layout
spin_system_body = html.Div(
    className="my-card hide-window",
    children=html.Div(
        [
            html.Div([spin_system_title, search_spin_system], className="card-header"),
            spin_system_slide,
        ]
    ),
    id="spin-system-body",
)

# Select spin-system when the respective graph is selected.
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="selected_spin_system"),
    Output("temp3", "children"),
    [Input("nmr_spectrum", "clickData")],
    [
        State("local-spin-system-index-map", "data"),
        State("decompose", "active"),
        State("select-method", "value"),
    ],
    prevent_initial_call=True,
)

# callback code section =======================================================
# app.clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="submit"),
#     Output("temp-json", "data"),
#     [Input("apply-spin-system-changes", "n_clicks_timestamp")],
# )

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_json"),
    Output("new-spin-system", "data"),
    [
        Input("apply-spin-system-changes", "n_clicks_timestamp"),
        Input("add-spin-system-button", "n_clicks_timestamp"),
        Input("duplicate-spin-system-button", "n_clicks_timestamp"),
        Input("remove-spin-system-button", "n_clicks_timestamp"),
        Input("spin-system-name", "value"),
        Input("spin-system-description", "value"),
        Input("spin-system-abundance", "value"),
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
