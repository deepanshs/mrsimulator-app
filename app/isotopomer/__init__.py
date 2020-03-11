# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrsimulator.dimension import ISOTOPE_DATA

from app.app import app
from app.custom_widgets import custom_collapsible
from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider


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
    id_ = kwargs["id"]
    custom_fitting_input_group(prepend_label, append_label, **kwargs)

    @app.callback(
        Output("local-isotopomers-data", "data"),
        [Input(f"{id_}", "value")],  # id belongs to the input field
        [State("local-isotopomers-data", "data")],
    )
    def update_isotopomers_data(value, local_isotopomer_data):
        key = id_.split("_")[1].replace("%", ".")
        print(key)
        local_isotopomer_data[key] = value
        return local_isotopomer_data


def fitting_collapsible(key, val, identity=None):
    collapsible = dbc.Row(html.Br())
    return collapsible


def populate_key_value_from_object(object_dict, id_old):
    lst = []
    for key, value in object_dict.items():  # keys():
        id_new = f"{id_old}%{key}"
        print(id_new)
        if isinstance(object_dict[key], dict):
            print("insode")
            new_lst = populate_key_value_from_object(object_dict[key], id_new)
            lst.append(
                custom_collapsible(
                    text=key,
                    identity=id_new,
                    children=new_lst,
                    is_open=False,
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
                value = value.split()
                if "_" in key:
                    key = key.replace("_", " ")
                lst.append(
                    html.Div(
                        [
                            custom_input_group_callable(
                                prepend_label=key,
                                append_label=value[-1],
                                value=value[0],
                                id=id_new,
                            ),
                            # fitting_collapsible(key, value, identity=id_new),
                        ],
                        className="input-group-append input-group d-flex",
                    )
                )
    return html.Div(lst, className="collapsible-body-control form")


def make_isotopomers_UI(isotopomers_data, id_):
    master_widgets = []
    for j, isotopomer in enumerate(isotopomers_data["isotopomers"]):
        widgets = []
        id_1 = f"{id_}_isotopomer[{j}]%site"
        for i, site in enumerate(isotopomer["sites"]):
            id_2 = f"{id_1}[{i}]"
            print(id_)
            widgets.append(
                dbc.Tab(
                    label=f"site {i}",
                    children=populate_key_value_from_object(
                        site, id_2
                    )  # custom_collapsible(
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

        master_widgets.append(dbc.Tabs(widgets))
    return master_widgets


def make_isotopomer_dropdown_UI(isotopomers_data):
    isotopomer_dropdown = dcc.Dropdown(
        value=0,
        options=[
            {"label": f"Isotopomer {i}", "value": i}
            for i in range(len(isotopomers_data["isotopomers"]))
        ],
        id="isotopomer_selection_dropdown",
        clearable=False,
    )
    return isotopomer_dropdown


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
        html.Div(
            [html.H4("Isotopomers", style={"fontWeight": "normal"}, className="pl-2")],
            className="d-flex justify-content-between p-2",
        ),
        html.Div(id="isotopomer_list"),
        html.Div(id="site_UI"),
    ],
    id="isotopomer-body",
)


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
