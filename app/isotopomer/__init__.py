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
from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.custom_widgets import custom_input_group
from app.isotopomer.draft import filter_isotopomer_list

# from app.custom_widgets import custom_slider

N_SITE = 2
ATTR_PER_SITE = 12
isotope_options_list = [{"label": key, "value": key} for key in ISOTOPE_DATA.keys()]
colors = {"background": "#e2e2e2", "text": "#585858"}

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


def fitting_collapsible(key, val, identity=None):
    collapsible = dbc.Row(html.Br())
    return collapsible


def populate_key_value_from_object(object_dict, id_old):
    lst = []
    for key, value in object_dict.items():  # keys():
        id_new = f"{id_old}-{key}"
        if isinstance(object_dict[key], dict):
            # print(id_new)
            new_lst = populate_key_value_from_object(object_dict[key], id_new)
            lst.append(
                custom_collapsible(
                    text=key,
                    identity=id_new,
                    children=new_lst,
                    is_open=True,
                    size="sm",
                    # button_classname="tree-control-button",
                    # collapse_classname="tree-control",
                    style={"padding-left": "7px"},
                )
            )
        else:
            if key == "isotope":
                # lst.append(
                #     custom_input_group(
                #         prepend_label=key, id=id_new, value=object_dict[key]
                #     )
                # )
                lst.append(
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("Isotope", addon_type="prepend"),
                            dbc.Select(
                                options=isotope_options_list, value=value, id=id_new
                            ),
                        ],
                        className="mb-3",
                    )
                )
            elif key == "eta":
                lst.append(
                    html.Div(
                        [
                            custom_input_group(
                                prepend_label=key, id=id_new, value=value, debounce=True
                            ),
                            # fitting_collapsible(key, value, identity=id_new),
                        ],
                        className="input-group-append input-group d-flex",
                    )
                )

            else:
                number, unit = value.split()  # splitting string into number and unit
                # if "_" in key:
                #     key = key.replace("_", " ")
                lst.append(
                    html.Div(
                        [
                            custom_input_group(
                                prepend_label=key,
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


with open("app/isotopomer/test.json", "r") as f:
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


advance_isotopomer_editor_button = dbc.Col(
    custom_button(
        icon_classname="fas fa-edit",
        id="json-file-editor-button",
        tooltip="Advanced isotopomer editor",
        active=False,
        outline=True,
        color="dark",
        style={"float": "right"},
    )
)

advance_isotopomer_text_area = dbc.Textarea(
    className="mb-3 p-0",
    id="json-file-editor",
    placeholder="Isotopomer editor",
    draggable="False",
    contentEditable="False",
    spellCheck="False",
    bs_size="sm",
    rows=10,
    value="",
)

advance_isotopomer_text_area_collapsible = dbc.Collapse(
    advance_isotopomer_text_area, id="json-file-editor-collapse"
)


isotopomer_name_field = dcc.Input(
    # value=isotopomer["name"],
    placeholder="Isotopomer name",
    id="isotopomer-name",
    style={"textAlign": "left", "color": colors["text"]},
    className="d-flex flex-column grow",
)

isotopomer_description_field = dcc.Input(
    # value=isotopomer["description"],
    placeholder="Isotopomer description ... ",
    id="isotopomer-description",
    style={"textAlign": "left", "color": colors["text"]},
    className=" d-flex",
)

isotopomer_abundance_field = dcc.Input(
    placeholder="Isotopomer abundance",
    # value=100,
    id="isotopomer-abundance",
    style={"textAlign": "left", "color": colors["text"]},
    className=" d-flex",
)

isotopomer_form = dbc.Collapse(
    [
        dbc.Col(
            [
                isotopomer_name_field,  # isotopomer name
                isotopomer_description_field,  # isotopomer description
                isotopomer_abundance_field,  # isotopomer abundance
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
            [
                html.H4(
                    "Isotopomers", style={"fontWeight": "normal"}, className="pl-2"
                ),
                advance_isotopomer_editor_button,
            ],
            className="d-flex justify-content-between p-2",
        ),
        dbc.Col(["Select Isotopomer", isotopomer_dropdown]),
        html.Br(),
        advance_isotopomer_text_area_collapsible,
        isotopomer_form,
    ],
    id="isotopomer-body",
)


list_2 = ["shielding_symmetric", "quadrupolar"]
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
    return [
        quantity
        if isinstance(quantity, (float, int))
        else float(quantity.split(" ")[0])
    ][0]


def extract_sites_dictionary_dash_triggers(dash_triggers):
    """
    Extract a list of site dictionaries from the dash ids. This
    method does not depend on how the trigger ids are ordered.
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


def extract_trigger_values_from_dictionary(site_lists):
    """
    Extract the trigger values from an ordered list of site objects.
    The order of the trigger values follows the order defined by variable
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
    [Input("isotopomer-dropdown", "value")],
    [State("local-isotopomers-data", "data"), State("isotope_id-0", "value")],
)
def populate_isotopomer_fields(index, local_isotopomer_data, isotope_id_value):
    if local_isotopomer_data is None:
        raise PreventUpdate
    if index is None:
        raise PreventUpdate

    isotopomer_list = filter_isotopomer_list(
        local_isotopomer_data["isotopomers"], isotope_id_value
    )
    if index >= len(isotopomer_list):
        index = 0

    values = extract_trigger_values_from_dictionary(isotopomer_list[index]["sites"])
    return values


@app.callback(
    Output("new-json", "data"),
    [
        *[Input(f"{i}-isotope", "n_blur") for i in range(N_SITE)],
        *[
            Input(f"{i}-{item}", "n_blur")
            for i in range(N_SITE)
            for item in all_keys
            if "isotope" not in item
        ],
    ],
    [*[State(f"{i}-{item}", "value") for i in range(N_SITE) for item in all_keys]],
)
def create_json(*args):
    """Create a json object from the input fields in the isotopomers UI"""

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # state is a list of dict where dict is of form {'dash_id.value': 'value'}.
    states = dash.callback_context.states

    # the dash_id is defined as site_index-key1-key2, which is used to generate site
    # dictionary as
    #           site[site_index][key1][key2] = value
    # with this method, we don't have to track the order of the inputs. See function
    # extract_sites_dictionary_dash_triggers()
    sites = extract_sites_dictionary_dash_triggers(states)

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
