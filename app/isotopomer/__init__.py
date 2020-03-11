# -*- coding: utf-8 -*-
# from copy import deepcopy
# import dash_bootstrap_components as dbc
# import dash_html_components as html
# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.dependencies import State
# from app.app import app
# from app.custom_widgets import custom_input_group
# keywords_site = [
#     "name",
#     "isotope",
#     "isotropic_chemical_shift",
#     ["zeta", "eta", "alpha", "beta", "gamma"],
#     ["Cq", "eta", "alpha", "beta", "gamma"],
# ]
# keywords_site_display = [
#     "name",
#     "isotope",
#     "δ",
#     ["ζ", "η", "α", "β", "γ"],
#     ["Cq", "η", "α", "β", "γ"],
# ]
# units_site = [
#     "",
#     "",
#     "ppm",
#     ["ppm", "", "rad", "rad", "rad"],
#     ["MHz", "", "rad", "rad", "rad"],
# ]
# # with open("app/isotopomer/test.json", "r") as f:
# #     input_ = json.load(f)
# # def add_sites(data):
# #     print(data)
# #     rows = []
# #     for k_d, k, u in zip(keywords_site_display, keywords_site, units_site):
# #         if isinstance(k, list):
# #             for k_1d, k_1, u_1 in zip(k_d, k, u):
# #                 if k_1 not in data:
# #                     value = None
# #                 else:
# #                     value = data[k_1]
# #                 rows.append(
# #                     custom_input_group(
# #                         prepend_label=k_1d, append_label=u_1, value=value, size="1"
# #                     )
# #                 )
# #         else:
# #             if k not in data:
# #                 value = None
# #             else:
# #                 value = data[k]
# #             rows.append(
# #                 custom_input_group(
# #                     prepend_label=k_d, append_label=u, value=value, size="2"
# #                 )
# #             )
# #     return dbc.Card(rows)
# keywords_isotopomers = ["name", "sites", "abundance"]
# def add_isotopomers(data):
#     rows = []
#     for k in keywords_isotopomers:
#         if k == "sites":
#             for site in data["sites"]:
#                 rows.append(add_sites(site))
#     return dbc.Card(rows)
# display_symbols = {
#     "zeta": "ζ",
#     "eta": "η",
#     "alpha": "α",
#     "beta": "β",
#     "gamma": "γ",
#     "Cq": "Cq",
# }
# classname_1 = "d-flex justify-content-between align-content-center formtext-dark"
# def display_sites(sites):
#     div = []
#     for site in sites:
#         for k, v in site.items():
#             if isinstance(v, dict):
#                 value = []
#                 for k_1, v_1 in v.items():
#                     value.append(
#                         html.Div(
#                             [html.Div(display_symbols[k_1]), html.Div(v_1)],
#                             className=classname_1,
#                         )
#                     )
#                 v = value
#             div.append(html.Div([html.Div(k), html.Div(v)], className=classname_1))
#     return html.Div(div)
# def display_isotopomers(isotopomers):
#     div = []
#     sub_div = []
#     for i, isotopomer in enumerate(isotopomers):
#         # sub_div = []
#         if "name" not in isotopomer:
#             name = f"isotopomer-{i}"
#         else:
#             if isotopomer["name"] in ["", None]:
#                 name = f"isotopomer-{i}"
#             else:
#                 name = isotopomer["name"]
#         if "abundance" not in isotopomer:
#             abundance = "100%"
#         else:
#             abundance = isotopomer["abundance"]
#         header = dbc.CardHeader(
#             html.Div([html.Div(name), html.Div(abundance)], className=classname_1)
#         )
#         body = dbc.CardBody(display_sites(isotopomer["sites"]))
#         sub_div.append(dbc.Col(dbc.Card([header, body])))
#         if (i + 1) % 3 == 0:
#             div.append(dbc.Row(deepcopy(sub_div)))
#             sub_div = []
#     return html.Div([*div, dbc.Row(sub_div)])
# # with open("app/isotopomer/test.json", "r") as f:
# #     input_ = json.load(f)
# # def populate_key_value_from_object(object_dict, id_old):
# #     lst = []
# #     for key in object_dict.keys():
# #         id_new = f"{key}_{id_old}"
# #         if isinstance(object_dict[key], dict):
# #             new_lst = populate_key_value_from_object(object_dict[key], id_new)
# #             lst.append(
# #                 custom_collapsible(
# #                     text=key,
# #                     identity=id_new,
# #                     children=new_lst,
# #                     is_open=False,
# #                     size="sm",
# #                     button_classname="tree-control-button",
# #                     collapse_classname="tree-control",
# #                     # style={"padding-left": "7px"},
# #                 )
# #             )
# #         else:
# #             lst.append(
# #                 custom_form_group(prepend_label=key, id=id_new,
# #                               value=object_dict[key])
# #             )
# #     return lst
# # widgets = []
# # for i, site in enumerate(input_["sites"]):
# #     id_ = f"site_{i}"
# #     widgets.append(
# #         html.Div(
# #             custom_collapsible(
# #                 text=id_,
# #                 identity=id_,
# #                 children=populate_key_value_from_object(site, id_),
# #                 is_open=False,
# #                 size="sm",
# #                 button_classname="tree-control-button",
# #                 collapse_classname="tree-control-input",
# #                 # style={"padding-left": "7px"},
# #             )
# #         )
# #     )
# # test = html.Div(
# #     className="form-popup",
# #     id="myForm",
# #     children=html.Form(
# #         action="/action_page.php",
# #         className="form-container",
# #         children=[
# #             html.H1("Login"),
# #             html.Label("Email"),
# #             dcc.Input(
# #                 type="text", placeholder="Enter Email", name="email", required=True
# #             ),
# #             html.Label("Password"),
# #             dcc.Input(
# #                 type="text", placeholder="Enter Password", name="psw", required=True
# #             ),
# #             html.Button(type="submit", className="btn", children="Login"),
# #             html.Button(
# #                 type="submit",
# #                 className="btn cancel",
# #                 # onclick="closeForm()",
# #                 children="Close",
# #             ),
# #         ],
# #     ),
# # )
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
# # test = html.Div(
# #     [
# #         html.Div(
# #             id="myNav-info",
# #             className="overlay",
# #             children=[
# #                 dbc.Button(
# #                     html.I(className="fas fa-times"),
# #                     id="toggle-overlay-hide",
# #                     # href="javascript:void(0)",
# #                     className="closebtn",
# #                     # onclick="closeNav()",
# #                 ),
# #                 html.Div(
# #                     className="overlay-content",
# #                     children=[
# #                         html.A("About", href="#"),
# #                         html.A("Services", href="#"),
# #                         html.A("Clients", href="#"),
# #                         html.A("Contact", href="#"),
# #                     ],
# #                 ),
# #             ],
# #             style={"z-index": 1},
# #         ),
# #         dbc.Button(
# #             "open",
# #             id="toggle-overlay-show",
# #             # style={"font-size": "30px", "cursor": "pointer"},
# #         ),
# #     ]
# # )
# # wd = html.Div(widgets)
# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app
from app.custom_widgets import custom_collapsible
from app.custom_widgets import custom_input_group
# from mrsimulator.dimension import ISOTOPE_DATA

# from app.custom_widgets import custom_slider

N_SITE = 2

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
        id_new = f"{id_old}%{key}"
        if isinstance(object_dict[key], dict):
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
                            dbc.Input(placeholder="#Nucleus", type="text"),
                        ],
                        className="mb-3",
                    )
                )
            elif key == "eta":
                lst.append(
                    html.Div(
                        [
                            custom_input_group(
                                prepend_label=key, id=id_new, value=value
                            ),
                            # fitting_collapsible(key, value, identity=id_new),
                        ],
                        className="input-group-append input-group d-flex",
                    )
                )

            else:
                number, unit = value.split()  # splitting string into number and unit
                if "_" in key:
                    key = key.replace("_", " ")
                lst.append(
                    html.Div(
                        [
                            custom_input_group(
                                prepend_label=key,
                                append_label=unit,
                                value=number,
                                id=id_new,
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


# Isotopomer layout
isotopomer_body = html.Div(
    className="v-100 my-card",
    children=[
        dcc.Store(id="new_json", storage_type="memory"),
        html.Div(
            [html.H4("Isotopomers", style={"fontWeight": "normal"}, className="pl-2")],
            className="d-flex justify-content-between p-2",
        ),
        isotopomer_dropdown,  # html.Div(id="isotopomer_list"),
        dbc.Tabs(widgets),
    ],
    id="isotopomer-body",
)

greek_list = ["eta", "alpha", "beta", "gamma"]
list_2 = ["shielding_symmetric", "quadrupolar"]
# Outermost loop = N_SITE, innermost loop = greek_letter for fifth input
# *[Input(f"site[{i}]%shielding_symmetric%eta", "value") for i in range(N_SITE)],
# *[Input(f"site[{i}]%shielding_symmetric%alpha", "value") for i in range(N_SITE)],
# *[Input(f"site[{i}]%shielding_symmetric%beta", "value") for i in range(N_SITE)],
# *[Input(f"site[{i}]%shielding_symmetric%gamma", "value") for i in range(N_SITE)],


@app.callback(
    Output("new_jason", "data"),
    [
        # *[Input(f"site[{i}]%isotope", "value") for i in range(N_SITE)],
        *[Input(f"site[{i}]%isotropic_chemical_shift", "value") for i in range(N_SITE)],
        *[Input(f"site[{i}]%shielding_symmetric%zeta", "value") for i in range(N_SITE)],
        *[Input(f"site[{i}]%quadrupolar%Cq", "value") for i in range(N_SITE)],
        *[
            Input(f"site[{i}]%{key1}%{key2}", "value")
            for i in range(N_SITE)
            for key1 in list_2
            for key2 in greek_list
        ],
    ],
)
def create_json(*args, **kwargs):
    print(args, kwargs)
    return ""


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
