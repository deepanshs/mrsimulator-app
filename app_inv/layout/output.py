# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.graph import generate_graph_instance

graph_output = generate_graph_instance(id_="INV-output")
graph_output.config["scrollZoom"] = True
interaction2 = dbc.Card(
    [
        dbc.CardHeader(html.H4("Parameters")),
        custom_input_group(
            prepend_label="l1 weight λ",
            append_label="",
            value=1e-6,
            id="INV-l1",
            min=0,
            debounce=True,
        ),
        custom_input_group(
            prepend_label="l2 weight α",
            append_label="",
            value=1e-6,
            id="INV-l2",
            min=0,
            debounce=True,
        ),
        dbc.Button("Invert", id="INV-solve"),
    ]
)
output_layer = dbc.Card(
    dbc.CardBody(dbc.Row([dbc.Col(graph_output), dbc.Col(interaction2, md=6, sm=12)]))
)
