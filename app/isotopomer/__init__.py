# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Isotopomer
from mrsimulator.dimension import ISOTOPE_DATA

from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group
from app.isotopomer.toolbar import advanced_isotopomer_text_area_collapsible
from app.isotopomer.toolbar import toolbar

# from dash.dependencies import ClientsideFunction


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

greek_list = ["eta", "alpha", "beta", "gamma"]
base_keys = ["isotope", "isotropic_chemical_shift"]
shielding_symmertic_keys = [
    f"shielding_symmetric-{item}" for item in ["zeta", *greek_list]
]
quadrupolar_keys = [f"quadrupolar-{item}" for item in ["Cq", *greek_list]]
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
    #     key = id_.split("_")[1].replace("%", ".")
    #     print(key)
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
        if attribute_1 is None or attribute_2 is None:
            return False
        if n is None:
            raise PreventUpdate

        return not is_open

    @app.callback(
        Output(f"{id_label}-feature-collapse", "is_open"), [Input("isotope", "value")]
    )
    def hide_quad(isotope):
        if id_label != "quadrupolar" or isotope is None:
            raise PreventUpdate
        return False if ISOTOPE_DATA[isotope]["spin"] == 1 else True

    return lst_collapsible


def populate_key_value_from_object(object_dict):
    lst = []

    for key, value in object_dict.items():
        print("initialize", key, value)
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
    # html.Div(lst_button, className="button-toolbar"),
    # ]


lst = populate_key_value_from_object(default_unit)
widgets = dbc.Tab(label=f"Site", children=lst, className="tab-scroll")

isotopomer_dropdown = dcc.Dropdown(
    value=None,
    options=[],
    multi=False,
    id="isotopomer-dropdown",
    searchable=True,
    clearable=False,
)

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
isotopomer_read_only = html.Div(
    id="isotopomer-read-only"
)  # dcc.Markdown(id="isotopomer-read-only",)
# isotopomer section
isotopomer_form = dbc.Collapse(
    html.Div(
        [
            html.Div(
                [isotopomer_title, isotopomer_abundance_field],
                className="collapsible-body-control",
            ),
            dbc.Tabs([widgets, transition_tab, metadata]),
        ],
        id="isotopomer-form-content",
        className="active",
    ),
    id="isotopomer_form-collapse",
    is_open=True,
)


@app.callback(
    [
        Output("json-file-editor-collapse", "is_open"),
        Output("json-file-editor-button", "active"),
        Output("isotopomer_form-collapse", "is_open"),
    ],
    [Input("json-file-editor-button", "n_clicks")],
    [State("json-file-editor-button", "active")],
)
def toggle_json_file_editor_collapse(n, active):
    """Callback for toggling collapsible json editor."""
    if n is None:
        raise PreventUpdate
    if active:
        return [False, False, True]
    return [True, True, False]


# slides
slide_1 = html.Div(isotopomer_read_only, className="slider1")
slide_2 = html.Div(
    [
        html.Div(toolbar),
        dbc.Col(["Select Isotopomer", isotopomer_dropdown]),
        advanced_isotopomer_text_area_collapsible,
        dcc.Loading(isotopomer_form),
    ],
    className="slider2",
)
slide = html.Div([slide_1, slide_2], id="slide", className="slide")

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
        slide,
    ],
    id="isotopomer-body",
)

isotopomer_body_card = html.Div(isotopomer_body, id="isotopomer-card-body")


# callback code section =======================================================
def extract_site_dictionary_from_dash_triggers(states):
    """
    Extract a site dictionary from dash states/triggers.

    Arg:
        states: A list of dash state/trigger dictionaries where each dictionary is
                of form {'dash_id.value': 'value'}

    We define the dash_id as `key1-key2`, which makes it easy to generate
    the site dictionary object following site[key1][key2] = value
    """
    site = {
        "isotope": None,
        "isotropic_chemical_shift": None,
        "shielding_symmetric": {},
        "quadrupolar": {},
    }
    for item in all_keys:
        value = states[f"{item}.value"]
        if value is not None:
            keys = item.split("-")

            # when only one key is present, use site[key1] = value
            if len(keys) == 1:
                site[keys[0]] = value

            # when two keys are present, use site[key1][key2] = value
            if len(keys) == 2:
                site[keys[0]][keys[1]] = value

    # Remove any instance of dict key with value as {}
    site = dict([(k, v) for k, v in site.items() if v != {}])

    # The input may contain value form all fields, some of which might not accurate.
    # Before returning the site dict, check if the site isotope is quadrupolar. If
    # false, delete the quadrupolar key, else, convert Cq from Hz to MHz.
    isotope = states["isotope.value"]
    if "quadrupolar" in site.keys():
        if ISOTOPE_DATA[isotope]["spin"] == 1:
            del site["quadrupolar"]  # delete quadrupolar dict for spin 1/2
        else:
            site["quadrupolar"]["Cq"] *= 1.0e6  # Cq in MHz
    return site


def extract_isotopomer_UI_field_values_from_dictionary(site):
    """
    Extract the values from an ordered list of site objects. the extracted values are
    sent to the dash Output.
    The order of the optput trigger values follows the order defined by the variable
    `all_keys`.
    """
    root_keys = site.keys()

    trigger_values = [None for _ in range(ATTR_PER_SITE)]
    index = 0
    for ids in all_keys:
        keys = ids.split("-")

        # when only one key is present, use the value of site[site_index][key1]
        if len(keys) == 1:
            k0 = keys[0]
            trigger_values[index] = site[k0] if k0 in root_keys else None

        # when two keys are present, use the value of site[site_index][key1][key2]
        if len(keys) == 2:
            k0, k1 = keys
            if k0 in root_keys:
                if site[k0] is not None:
                    trigger_values[index] = (
                        site[k0][k1] if k1 in site[k0].keys() else None
                    )
        index += 1

    # convert trigger index 7 => quadrupolar coupling constant from Hz to MHz.
    if trigger_values[7] is not None:
        trigger_values[7] /= 1.0e6
    return trigger_values


@app.callback(
    [
        *[Output(item, "value") for item in all_keys],
        Output("isotopomer-abundance", "value"),
        Output("isotopomer-name", "value"),
        Output("isotopomer-description", "value"),
        Output("isotopomer-transitions", "options"),
    ],
    [Input("isotopomer-dropdown", "value"), Input("json-file-editor-button", "active")],
    [State("local-isotopomers-data", "data")],
)
def populate_isotopomer_fields(index, is_advanced_editor_open, local_isotopomer_data):
    """Extract the values from the local isotopomer data and populate the input fields
    in the isotopomer UI corresponding to the dropdown selection index."""
    # The argument `is_advanced_editor_open` is for checking if the fields are in view.
    # If this argument is true, the advanced editor is open and, therefore, the
    # isotopomer UI fields are hidden. In this case, we want to prevent any updates
    # from the `populate_isotopomer_fields` (this function) to improve the performance.
    print("index in mass", index)
    if is_advanced_editor_open:
        raise PreventUpdate
    if None in [local_isotopomer_data, index]:
        raise PreventUpdate

    # Get the isotopomer at `index`, where index is the selection from the dropdown
    # menu.
    isotopomer = local_isotopomer_data["isotopomers"][index]

    # Updates for the site tab
    # ------------------------
    # Extract the UI input field values from the site a index zero of the isotopomer.
    # At the moment, we only support one site per isotopomer.
    values = extract_isotopomer_UI_field_values_from_dictionary(isotopomer["sites"][0])

    # Updates for the metadata tab
    # ----------------------------
    # Get the name, description, and abundance from the isotopomer
    name = isotopomer["name"]
    description = isotopomer["description"]
    abundance = isotopomer["abundance"] if "abundance" in isotopomer.keys() else 100

    # Updates for the transition tab
    # ------------------------------
    # Get the list of all transitions from the isotopomer
    transition_objects = Isotopomer(**isotopomer).all_transitions
    transition_options = [{"label": "Default Δm=-1", "value": 0}] + [
        {"label": str(item), "value": str(item)} for item in transition_objects
    ]

    return [*values, abundance, name, description, transition_options]


@app.callback(
    Output("new-json", "data"),
    [Input("apply-isotopomer-changes", "n_clicks")],
    [
        *[State(item, "value") for item in all_keys],
        State("local-isotopomers-data", "data"),
        State("isotopomer-dropdown", "value"),
        State("isotopomer-name", "value"),
        State("isotopomer-description", "value"),
        State("isotopomer-abundance", "value"),
    ],
)
def create_json(n, *args):
    """Generate a python dict object from the input fields in the isotopomers UI"""
    if n is None:
        raise PreventUpdate

    states = dash.callback_context.states
    data = states["local-isotopomers-data.data"]
    if data is None:
        raise PreventUpdate

    print("creating json")

    # Extract the current isotopomer index, and get the respective isotopomer.
    isotopomer_index = states["isotopomer-dropdown.value"]
    isotopomer = data["isotopomers"][isotopomer_index]

    # Extract name and description information from the states and update the
    # isotopomer dict
    isotopomer["name"] = states["isotopomer-name.value"]
    isotopomer["description"] = states["isotopomer-description.value"]

    # Extract site information from the states
    site = extract_site_dictionary_from_dash_triggers(states)

    # At present, we only support one site per isotopomer. Assign the above site
    # to the index zero of sites array.
    isotopomer["sites"][0] = site

    # Extract the abundance information and update the isotopomer
    isotopomer["abundance"] = states["isotopomer-abundance.value"]

    return isotopomer
