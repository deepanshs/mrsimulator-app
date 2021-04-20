# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output

from app import app

with open("app/examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)


mrinversion_examples = [
    {
        "label": "KMg0.5-4SiO2 MAT",
        "value": "https://zenodo.org/record/3964531/files/KMg0_5-4SiO2-MAT.csdf",
    },
    {
        "label": "Rb2O-2.25SiO2 MAF",
        "value": "https://zenodo.org/record/3964531/files/Rb2O-2_25SiO2-MAF.csdf",
    },
]


def card(item, app_name):
    img_src = "/assets/fit.png" if "img" not in item else item["img"]
    img = dbc.CardImg(src=img_src, top=True)
    title = html.H4(item["label"])
    des = "This is description" if "description" not in item else item["description"]
    body = dbc.CardBody([title, html.P(des)])
    card_ = dbc.Card([img, body])
    a = html.A(card_, href=f"./{app_name}?a=" + item["value"])
    return dbc.Col(a, xl=2, lg=3, md=3, sm=4, xs=6)


# def search_engine():
#     dropdown_menu_items = [
#         dbc.DropdownMenuItem("Mrsimulator", id="search-here"),
#         dbc.DropdownMenuItem("Material project", id="search-mp-contribs"),
#     ]

#     search_button = dbc.Button("Search", id="mrsim-search-button", color="light")
#     search_bar = dbc.InputGroup(
#         [
#             dbc.DropdownMenu(
#                 dropdown_menu_items, label="Target", color="light",
#                   addon_type="prepend"
#             ),
#             dbc.Input(id="input-group-search", placeholder="Search on site"),
#             dbc.InputGroupAddon(search_button, addon_type="append"),
#         ],
#         size="lg",
#     )
#     return search_bar


# app.clientside_callback(
#     """
#     function () {
#         let trigger = dash_clientside.callback_context.triggered;
#         let trigger_id = trigger.map((t) => t["prop_id"])[0].split(".")[0];
#         if (trigger_id == 'search-mp-contribs') return 'Search on Material project';
#         if (trigger_id == 'search-here') return 'Search on site';
#     }
#     """,
#     Output("input-group-search", "placeholder"),
#     [Input("search-mp-contribs", "n_clicks"), Input("search-here", "n_clicks")],
#     prevent_initial_call=True,
# )


def examples_ui(examples, app_name):
    return [dbc.Row([card(item, app_name) for item in examples])]


def generic_ui(image, description, button, children=[]):
    body = dbc.Row(
        [dbc.Col(image, sm=12, md=8), dbc.Col([html.P(description), button])],
        className="header",
    )
    return [body, *children]


def mrsimulator_ui():
    image = html.Img(src="/assets/images/mrsimulator.svg", alt="Mrsimulator")
    description = (
        "Build with plotly-dash, Mrsimulator app brings a convenient user "
        "interface for fast solid-state NMR spectum simulation and "
        "least-squares analysis."
    )
    button = dbc.Button("Open App", href="/simulator", id="simulator-app")

    children = [
        # html.Section(search_engine()),
        html.Section(
            [
                html.H1("Featured Examples"),
                *examples_ui(mrsimulator_examples, "simulator"),
            ]
        ),
    ]
    return generic_ui(image, description, button, children)


def mrinversion_ui():
    image = html.Img(src="/assets/images/mrinversion.png", alt="Mrinversion")
    description = ""
    button = dbc.Button("Comming Soon", href="/", id="inversion-app")

    # children = [
    #     html.Section(
    #         [
    #             html.H1("Featured Examples"),
    #             *examples_ui(mrinversion_examples, "inversion"),
    #         ]
    #     ),
    # ]
    return generic_ui(image, description, button)  # , children)


mrsim_btn = html.Button(
    html.Img(src="assets/fit.png"),
    id="mrsim-app-selection-button",
    # color="light",
    # active=True,
)
mrinv_btn = html.Button("Inversion", id="mrinv-app-selection-button")
root_app = html.Div(
    [
        html.Section(
            [
                html.H1("Apps"),
                mrsim_btn,
                mrinv_btn,
                # html.Hr(),
                dcc.Loading(html.Div(children=mrsimulator_ui(), id="empty-main-div")),
            ]
        ),
    ],
    className="home-page",
)


@app.callback(
    [
        Output("empty-main-div", "children"),
        # Output("mrsim-app-selection-button", "active"),
        # Output("mrinv-app-selection-button", "active"),
    ],
    [
        Input("mrsim-app-selection-button", "n_clicks"),
        Input("mrinv-app-selection-button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def update_main_page(*args):
    trigger = ctx.triggered[0]["prop_id"]
    if trigger == "mrsim-app-selection-button.n_clicks":
        return [mrsimulator_ui()]  # , True, False]
    if trigger == "mrinv-app-selection-button.n_clicks":
        return [mrinversion_ui()]  # , False, True]
    return [mrsimulator_ui()]  # , True, False]
