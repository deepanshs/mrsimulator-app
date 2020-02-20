# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from mrsimulator.dimension import ISOTOPE_DATA

from app.app import app
from app.custom_widgets import custom_collapsible
from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider

with open("app/isotopomer/test.json", "r") as f:
    input_ = json.load(f)
input_ = input_["isotopomers"][0]


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


def custom_fitting_input_group(
    prepend_label="", append_label="", identity=None, **kwargs
):
    """
        A custom dash bootstrap component input-group widget with a prepend-label,
        followed by an Input box, and an append-label.

        Args:
            prepend_label: A string to prepend dash-bootstrap-component Input widget.
            append_label: A string to append dash-bootstrap-component Input widget.
            kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    # Yeet custom collapsible into here oops
    group = [
        dbc.Button(
            prepend_label,
            className="input-group-prepend",
            id=f"{identity}-collapse-button",
        ),
        dcc.Input(
            type="number",
            # pattern="?[0-9]*\\.?[0-9]",
            className="form-control",
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


def fitting_collapsible(key, val, identity=None):
    if type(val) == int:
        valArray = (val, "")
        val = (valArray[0], valArray[1])

    tick_list = np.linspace(int(val[0]) - 10, int(val[0]) + 10, 5)
    tick_dict = {}
    for items in tick_list:
        tick_dict[int(items)] = f"{int(items)}"

    collapsible = dbc.Row(
        [
            dbc.Collapse(
                [
                    dbc.FormGroup(
                        [
                            dbc.Checklist(
                                options=[{"label": "Fix", "value": 1}],
                                value=[],
                                id=f"{identity}-switches-fix-input",
                                switch=True,
                            ),
                            dcc.Slider(
                                id=f"{identity}-slider",
                                # return_function=lambda x:f"{x} {val[1]}",
                                min=int(val[0]) - 10,
                                max=int(val[0]) + 10,
                                marks=tick_dict,
                                step=1,
                                value=int(val[0]),
                            ),
                            html.Br(),
                        ]
                    ),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    custom_input_group(
                                        prepend_label="Max",
                                        size="md",
                                        value=int(val[0]),
                                        id=f"{identity}_max-{i}",
                                    )
                                ),
                                dbc.Col(
                                    custom_input_group(
                                        prepend_label="Min",
                                        size="md",
                                        value=int(val[0]),
                                        id=f"{identity}_min-{i}",
                                    )
                                ),
                                dbc.Col(
                                    dbc.Checklist(
                                        options=[{"label": "Constraint", "value": 1}],
                                        value=0,
                                        id=f"{identity}-switches-constraint-input",
                                        switch=True,
                                    ),
                                    align="center",
                                ),
                            ],
                            no_gutters=True,
                            align="center",
                        )
                    ),
                    html.Div(
                        dbc.Collapse(
                            dcc.Textarea(placeholder="Expression"),
                            className="mb-3",
                            id=f"{identity}-collapse-expression",
                        )
                    ),
                ],
                id=f"{identity}-collapse",
            )
        ]
    )

    @app.callback(
        Output(f"{identity}-collapse", "is_open"),
        [Input(f"{identity}-collapse-button", "n_clicks")],
        [State(f"{identity}-collapse", "is_open")],
    )
    def toggle_collapse(button, is_open):
        if button:
            return not is_open
        return is_open

    @app.callback(
        Output(f"{identity}-collapse-expression", "is_open"),
        [Input(f"{identity}-switches-constraint-input", "value")],
        [State(f"{identity}-collapse-expression", "is_open")],
    )
    def toggle_switch(button, is_open):
        if button:
            return not is_open
        # return is_open

    return collapsible


def populate_key_value_from_object(object_dict, id_old):
    lst = []
    for key, value in object_dict.items():  # keys():
        id_new = f"{key}_{id_old}"
        print("new ", id_new)
        if isinstance(object_dict[key], dict):
            new_lst = populate_key_value_from_object(object_dict[key], id_new)
            lst.append(
                custom_collapsible(
                    text=key,
                    identity=id_new,
                    children=new_lst,
                    is_open=False,
                    size="sm",
                    button_classname="tree-control-button",
                    collapse_classname="tree-control",
                    style={"padding-left": "7px"},
                )
            )
        else:
            if key == "isotope":
                lst.append(
                    custom_input_group(
                        prepend_label=key, id=id_new, value=object_dict[key]
                    )
                )
            elif key == "eta":
                lst.append(
                    html.Div(
                        [
                            custom_fitting_input_group(
                                prepend_label=key,
                                id=id_new,
                                value=value,
                                identity=id_new,
                            ),
                            fitting_collapsible(key, value, identity=id_new),
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
                            custom_fitting_input_group(
                                prepend_label=key,
                                append_label=value[-1],
                                id=id_new,
                                value=value[0],
                                identity=id_new,
                            ),
                            fitting_collapsible(key, value, identity=id_new),
                        ],
                        className="input-group-append input-group d-flex",
                    )
                )
    return lst


widgets = []
for i, site in enumerate(input_["sites"]):
    id_ = f"site_{i}"
    widgets.append(
        html.Div(
            custom_collapsible(
                text=id_,
                identity=id_,
                children=populate_key_value_from_object(site, id_),
                is_open=False,
                size="sm",
                button_classname="tree-control-button",
                collapse_classname="tree-control-input",
                # style={"padding-left": "7px"},
            )
        )
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


wd = html.Div(widgets)
