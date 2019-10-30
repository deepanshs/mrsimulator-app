# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app

# with open("app/isotopomer/test.json", "r") as f:
#     input_ = json.load(f)


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


# def populate_key_value_from_object(object_dict, id_old):
#     lst = []
#     for key in object_dict.keys():
#         id_new = f"{key}_{id_old}"
#         if isinstance(object_dict[key], dict):
#             new_lst = populate_key_value_from_object(object_dict[key], id_new)
#             lst.append(
#                 custom_collapsible(
#                     text=key,
#                     identity=id_new,
#                     children=new_lst,
#                     is_open=False,
#                     size="sm",
#                     button_classname="tree-control-button",
#                     collapse_classname="tree-control",
#                     # style={"padding-left": "7px"},
#                 )
#             )
#         else:
#             lst.append(
#                 custom_form_group(prepend_label=key, id=id_new,
#                               value=object_dict[key])
#             )
#     return lst


# widgets = []
# for i, site in enumerate(input_["sites"]):
#     id_ = f"site_{i}"
#     widgets.append(
#         html.Div(
#             custom_collapsible(
#                 text=id_,
#                 identity=id_,
#                 children=populate_key_value_from_object(site, id_),
#                 is_open=False,
#                 size="sm",
#                 button_classname="tree-control-button",
#                 collapse_classname="tree-control-input",
#                 # style={"padding-left": "7px"},
#             )
#         )
#     )


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

slide_from_left = html.Div(
    [
        html.Div(
            id="myNav",
            className="overlay",
            children=[
                dbc.Button(
                    html.I(className="fas fa-times"),
                    id="toggle-overlay-hide",
                    className="closebtn",
                ),
                html.Div(
                    className="overlay-content",
                    children=[
                        html.A("About", href="#"),
                        html.A("Services", href="#"),
                        html.A("Clients", href="#"),
                        html.A("Contact", href="#"),
                    ],
                ),
            ],
        ),
        dbc.Button("open overlay", id="toggle-overlay-show"),
    ]
)


@app.callback(
    Output("myNav", "style"),
    [
        Input("toggle-overlay-show", "n_clicks"),
        Input("toggle-overlay-hide", "n_clicks"),
    ],
    [State("myNav", "style")],
)
def callback_overlay(n1, n2, style):
    if n1 == n2 is None:
        style["width"] = "0%"
        return style
    max_ = max(i for i in [n1, n2] if i is not None)
    if max_ == n1:
        style["width"] = "80%"
    if max_ == n2:
        style = {"width": "0%"}
    return style


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


# wd = html.Div(widgets)
