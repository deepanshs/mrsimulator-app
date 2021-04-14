# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


with open("app/examples/example_link.json", "r") as f:
    mrsimulator_examples = json.load(f)

# mrsimulator_examples = []
example_length = len(mrsimulator_examples)


def card(entry):
    title = dbc.Card(dbc.CardHeader(entry["label"]))
    return html.A(title, href="./simulator?a=" + entry["value"], target="_blank")


def examples():
    return [dbc.Col(card(item)) for item in mrsimulator_examples]


root_app = html.Div(
    [
        dcc.Link("Simulator", href="/simulator", id="simulator-app"),
        dcc.Link("Inversion", href="/inversion", id="inversion-app"),
        *examples(),
    ],
    className="home-page",
)
