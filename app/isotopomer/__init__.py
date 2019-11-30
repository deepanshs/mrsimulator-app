# -*- coding: utf-8 -*-
from copy import deepcopy

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app
from app.custom_widgets import custom_input_group

keywords_site = [
    "name",
    "isotope",
    "isotropic_chemical_shift",
    ["zeta", "eta", "alpha", "beta", "gamma"],
    ["Cq", "eta", "alpha", "beta", "gamma"],
]
keywords_site_display = [
    "name",
    "isotope",
    "δ",
    ["ζ", "η", "α", "β", "γ"],
    ["Cq", "η", "α", "β", "γ"],
]
units_site = [
    "",
    "",
    "ppm",
    ["ppm", "", "rad", "rad", "rad"],
    ["MHz", "", "rad", "rad", "rad"],
]

# with open("app/isotopomer/test.json", "r") as f:
#     input_ = json.load(f)


def add_sites(data):
    print(data)
    rows = []
    for k_d, k, u in zip(keywords_site_display, keywords_site, units_site):
        if isinstance(k, list):
            for k_1d, k_1, u_1 in zip(k_d, k, u):
                if k_1 not in data:
                    value = None
                else:
                    value = data[k_1]
                rows.append(
                    custom_input_group(
                        prepend_label=k_1d, append_label=u_1, value=value, size="1"
                    )
                )
        else:
            if k not in data:
                value = None
            else:
                value = data[k]
            rows.append(
                custom_input_group(
                    prepend_label=k_d, append_label=u, value=value, size="2"
                )
            )
    return dbc.Card(rows)


keywords_isotopomers = ["name", "sites", "abundance"]


def add_isotopomers(data):
    rows = []
    for k in keywords_isotopomers:
        if k == "sites":
            for site in data["sites"]:
                rows.append(add_sites(site))
    return dbc.Card(rows)


display_symbols = {
    "zeta": "ζ",
    "eta": "η",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "Cq": "Cq",
}

classname_1 = "d-flex justify-content-between align-content-center formtext-dark"


def display_sites(sites):
    div = []
    for site in sites:
        for k, v in site.items():
            if isinstance(v, dict):
                value = []
                for k_1, v_1 in v.items():
                    value.append(
                        html.Div(
                            [html.Div(display_symbols[k_1]), html.Div(v_1)],
                            className=classname_1,
                        )
                    )
                v = value
            div.append(html.Div([html.Div(k), html.Div(v)], className=classname_1))
    return html.Div(div)


def display_isotopomers(isotopomers):
    div = []
    sub_div = []
    for i, isotopomer in enumerate(isotopomers):
        # sub_div = []
        if "name" not in isotopomer:
            name = f"isotopomer-{i}"
        else:
            if isotopomer["name"] in ["", None]:
                name = f"isotopomer-{i}"
            else:
                name = isotopomer["name"]
        if "abundance" not in isotopomer:
            abundance = "100%"
        else:
            abundance = isotopomer["abundance"]

        header = dbc.CardHeader(
            html.Div([html.Div(name), html.Div(abundance)], className=classname_1)
        )
        body = dbc.CardBody(display_sites(isotopomer["sites"]))
        sub_div.append(dbc.Col(dbc.Card([header, body])))
        if (i + 1) % 3 == 0:
            div.append(dbc.Row(deepcopy(sub_div)))
            sub_div = []
    return html.Div([*div, dbc.Row(sub_div)])


# with open("app/isotopomer/test.json", "r") as f:
#     input_ = json.load(f)


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
    if n1 is n2 is None:
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
