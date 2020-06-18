# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


colors = {"background": "#e2e2e2", "text": "#585858"}

# Info ------------------------------------------------------------------------------ #


sample_info = html.Div(
    className="my-card",
    children=dcc.Upload(
        html.Div(id="info-read-only"),
        id="upload-spin-system-local",
        disable_click=True,
        multiple=False,
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
        },
    ),
    id="info-body",
)


def update_sample_info(json_data):
    title = json_data["name"]
    title = "Sample" if title == "" else title
    description = json_data["description"]
    data = dbc.CardBody(
        [
            html.H5(title),
            html.P(description, style={"textAlign": "left", "color": colors["text"]}),
        ],
        className="sample-info-cards",
    )
    return dbc.Card(data)
