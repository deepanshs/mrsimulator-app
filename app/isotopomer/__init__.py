# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import no_update
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator import Dimension
from mrsimulator import Isotopomer
from mrsimulator.dimension import ISOTOPE_DATA

from app.app import app
from app.custom_widgets import custom_input_group
from app.isotopomer.toolbar import advanced_isotopomer_text_area_collapsible
from app.isotopomer.toolbar import toolbar

# from dash.dependencies import ClientsideFunction

# from app.isotopomer.draft import filter_isotopomer_list

# from app.custom_widgets import custom_slider

N_SITE = 1
ATTR_PER_SITE = 12
isotope_options_list = [{"label": key, "value": key} for key in ISOTOPE_DATA.keys()]

isotopomer_prepend_labels = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "zeta": "anisotropy (ζ)",
    "eta": "asymmetry (η)",
    "isotropic_chemical_shift": "isotropic chemical shift (δ)",
    "Cq": "coupling constant (Cq)",
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
        "Cq": "Hz",
        "eta": "",
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
}

# def custom_form_group(prepend_label="", **kwargs):
#     if "step" not in kwargs.keys():
#         kwargs["step"] = 1e-5
#     return dbc.InputGroup(
#         [
#             dbc.Label(
#                 prepend_label,
#                 className="append-addon form-control .form-control-sm, tree-control",
#                 size="sm",
#                 style={"width": "30%"},
#             ),
#             dbc.Input(
#                 type="text",
#                 bs_size="sm",
#                 className=("append-addon form-control .form-control-sm ",
#                           "tree-control tree-control-input"),
#                 **kwargs,
#             ),
#         ]
#     )


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
            className="form-control",
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


def feature_orientation_collapsible(key_dict, id_label, site_number):
    # print('old id', id_old)
    # print('id label', id_label)
    feature_dict = {k: key_dict[k] for k in list(key_dict)[:2]}
    orientation_dict = {k: key_dict[k] for k in list(key_dict)[2:]}

    # zeta/eta and Cq/eta:
    feature_input_fields = []
    for key, value in feature_dict.items():
        feature_input_fields.append(
            custom_input_group(
                prepend_label=isotopomer_prepend_labels[key],
                append_label=value,
                id=f"{site_number}-{id_label}-{key}",
                debounce=True,
            )
        )

    orientation_input_fields = []
    for key, value in orientation_dict.items():
        orientation_input_fields.append(
            custom_input_group(
                prepend_label=isotopomer_prepend_labels[key],
                append_label=value,
                id=f"{site_number}-{id_label}-{key}",
                debounce=True,
            )
        )
    lst_button = dbc.ButtonGroup(
        [
            dbc.Button(f"{id_label[0]}", id=f"{id_label}-button", disabled=False),
            dbc.Button(
                f"Orientation", id=f"{id_label}-orientation-button", disabled=False
            ),
        ],
        size="sm",
        className="mr-1",
    )

    lst_collapsible = html.Div(
        [
            dbc.Collapse(
                dbc.Card(
                    [
                        html.P(
                            f"{id_label.replace('_',' ')}",
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
        ]
    )

    # @app.callback(
    #     [
    #         Output(f"{id_label}-feature-collapse", "is_open"),
    #         Output(f"{id_label}-orientation-collapse", "is_open"),
    #     ],
    #     [
    #         Input(f"{id_label}-button", "n_clicks"),
    #         Input(f"{id_label}-orientation-button", "n_clicks"),

    #     ],
    #     [
    #         State(f"0-isotope", "value"),
    #         State(f"{id_label}-button", "children"),
    #         *[
    #             State(f"{site_number}-{id_label}-{key}", "value")
    #             for key in feature_dict.keys()
    #         ],
    #         State(f"{id_label}-feature-collapse", "is_open"),
    #         State(f"{id_label}-orientation-collapse", "is_open"),
    #     ],
    # )
    # def toggle_feature_buttons(
    #     n1, n2, isotope, feature_label, data1, data2, feature_active, orientation_active
    # ):
    #     # Closes quad buttons if non-quad nuclei. A separate callback will disable
    #     # the buttons
    #     print("in toggle", dash.callback_context.triggered)
    #     dim = Dimension(isotope=isotope, spectral_width=50000)
    #     if dim.spin == 0.5:
    #         return True, False

    #     ctx = dash.callback_context
    #     if not ctx.triggered:
    #         return [no_update, no_update]

    #     button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    #     # toggles buttons
    #     if button_id == f"{id_label}-button":
    #         return feature_active, orientation_active
    #     if button_id == f"{id_label}-orientation-button":
    #         return True, not orientation_active

    #     if None in [data1, data2]:  # and feature_active == True:
    #         return True, False

    #     return True, False

    @app.callback(
        Output(f"{id_label}-orientation-button", "disabled"),
        [
            *[
                Input(f"{site_number}-{id_label}-{key}", "value")
                for key in feature_dict.keys()
            ],
            Input(f"{id_label}-button", "disabled"),
        ],
    )
    def freeze_orientation_button(*args):
        print(f"My data for {id_label}", args[0], args[1])
        if args[0] is None or args[1] is None:
            return True
        if args[-1]:
            return True
        return False

    return [lst_collapsible, lst_button]


@app.callback(Output(f"quadrupolar-button", "disabled"), [Input("0-isotope", "value")])
def freeze_quad_button(isotope):
    dim = Dimension(isotope=isotope, spectral_width=50000)
    if dim.spin == 0.5:
        return True
    return False


def populate_key_value_from_object(object_dict, id_old):
    lst = []
    lst_button = []
    for key, value in object_dict.items():  # keys():
        id_new = f"{id_old}-{key}"
        if isinstance(object_dict[key], dict):
            feature_collapsible, feature_button = feature_orientation_collapsible(
                object_dict[key], key, id_old
            )
            lst.append(feature_collapsible)
            lst_button.append(feature_button)
        else:
            if key == "isotope":
                lst.append(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Isotope", addon_type="prepend"),
                            dbc.Select(
                                options=isotope_options_list, value=value, id=id_new
                            ),
                        ],
                        className="mb-0",
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
                                id=id_new,
                                debounce=True,
                            ),
                            # fitting_collapsible(key, value, identity=id_new),
                        ]
                    )
                )
    return [
        html.Div(lst, className="collapsible-body-control form"),
        html.Div(lst_button),
    ]


lst, button = populate_key_value_from_object(default_unit, "0")
widgets = dbc.Tab(label=f"Site", children=[button, lst], className="tab-scroll")

isotopomer_dropdown = dcc.Dropdown(
    value=None,
    options=[],
    multi=False,
    id="isotopomer-dropdown",
    searchable=True,
    clearable=False,
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

isotopomer_name_field = custom_input_group(
    prepend_label="Name",
    input_type="text",
    placeholder="Isotopomer name",
    id="isotopomer-name",
    debounce=True,
)

isotopomer_description_field = custom_input_group(
    prepend_label="Description",
    input_type="text",
    placeholder="Isotopomer description ... ",
    id="isotopomer-description",
    debounce=True,
)

isotopomer_abundance_field = custom_input_group(
    prepend_label="Abundance",
    placeholder="Isotopomer abundance",
    id="isotopomer-abundance",
    debounce=True,
)

isotopomer_form = dbc.Collapse(
    html.Div(
        [
            html.Div(
                [
                    isotopomer_name_field,  # isotopomer name
                    isotopomer_description_field,  # isotopomer description
                    isotopomer_abundance_field,  # isotopomer abundance
                ],
                className="collapsible-body-control",
            ),
            dbc.Tabs([widgets, transition_tab]),
        ],
        id="isotopomer-form-content",
        className="inactive",
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


# Isotopomer layout
isotopomer_body = html.Div(
    className="my-card",
    children=[
        html.Div(
            html.H4("Isotopomers", id="isotopomer-card-title"), className="card-header"
        ),
        html.Div(className="color-gradient-2"),
        html.Div(toolbar),
        dbc.Col(["Select Isotopomer", isotopomer_dropdown]),
        advanced_isotopomer_text_area_collapsible,
        isotopomer_form,
    ],
    id="isotopomer-body",
)

isotopomer_body_card = html.Div(
    isotopomer_body, id="isotopomer-card-body", className="h-100"
)


# callback code section =======================================================
def extract_site_dictionary_from_dash_triggers(dash_triggers):
    """
    Extract a list of site dictionaries from the dash_id. This method does not
    depend on how the trigger dash_id are ordered.

    Arg:
        dash_trigger: A list of dash trigger dictionaries where each dictionary is
                of form {'dash_id.value': 'value'}

    We define the dash_id as `site_index-key1-key2`, which makes it easy to generate
    the site dictionary objects following
                site[site_index][key1][key2] = value
    """
    site = {
        "isotope": None,
        "isotropic_chemical_shift": None,
        "shielding_symmetric": {},
        "quadrupolar": {},
    }
    for key, value in dash_triggers.items():
        if value is not None:
            group = key.split(".")[0].split("-")
            _, keys = int(group[0]), group[1:]

            # when only one key is present, use site[key1] = value
            if len(keys) == 1:
                site[keys[0]] = value

            # when two keys are present, use site[key1][key2] = value
            if len(keys) == 2:
                site[keys[0]][keys[1]] = value
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

    return trigger_values


# app.clientside_callback(
#     ClientsideFunction(
#         namespace="clientside", function_name="populate_isotopomer_fields"
#     ),
#     [*[Output(f"{i}-{item}", "value") for i in range(N_SITE) for item in all_keys]],
#     [Input("isotopomer-dropdown", "value"),
#       Input("json-file-editor-button", "active")],
#     [State("local-isotopomers-data", "data")],
# )


@app.callback(
    [
        *[Output(f"0-{item}", "value") for item in all_keys],
        Output("isotopomer-abundance", "value"),
        Output("isotopomer-name", "value"),
        Output("isotopomer-description", "value"),
        Output("isotopomer-form-content", "className"),
        Output("isotopomer-transitions", "options"),
    ],
    [Input("isotopomer-dropdown", "value"), Input("json-file-editor-button", "active")],
    [State("local-isotopomers-data", "data")],
)
def populate_isotopomer_fields(index, is_advanced_editor_open, local_isotopomer_data):
    """Extract the values from the local isotopomer data and populate the input fields
    in the isotopomer UI. """
    # The argument `is_advanced_editor_open` is for checking if the fields are in view.
    # If this argument is true, the advanced editor is open and, therefore, the
    # isotopomer UI fields are hidden. In this case, we want to prevent any updates
    # from the `populate_isotopomer_fields` (this function) to improve the performance.
    print("index in mass", index, type(index))
    if is_advanced_editor_open:
        raise PreventUpdate
    if None in [local_isotopomer_data, index]:
        return [*[no_update for _ in range(ATTR_PER_SITE + 3)], "inactive", no_update]
    # if index is None:
    #     return [*[no_update for _ in range(ATTR_PER_SITE + 3)], "inactive", no_update]

    isotopomer = local_isotopomer_data["isotopomers"][index]
    values = extract_isotopomer_UI_field_values_from_dictionary(isotopomer["sites"][0])

    name = isotopomer["name"]
    description = isotopomer["description"]
    abundance = isotopomer["abundance"] if "abundance" in isotopomer.keys() else 1

    transition_objects = Isotopomer(**isotopomer).all_transitions
    transition_options = [{"label": "Default Δm=-1", "value": 0}] + [
        {"label": str(item), "value": str(item)} for item in transition_objects
    ]
    return [*values, abundance, name, description, "active", transition_options]


# @app.callback(
#     Output("shielding_symmetric", "data"),
#     [
#         Input(f"{i}-shielding_symmetric-{item}", "value")
#         for i in range(N_SITE)
#         for item in ["zeta", "eta"]
#     ],
# )
# def check_for_shielding_symmetric_pair(*args):
#     print("check_for_shielding_symmetric_pair")
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         raise PreventUpdate

#     inputs = dash.callback_context.inputs
#     print(inputs)
#     val = check_for_pairs(["zeta", "eta"], inputs)
#     print("check shielding", val)
#     return [f"{i} ppm" for i in val[0::2]]


# def check_for_pairs(pair, inputs):
#     val = []
#     for i in range(N_SITE):
#         zeta_or_Cq = inputs[f"{i}-shielding_symmetric-{pair[0]}.value"]
#         eta = inputs[f"{i}-shielding_symmetric-{pair[1]}.value"]
#         if zeta_or_Cq not in [None, ""] and eta not in [None, ""]:
#             raise PreventUpdate
#         val += [zeta_or_Cq, eta]
#     return val

orientations = ["alpha", "beta", "gamma"]
shielding_pairs = ["zeta", "eta"]
quad_pairs = ["Cq", "eta"]
root_options = ["name", "description", "abundance"]


def check_groups(states, k0, k1):
    # check if the value for all orientations is given.
    # 1) get the state values of the orientations,
    # 2) stop the update if
    #   a) the trigger originated from orientation field, and
    #   b) any of the orientation state value is None, and
    #   c) not all orientation state value are None.
    orientation_group = [states[f"0-{k0}-{_}.value"] for _ in orientations]
    print("orientation group", orientation_group)
    if (
        k1 in orientations
        and None in orientation_group
        and orientation_group != [None, None, None]
    ):
        print("stop because not all alpha, beta, gamma is given.")
        raise PreventUpdate

    if k0 == "shielding_symmetric":
        shielding_group = [states[f"0-{k0}-{_}.value"] for _ in shielding_pairs]
        print("shielding group", shielding_group)
        if (
            k1 in shielding_pairs
            and None in shielding_group
            and shielding_group != [None, None]
        ):
            print("stop because not either zeta or eta is missing.")
            raise PreventUpdate
    if k0 == "quadrupolar":
        quad_group = [states[f"0-{k0}-{_}.value"] for _ in quad_pairs]
        print("quad group", quad_group)
        if k1 in quad_pairs and None in quad_group and quad_group != [None, None]:
            print("stop because not either Cq or eta is missing.")
            raise PreventUpdate


def if_value_change(trigger_site, trigger_value, keys, states):
    empty = ["", None]
    root_keys = trigger_site.keys()
    k0 = keys[0]
    if len(keys) == 1:
        if k0 not in root_keys and trigger_value in empty:
            print("stop because sub key is missing and value is None or ''")
            raise PreventUpdate
        if k0 in root_keys:
            print("previous_value", trigger_site[k0])
            if trigger_value == trigger_site[k0]:
                print("stop because value did not change")
                raise PreventUpdate

    else:
        k1 = keys[1]
        if k0 not in root_keys and trigger_value in empty:
            print("stop because sub key is missing and value is None or ''")
            raise PreventUpdate
        if k0 in root_keys:
            trigger_sub_key = trigger_site[k0].keys()
            # print("sub keys", trigger_sub_key)
            if k1 not in trigger_sub_key and trigger_value in empty:
                print("stop because sub key is missing and value is None or ''")
                raise PreventUpdate
            if k1 in trigger_sub_key:
                print("previous_value", trigger_site[k0][k1])
                if trigger_value == trigger_site[k0][k1]:
                    print("stop because value did not change")
                    raise PreventUpdate

            check_groups(states, k0, k1)


@app.callback(
    Output("new-json", "data"),
    [
        Input(f"0-isotope", "value"),
        *[Input(f"0-{item}", "n_blur") for item in all_keys if "isotope" not in item],
        Input("isotopomer-name", "n_blur"),
        Input("isotopomer-description", "n_blur"),
        Input("isotopomer-abundance", "n_blur"),
    ],
    [
        *[State(f"0-{item}", "value") for item in all_keys],
        State("local-isotopomers-data", "data"),
        State("isotopomer-dropdown", "value"),
        State("isotopomer-name", "value"),
        State("isotopomer-description", "value"),
        State("isotopomer-abundance", "value"),
    ],
)
def create_json(*args):
    """Generate a json object from the input fields in the isotopomers UI"""
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    if ctx.triggered[0]["value"] is None:
        raise PreventUpdate

    states = dash.callback_context.states
    print(ctx.triggered)
    # inputs = dash.callback_context.inputs

    data = states["local-isotopomers-data.data"]
    if data is None:
        raise PreventUpdate

    index = states["isotopomer-dropdown.value"]
    isotopomer = data["isotopomers"][index]

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id in [f"isotopomer-{_}" for _ in root_options]:
        print("creating json")
        isotopomer["abundance"] = states["isotopomer-abundance.value"]
        isotopomer["name"] = states["isotopomer-name.value"]
        isotopomer["description"] = states["isotopomer-description.value"]
        return isotopomer

    del (
        states["isotopomer-dropdown.value"],
        states["local-isotopomers-data.data"],
        states["isotopomer-abundance.value"],
        states["isotopomer-description.value"],
        states["isotopomer-name.value"],
    )

    sites = isotopomer["sites"]
    trigger_key = trigger_id.split("-")
    trigger_site_index, keys = trigger_key[0], trigger_key[1:]
    trigger_site = sites[int(trigger_site_index)]
    trigger_value = states[f"{trigger_id}.value"]

    if_value_change(trigger_site, trigger_value, keys, states)

    site = extract_site_dictionary_from_dash_triggers(states)
    # remove key entries with empty dict value.
    site = dict([(k, v) for k, v in site.items() if v != {}])
    sites[int(trigger_site_index)] = site
    print("creating json", site)
    return isotopomer


# test = html.Div(
#     className="form-popup",
#     id="myForm",
#     children=html.Form(
#         action="/action_page.php",
#         className="form-container",
#         children=[
#             html.H1("Login"),
#             html.Label("Email"),
#             dcc.Input(
#                 type="text", placeholder="Enter Email", name="email", required=True
#             ),
#             html.Label("Password"),
#             dcc.Input(
#                 type="text", placeholder="Enter Password", name="psw", required=True
#             ),
#             html.Button(type="submit", className="btn", children="Login"),
#             html.Button(
#                 type="submit",
#                 className="btn cancel",
#                 # onclick="closeForm()",
#                 children="Close",
#             ),
#         ],
#     ),
# )

# slide_from_left = html.Div(
#     [
#         html.Div(
#             id="myNav",
#             className="overlay",
#             children=[
#                 dbc.Button(
#                     html.I(className="fas fa-times"),
#                     id="toggle-overlay-hide",
#                     className="closebtn",
#                 ),
#                 html.Div(
#                     className="overlay-content",
#                     children=[
#                         html.A("About", href="#"),
#                         html.A("Services", href="#"),
#                         html.A("Clients", href="#"),
#                         html.A("Contact", href="#"),
#                     ],
#                 ),
#             ],
#         ),
#         dbc.Button("open overlay", id="toggle-overlay-show"),
#     ]
# )


# @app.callback(
#     Output("myNav", "style"),
#     [
#         Input("toggle-overlay-show", "n_clicks"),
#         Input("toggle-overlay-hide", "n_clicks"),
#     ],
#     [State("myNav", "style")],
# )
# def callback_overlay(n1, n2, style):
#     if n1 is n2 is None:
#         style["width"] = "0%"
#         return style
#     max_ = max(i for i in [n1, n2] if i is not None)
#     if max_ == n1:
#         style["width"] = "80%"
#     if max_ == n2:
#         style = {"width": "0%"}
#     return style


# test = html.Div(
#     [
#         html.Div(
#             id="myNav-info",
#             className="overlay",
#             children=[
#                 dbc.Button(
#                     html.I(className="fas fa-times"),
#                     id="toggle-overlay-hide",
#                     # href="javascript:void(0)",
#                     className="closebtn",
#                     # onclick="closeNav()",
#                 ),
#                 html.Div(
#                     className="overlay-content",
#                     children=[
#                         html.A("About", href="#"),
#                         html.A("Services", href="#"),
#                         html.A("Clients", href="#"),
#                         html.A("Contact", href="#"),
#                     ],
#                 ),
#             ],
#             style={"z-index": 1},
#         ),
#         dbc.Button(
#             "open",
#             id="toggle-overlay-show",
#             # style={"font-size": "30px", "cursor": "pointer"},
#         ),
#     ]
# )
