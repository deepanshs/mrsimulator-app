# -*- coding: utf-8 -*-
import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator.dimension import ISOTOPE_DATA

from app.app import app
from app.custom_widgets import custom_collapsible
from app.custom_widgets import custom_input_group
from app.isotopomer.toolbar import advanced_isotopomer_text_area_collapsible
from app.isotopomer.toolbar import toolbar

N_SITE = 1
ATTR_PER_SITE = 12
isotope_options_list = [{"label": key, "value": key} for key in ISOTOPE_DATA.keys()]
colors = {"background": "#e2e2e2", "text": "#585858"}

isotopomer_prepend_labels = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "zeta": "ζ",
    "eta": "η",
    "isotropic_chemical_shift": "δ",
    "Cq": "Cq",
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
        "eta": None,
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
    "quadrupolar": {
        "Cq": "MHz",
        "eta": None,
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
        if isinstance(value, str):
            number, unit = value.split()  # splitting string into number and unit
        else:
            number = value
            unit = None

        feature_input_fields.append(
            html.Div(
                [
                    custom_input_group(
                        prepend_label=isotopomer_prepend_labels[key],
                        append_label=unit,
                        value=number,
                        id=f"{site_number}-{id_label}-{key}",
                        debounce=True,
                    )
                ]
            )
        )

    orientation_input_fields = []
    for key, value in orientation_dict.items():
        if isinstance(value, str):
            number, unit = value.split()  # splitting string into number and unit
        else:
            number = value
            unit = None

        orientation_input_fields.append(
            html.Div(
                [
                    custom_input_group(
                        prepend_label=isotopomer_prepend_labels[key],
                        append_label=unit,
                        value=number,
                        id=f"{site_number}-{id_label}-{key}",
                        debounce=True,
                    )
                ]
            )
        )

    lst = html.Div(
        [
            html.Br(),
            dbc.ButtonGroup(
                [
                    dbc.Button(f"{id_label}", id=f"{id_label}-button", disabled=False),
                    dbc.Button(
                        f"Orientation",
                        id=f"{id_label}-orientation-button",
                        disabled=False,
                    ),
                ],
                size="sm",
                className="mr-1",
            ),
            dbc.InputGroup(
                [
                    dbc.Collapse(
                        feature_input_fields, id=f"{id_label}-feature-collapse"
                    ),
                    dbc.Collapse(
                        orientation_input_fields, id=f"{id_label}-orientation-collapse"
                    ),
                ],
                className="mb-3",
                style={"display": "inline"},
            ),
        ]
    )

    @app.callback(
        [
            Output(f"{id_label}-feature-collapse", "is_open"),
            Output(f"{id_label}-orientation-collapse", "is_open"),
        ],
        [
            Input(f"{id_label}-button", "n_clicks"),
            Input(f"{id_label}-orientation-button", "n_clicks"),
        ],
        [
            State(f"{id_label}-feature-collapse", "is_open"),
            State(f"{id_label}-orientation-collapse", "is_open"),
        ],
    )
    def toggle_feature_buttons(n1, n2, feature_active, orientation_active):
        ctx = dash.callback_context

        if not ctx.triggered:
            return ""
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            print(button_id)

        if button_id == f"{id_label}-button" and n1:
            return not feature_active, False
        elif button_id == f"{id_label}-orientation-button" and n2:
            return False, not orientation_active
        return False, False

    @app.callback(
        [Output(f"{id_label}-orientation-button", "disabled")],
        [
            *[
                Input(f"{site_number}-{id_label}-{key}", "value")
                for key in feature_dict.keys()
            ]
        ],
    )
    def freeze_orientation_button(*args):
        print(f"My data for {id_label}", args[0], args[1])
        if args[0] is None and args[1] is None:
            return [True]
        else:
            return [False]

    return lst


def populate_key_value_from_object(object_dict, id_old):
    lst = []
    for key, value in object_dict.items():  # keys():
        id_new = f"{id_old}-{key}"
        print("id new", id_new)
        if isinstance(object_dict[key], dict):
            print("the key", key)
            # feature_orientation_collapsible(object_dict[key])
            new_lst = populate_key_value_from_object(object_dict[key], id_new)
            lst.append(feature_orientation_collapsible(object_dict[key], key, id_old))
            #     custom_collapsible(
            #         text=key.replace("_", " "),
            #         identity=id_new,
            #         children=new_lst,
            #         is_open=True,
            #         size="sm",
            #         # button_classname="tree-control-button",
            #         # collapse_classname="tree-control",
            #         style={"padding-left": "7px"},
            #     )
            # )
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
                if isinstance(value, str):
                    number, unit = (
                        value.split()
                    )  # splitting string into number and unit
                else:
                    number = value
                    unit = None
                # if "_" in key:
                #     key = key.replace("_", " ")
                lst.append(
                    html.Div(
                        [
                            custom_input_group(
                                prepend_label=isotopomer_prepend_labels[key],
                                append_label=unit,
                                value=number,
                                id=id_new,
                                debounce=True,
                            ),
                            # fitting_collapsible(key, value, identity=id_new),
                        ],
                        # className="input-group-append input-group d-flex",
                    )
                )
    return html.Div(lst, className="collapsible-body-control form")


with open("app/isotopomer/template.json", "r") as f:
    isotopomer = json.load(f)
# def make_isotopomers_UI(isotopomers_data, id_):
# master_widgets = []
# for j, isotopomer in enumerate(isotopomers_data["isotopomers"]):
widgets = []
# id_1 = f"[{1}]%site"
for i, site in enumerate(isotopomer["sites"]):
    id_2 = f"{i}"
    widgets.append(
        dbc.Tab(
            label=f"site {i}",
            children=populate_key_value_from_object(site, id_2)  # custom_collapsible(
            # text=id_,
            # identity=id_,
            # children=populate_key_value_from_object(site, id_),
            # is_open=True,
            # size="sm",
            # button_classname="tree-control-button",
            # collapse_classname="tree-control-input",
            # style={"padding-left": "7px"},
        )
    )

# master_widgets.append(dbc.Tabs(widgets))
# return master_widgets


# def make_isotopomer_dropdown_UI():#isotopomers_data):
isotopomer_dropdown = dcc.Dropdown(
    value=0,
    options=[
        # {"label": f"Isotopomer {i}", "value": i}
        # for i in range(len(isotopomers_data["isotopomers"]))
    ],
    multi=False,
    id="isotopomer-dropdown",
    clearable=False,
)
# return isotopomer_dropdown


@app.callback(
    Output("site_UI", "children"),
    [Input("isotopomer_selection_dropdown", "value")],
    [State("local-isotopomers-ui-data", "data")],
)
def site_UI_update(value, UI_data):
    if UI_data is None:
        raise PreventUpdate
    return UI_data[value]


isotopomer_name_field = custom_input_group(
    prepend_label="Name",
    input_type="text",
    # value=isotopomer["name"],
    placeholder="Isotopomer name",
    id="isotopomer-name",
    style={"textAlign": "left", "color": colors["text"]},
)

isotopomer_description_field = custom_input_group(
    # value=isotopomer["description"],
    prepend_label="Description",
    input_type="text",
    placeholder="Isotopomer description ... ",
    id="isotopomer-description",
    style={"textAlign": "left", "color": colors["text"]},
    size="sm",
)

isotopomer_abundance_field = custom_input_group(
    prepend_label="Abundance",
    input_type="text",
    placeholder="Isotopomer abundance",
    value=isotopomer["abundance"],
    id="isotopomer-abundance",
    style={"textAlign": "left", "color": colors["text"]},
)

isotopomer_form = dbc.Collapse(
    [
        dbc.Col(
            [
                isotopomer_name_field,  # isotopomer name
                isotopomer_description_field,  # isotopomer description
                isotopomer_abundance_field,  # isotopomer abundance
                html.Br(),
            ]
        ),
        dbc.Tabs(widgets),
    ],
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
    className="v-100 my-card",
    children=[
        html.Div(
            html.H4(
                "Isotopomers",
                style={"fontWeight": "normal"},
                className="pl-2",
                id="isotopomer-card",
            ),
            className="d-flex justify-content-between p-2",
        ),
        dbc.Col(toolbar),
        dbc.Col(["Select Isotopomer", isotopomer_dropdown]),
        html.Br(),
        advanced_isotopomer_text_area_collapsible,
        isotopomer_form,
    ],
    id="isotopomer-body",
)

isotopomer_body_card = html.Div(isotopomer_body, id="isotopomer-body-card")


# callback code section =======================================================

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
        "eta": None,
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
    "quadrupolar": {
        "Cq": "MHz",
        "eta": None,
        "alpha": "deg",
        "beta": "deg",
        "gamma": "deg",
    },
}


def parse_number(quantity):
    """Return the numerical value of a quantity."""
    return (
        quantity
        if isinstance(quantity, (float, int))
        else float(quantity.split(" ")[0])
    )


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
    sites = [
        {
            "isotope": None,
            "isotropic_chemical_shift": None,
            "shielding_symmetric": {},
            "quadrupolar": {},
        }
        for _ in range(N_SITE)
    ]
    for key, value in dash_triggers.items():
        if value is not None:
            group = key.split(".")[0].split("-")
            i = int(group[0])
            if len(group) == 2:
                unit = default_unit[group[1]]
                val = [value if unit is None else f"{value} {unit}"][0]
                sites[i][group[1]] = val
            if len(group) == 3:
                unit = default_unit[group[1]][group[2]]
                val = [value if unit is None else f"{value} {unit}"][0]
                sites[i][group[1]][group[2]] = val
    return sites


# def flatten_dict(dd, separator="-", prefix=""):
#     return (
#         {
#             "".join([prefix, separator, k]) if prefix else k: v
#             for kk, vv in dd.items()
#             for k, v in flatten_dict(vv, separator, kk).items()
#         }
#         if isinstance(dd, dict)
#         else {prefix: dd}
#     )


def extract_isotopomer_UI_field_values_from_dictionary(site_lists):
    """
    Extract the values from an ordered list of site objects. the extracted values are
    sent to the dash Output.
    The order of the optput trigger values follows the order defined by the variable
    `all_keys`.
    """
    root_keys = [site.keys() for site in site_lists]

    trigger_values = [None for _ in range(ATTR_PER_SITE * N_SITE)]
    for i, site in enumerate(site_lists):
        for k, key in enumerate(all_keys):
            group = key.split("-")
            if len(group) == 1:
                if group[0] in root_keys[i]:
                    val = site[group[0]]
                    trigger_values[i * ATTR_PER_SITE + k] = [
                        parse_number(val) if key != "isotope" else val
                    ][0]
            if len(group) == 2:
                if group[0] in root_keys[i]:
                    sub_root_keys = site[group[0]].keys()
                    if group[1] in sub_root_keys:
                        val = site[group[0]][group[1]]
                        trigger_values[i * ATTR_PER_SITE + k] = parse_number(val)

    return trigger_values


@app.callback(
    [*[Output(f"{i}-{item}", "value") for i in range(N_SITE) for item in all_keys]],
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
    if is_advanced_editor_open:
        raise PreventUpdate
    if local_isotopomer_data is None:
        raise PreventUpdate
    if index is None:
        raise PreventUpdate

    # isotopomer_list = filter_isotopomer_list(
    #     local_isotopomer_data["isotopomers"], isotope_id_value
    # )
    isotopomer_list = local_isotopomer_data["isotopomers"]
    if index >= len(isotopomer_list):
        index = 0

    values = extract_isotopomer_UI_field_values_from_dictionary(
        isotopomer_list[index]["sites"]
    )
    return values


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


@app.callback(
    Output("new-json", "data"),
    [
        *[Input(f"{i}-isotope", "value") for i in range(N_SITE)],
        *[
            Input(f"{i}-{item}", "n_blur")
            for i in range(N_SITE)
            for item in all_keys
            if "isotope" not in item
        ],
        # *[Input(f"{i}-{item}", "n_blur") for i in range(N_SITE) for item in all_keys],
    ],
    [
        *[State(f"{i}-{item}", "value") for i in range(N_SITE) for item in all_keys],
        State("local-isotopomers-data", "data"),
        State("isotopomer-dropdown", "value"),
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
    data = data["isotopomers"][index]

    del states["isotopomer-dropdown.value"], states["local-isotopomers-data.data"]
    # print(data)

    # if data is not None:
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    trigger_key = trigger_id.split("-")
    trigger_site_index, keys = trigger_key[0], trigger_key[1:]
    trigger_site = data["sites"][int(trigger_site_index)]
    trigger_value = str(states[f"{trigger_id}.value"]).strip()
    # print("state", states[f"{trigger_id}.value"])
    # print(trigger_value)

    empty = ["", "None"]
    root_keys = trigger_site.keys()
    if len(keys) == 1:
        if keys[0] not in root_keys and trigger_value in empty:
            print("stop because sub key is missing and value is None or ''")
            raise PreventUpdate
        if keys[0] in root_keys:
            previous_value = str(trigger_site[keys[0]]).split(" ")[0]
            print("previous_value", previous_value)
            if previous_value == trigger_value:
                print("stop because value did not change")
                raise PreventUpdate

    else:
        if keys[0] not in root_keys and trigger_value in empty:
            print("stop because sub key is missing and value is None or ''")
            raise PreventUpdate
        if keys[0] in root_keys:
            trigger_sub_key = trigger_site[keys[0]].keys()
            # print("sub keys", trigger_sub_key)
            if keys[1] not in trigger_sub_key and trigger_value in empty:
                print("stop because sub key is missing and value is None or ''")
                raise PreventUpdate
            if keys[1] in trigger_sub_key:
                previous_value = str(trigger_site[keys[0]][keys[1]]).split(" ")[0]
                print("previous_value", previous_value)
                if previous_value == trigger_value:
                    print("stop because value did not change")
                    raise PreventUpdate

    print("creating json")

    sites = extract_site_dictionary_from_dash_triggers(states)

    # remove key entries with empty dict.
    sites = [site for site in sites if site["isotope"] is not None]
    sites = [dict([(k, v) for k, v in site.items() if v != {}]) for site in sites]

    isotopomer_dict = {}
    isotopomer_dict["sites"] = sites
    return isotopomer_dict


# (None, None, None, None, None, None, None, None, None, None,
#  None, None, None, None, None, None, None, None, None, None,
#  None, None, None, None, '1H', '1H', '100', '200', '1', '9',
#  '5', '13', 0.5, '2', '3', '4', 0.7, '6', '7', '8', 0.8, '10',
#  '11', '12', 0.9, '14', '15', '16')

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
