# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator.dimension import ISOTOPE_DATA

from .toolbar import toolbar
from .util import blank_display
from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group

# from .toolbar import advanced_isotopomer_text_area_collapsible

ATTR_PER_SITE = 12
isotope_options_list = [{"label": key, "value": key} for key in ISOTOPE_DATA.keys()]

isotopomer_prepend_labels = {
    "alpha": "alpha (α)",
    "beta": "beta (β)",
    "gamma": "gamma (γ)",
    "zeta": "Anisotropy (ζ)",
    "eta": "Asymmetry (η)",
    "isotropic_chemical_shift": "Isotropic shift (δ)",
    "Cq": "Coupling constant (Cq)",
}

euler_angles = ["alpha", "beta", "gamma"]
base_keys = ["isotope", "isotropic_chemical_shift"]
shielding_symmertic_keys = [
    f"shielding_symmetric-{item}" for item in ["zeta", "eta", *euler_angles]
]
quadrupolar_keys = [f"quadrupolar-{item}" for item in ["Cq", "eta", *euler_angles]]
all_keys = [*base_keys, *shielding_symmertic_keys, *quadrupolar_keys]

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


def custom_fitting_input_group(prepend_label="", append_label="", **kwargs):
    """
        A custom dash bootstrap component input-group widget with a prepend-label,
        followed by an Input box, and an append-label.

        Args:
            prepend_label: A string to prepend dash-bootstrap-component Input widget.
            append_label: A string to append dash-bootstrap-component Input widget.
            kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    id_ = kwargs["id"]
    # custom collapsible into here
    group = [
        dbc.Button(
            prepend_label,
            className="input-group-prepend",
            id=f"{id_}-fit-collapse-button",
        ),
        dcc.Input(
            type="number",
            # pattern="?[0-9]*\\.?[0-9]",
            n_submit=0,
            **kwargs,
        ),
    ]
    if append_label != "":
        return html.Div(
            [
                *group,
                html.Div(
                    html.Span(append_label, className="input-group-text"),
                    className="input-group-append",
                ),
            ],
            className="input-group d-flex",
        )
    else:
        return html.Div(group, className="input-group p1 d-flex")


def custom_input_group_callable(prepend_label="", append_label="", **kwargs):
    """
        A custom dash bootstrap component input-group widget with a prepend-label,
        followed by an Input box, and an append-label.

        Args:
            prepend_label: A string to prepend dash-bootstrap-component Input widget.
            append_label: A string to append dash-bootstrap-component Input widget.
            kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    # id_ = kwargs["id"]
    custom_fitting_input_group(prepend_label, append_label, **kwargs)

    # @app.callback(
    #     Output("local-isotopomers-data", "data"),
    #     [Input(f"{id_}", "value")],  # id belongs to the input field
    #     [State("local-isotopomers-data", "data")],
    # )
    # def update_isotopomers_data(value, local_isotopomer_data):
    #     key = id_.split("_")[1].replace("%", "."))
    #     local_isotopomer_data[key] = value
    #     return local_isotopomer_data


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
                prepend_label=isotopomer_prepend_labels[key],
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
                prepend_label=isotopomer_prepend_labels[key],
                append_label=value,
                id=f"{id_label}-{key}",
                debounce=True,
            )
        )
    lst_button = dbc.Button(
        f"Euler Angles", id=f"{id_label}-orientation-button", size="sm", outline=True
    )

    lst_collapsible = dbc.Collapse(
        dbc.Card(
            [
                html.Div(
                    [html.P(f"{id_label.replace('_',' ')}"), lst_button],
                    className="my-sub-card-title",
                ),
                html.Div(feature_input_fields),
                dbc.Collapse(
                    orientation_input_fields,
                    id=f"{id_label}-orientation-collapse",
                    is_open=False,
                ),
            ],
            className="my-sub-card",
        ),
        id=f"{id_label}-feature-collapse",
        is_open=True,
    )

    @app.callback(
        Output(f"{id_label}-orientation-collapse", "is_open"),
        [Input(f"{id_label}-orientation-button", "n_clicks")],
        [
            State(f"{id_label}-orientation-collapse", "is_open"),
            *[State(f"{id_label}-{key}", "value") for key in feature_dict.keys()],
        ],
    )
    def toggle_orientation_collapsible(n, is_open, attribute_1, attribute_2):
        # print("toggle_orientation", attribute_1, attribute_2)
        # if attribute_1 is None or attribute_2 is None:
        #     return False
        if n is None:
            raise PreventUpdate

        return not is_open

    # @app.callback(
    #     Output(f"{id_label}-feature-collapse", "is_open"), [Input("isotope", "value")]
    # )
    # def hide_quad(isotope):
    #     if id_label != "quadrupolar" or isotope is None:
    #         raise PreventUpdate
    #     return False if ISOTOPE_DATA[isotope]["spin"] == 1 else True

    return lst_collapsible


def populate_key_value_from_object(object_dict):
    lst = []

    for key, value in object_dict.items():
        if isinstance(object_dict[key], dict):
            lst.append(feature_orientation_collapsible(object_dict[key], key))
        elif key == "isotope":
            lst.append(
                dbc.InputGroup(
                    [
                        dbc.InputGroupAddon("Isotope", addon_type="prepend"),
                        dbc.Select(options=isotope_options_list, value=value, id=key),
                    ]
                )
            )
        else:
            lst.append(
                html.Div(
                    [
                        custom_input_group(
                            prepend_label=isotopomer_prepend_labels[key],
                            append_label=value,
                            value="",
                            id=key,
                            debounce=True,
                        ),
                        # fitting_collapsible(key, value, identity=key),
                    ]
                )
            )
    return html.Div(lst, className="collapsible-body-control form")


lst = populate_key_value_from_object(default_unit)
widgets = dbc.Tab(label=f"Site", children=lst, className="tab-scroll")

# isotopomer abundance
isotopomer_abundance_field = custom_input_group(
    append_label="%",
    prepend_label="Abundance",
    placeholder="Isotopomer abundance",
    id="isotopomer-abundance",
    debounce=True,
    max=100,
    min=0,
)

# metadata
isotopomer_name_field = custom_input_group(
    prepend_label="Name",
    input_type="text",
    placeholder="Add name",
    value="Isotopomer Name",
    id="isotopomer-name",
    debounce=True,
)

isotopomer_description_field = html.Div(
    [
        html.Label("Description"),
        dbc.Textarea(placeholder="Add description ... ", id="isotopomer-description"),
    ]
)

metadata = dcc.Tab(
    label="Metadata",
    children=html.Div(
        [isotopomer_name_field, isotopomer_description_field], className="p-2"
    ),
)

# spin transition
transition = dcc.Dropdown(
    value=None,
    options=[],
    multi=True,
    id="isotopomer-transitions",
    searchable=True,
    clearable=False,
)
transition_group = html.Label("Spin transition")
transition_tab = dcc.Tab(
    label="Properties",
    children=html.Div([transition_group, transition], className="p-2"),
)

# isotopomer-title
isotopomer_title = html.Div(
    [
        html.Label(id="isotopomer-title"),
        custom_button(text="Apply", id="apply-isotopomer-changes"),
    ],
    className="input-text-group",
)


@app.callback(
    Output("isotopomer-title", "children"), [Input("isotopomer-name", "value")]
)
def update_isotopomer_title(value):
    value = value if value is not None else "Name"
    return value


isotopomer_edit_button = custom_button(
    icon_classname="fas fa-pencil-alt",
    id="edit_isotopomer",
    tooltip="Edit",
    outline=True,
    color="dark",
)


@app.callback(
    [Output("slide", "className"), Output("edit_isotopomer", "active")],
    [Input("edit_isotopomer", "n_clicks")],
    [State("slide", "className")],
)
def toggle_classname(n, previous_class):
    if n is None:
        raise PreventUpdate
    if previous_class == "slide":
        return ["slide-offset", True]
    return ["slide", False]


# isotopomer read-only section
# By default, display a custom screen so that the user doesn't see a blank card.
# See blank_dispaly function for details.
isotopomer_read_only = html.Div(blank_display, id="isotopomer-read-only")


# isotopomer section
isotopomer_form = dbc.Collapse(
    html.Div(
        [
            html.Div(
                [isotopomer_title, isotopomer_abundance_field],
                className="collapsible-body-control",
            ),
            dbc.Tabs([widgets, metadata]),
        ],
        id="isotopomer-form-content",
        className="active",
    ),
    id="isotopomer_form-collapse",
    is_open=True,
)


# @app.callback(
#     [
#         Output("json-file-editor-collapse", "is_open"),
#         Output("json-file-editor-button", "active"),
#         Output("isotopomer_form-collapse", "is_open"),
#     ],
#     [Input("json-file-editor-button", "n_clicks")],
#     [State("json-file-editor-button", "active")],
# )
# def toggle_json_file_editor_collapse(n, active):
#     """Callback for toggling collapsible json editor."""
#     if n is None:
#         raise PreventUpdate
#     if active:
#         return [False, False, True]
#     return [True, True, False]


# slides
slide_1 = html.Div(isotopomer_read_only, className="slider1")
slide_2 = html.Div(
    [
        # advanced_isotopomer_text_area_collapsible,
        isotopomer_form
    ],
    className="slider2",
)
slide = html.Div([slide_1, slide_2], id="slide", className="slide-offset")

# Isotopomer layout
isotopomer_body = html.Div(
    className="my-card",
    children=[
        html.Div(
            [
                html.H4("Isotopomers", id="isotopomer-card-title"),
                isotopomer_edit_button,
            ],
            className="card-header",
        ),
        html.Div(className="color-gradient-2"),
        html.Div(toolbar),
        slide,
    ],
    id="isotopomer-body",
)

isotopomer_body_card = html.Div(isotopomer_body, id="isotopomer-card-body")


# callback code section =======================================================

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_json"),
    Output("new-json", "data"),
    [
        Input("apply-isotopomer-changes", "n_clicks_timestamp"),
        Input("add-isotopomer-button", "n_clicks_timestamp"),
        Input("duplicate-isotopomer-button", "n_clicks_timestamp"),
        Input("trash-isotopomer-button", "n_clicks_timestamp"),
    ],
)
