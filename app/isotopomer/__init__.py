# -*- coding: utf-8 -*-
import json
from copy import deepcopy

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
        id_new = f"{id_old}{key}"
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
    id_2 = f"site[{i}]"
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

greek_list = ["eta", "alpha", "beta", "gamma"]
list_2 = ["shielding_symmetric", "quadrupolar"]


def parse_number(quantity):
    if isinstance(quantity, (float, int)):
        return quantity
    return float(quantity.split(" ")[0])


# one function Input(isotopomoer-dropdown value) updates the fields, and create one json file
def parse_isotopomer_for_input_fields(isotopomer):
    sites = isotopomer["sites"]
    length = len(sites)

    isotope_field = [site["isotope"] for site in sites]
    shift_field = [parse_number(site["isotropic_chemical_shift"]) for site in sites]
    zeta_field = [
        parse_number(site["shielding_symmetric"]["zeta"])
        if "shielding_symmetric" in site.keys()
        else None
        for site in sites
    ]
    Cq_field = [
        parse_number(site["quadrupolar"]["Cq"])
        if "quadrupolar" in site.keys()
        else None
        for site in sites
    ]
    greek_field = [
        parse_number(site[key1][key2])
        if key1 in site.keys() and key2 in site[key1].keys()
        else None
        for site in sites
        for key1 in list_2
        for key2 in greek_list
    ]

    if length < 2:
        diff = 2 - length
        empty_field = [None] * diff
        isotope_field += empty_field
        shift_field += empty_field
        zeta_field += empty_field
        Cq_field += empty_field
        greek_field += empty_field * 8

    return [*isotope_field, *shift_field, *zeta_field, *Cq_field, *greek_field]


@app.callback(
    [
        *[Output(f"site[{i}]isotope", "value") for i in range(N_SITE)],
        *[Output(f"site[{i}]isotropic_chemical_shift", "value") for i in range(N_SITE)],
        *[Output(f"site[{i}]shielding_symmetriczeta", "value") for i in range(N_SITE)],
        *[Output(f"site[{i}]quadrupolarCq", "value") for i in range(N_SITE)],
        *[
            Output(f"site[{i}]{key1}{key2}", "value")
            for i in range(N_SITE)
            for key1 in list_2
            for key2 in greek_list
        ],
    ],
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

    return parse_isotopomer_for_input_fields(isotopomer_list[index])


@app.callback(
    Output("new_json", "data"),
    [
        *[Input(f"site[{i}]isotope", "n_blur") for i in range(N_SITE)],
        *[Input(f"site[{i}]isotropic_chemical_shift", "n_blur") for i in range(N_SITE)],
        *[Input(f"site[{i}]shielding_symmetriczeta", "n_blur") for i in range(N_SITE)],
        *[Input(f"site[{i}]quadrupolarCq", "n_blur") for i in range(N_SITE)],
        *[
            Input(f"site[{i}]{key1}{key2}", "n_blur")
            for i in range(N_SITE)
            for key1 in list_2
            for key2 in greek_list
        ],
    ],
    [
        *[State(f"site[{i}]isotope", "value") for i in range(N_SITE)],
        *[State(f"site[{i}]isotropic_chemical_shift", "value") for i in range(N_SITE)],
        *[State(f"site[{i}]shielding_symmetriczeta", "value") for i in range(N_SITE)],
        *[State(f"site[{i}]quadrupolarCq", "value") for i in range(N_SITE)],
        *[
            State(f"site[{i}]{key1}{key2}", "value")
            for i in range(N_SITE)
            for key1 in list_2
            for key2 in greek_list
        ],
    ],
)
def create_json(*args):
    print(args)
    remaining_items = [
        "isotope",
        "isotropic_chemical_shift",
        "shielding_symmetric",
        "quadrupolar",
    ]
    arg_list = args[12 * N_SITE :]
    """create a json object frim the input fields in the isotopomers UI"""
    default_site = {
        "isotope": "",
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
    default_isotopomer = {}
    default_isotopomer["sites"] = [deepcopy(default_site) for _ in range(N_SITE)]

    for i in range(N_SITE):
        site = default_isotopomer["sites"][i]

        for j1, key1 in enumerate(list_2):
            for j2, key2 in enumerate(greek_list):
                element = arg_list[4 * N_SITE + 4 * j1 + j2 + 8 * i]
                if element is not None:
                    if key2 == "eta":
                        site[key1][key2] = element
                    else:
                        site[key1][key2] = f"{element} {site[key1][key2]}"
                else:
                    del site[key1][key2]
        # print(site)
    for k, item in enumerate(remaining_items):
        for j, site in enumerate(default_isotopomer["sites"]):

            element = arg_list[k * N_SITE + j]
            if item == "shielding_symmetric":

                if element is not None:
                    site[item]["zeta"] = f"{element} {site[item]['zeta']}"
                else:
                    del site[item]["zeta"]
            elif item == "quadrupolar":

                if element is not None:
                    site[item]["Cq"] = f"{element} {site[item]['Cq']}"
                else:
                    del site[item]["Cq"]
            else:
                if element is not None:
                    site[item] = f"{element} {site[item]}"
                else:
                    del site[item]
        print(site)

        if site["shielding_symmetric"] == {}:
            del site["shielding_symmetric"]
        if site["quadrupolar"] == {}:
            del site["quadrupolar"]

    return json.dumps(default_isotopomer)


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
