# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app
from app.toolbar import collapsible_download_menu
from app.toolbar import toolbar

# from app.custom_widgets import custom_hover_help

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


help_message = html.Div(
    [
        html.Div(
            [
                html.I(className="fas fa-arrows-alt-v"),
                "  Scale maximum amplitude to one.",
            ]
        ),
        html.Div(
            [
                html.I(className="fas fa-chart-area"),
                "  Show spectrum from individual isotopomers.",
            ]
        ),
        html.Div(
            [
                html.I(className="fas fa-download"),
                "  Download dataset as `.csdf` or `.csv` format.",
            ]
        ),
    ]
)


button = html.P(
    html.I(className="fas fa-question-circle"), id="pop-up-simulation-button"
)

help_popup = dbc.Popover(
    [dbc.PopoverHeader("The simulated spectrum"), dbc.PopoverBody(help_message)],
    id="pop-up-simulation-help",
    is_open=False,
    placement="auto",
    target="pop-up-simulation-button",
)


@app.callback(
    Output("pop-up-simulation-help", "is_open"),
    [Input("pop-up-simulation-button", "n_clicks")],
    [State("pop-up-simulation-help", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


# help_popup = html.Div(
#     [
#         html.I(className="fas fa-question-circle"),
#         dbc.Tooltip(help_message, target="pop-up-simulation-help"),
#     ],
#     id="pop-up-simulation-help",
#     className="align-self-start",
# )

plotly_graph = dcc.Graph(
    id="nmr_spectrum",
    figure={
        "data": [
            go.Scatter(
                x=[-1.2, 0, 1.2],
                y=[0, 0, 0],
                mode="lines",
                line={"color": "black", "width": 1.2},
            )
        ],
        "layout": go.Layout(
            xaxis=dict(
                title="frequency",
                ticks="outside",
                showline=True,
                autorange="reversed",
                zeroline=False,
            ),
            yaxis=dict(
                title="arbitrary unit",
                ticks="outside",
                showline=True,
                zeroline=False,
                rangemode="tozero",
            ),
            autosize=True,
            transition={
                "duration": 175,
                "easing": "sin-out",
                "ordering": "traces first",
            },
            margin={"l": 50, "b": 45, "t": 5, "r": 5},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            template="none",
        ),
    },
    config={
        # "editable": True,
        # "edits": {"axisTitleText": True},
        "responsive": True,
        "scrollZoom": False,
        "showLink": False,
        # "autosizable": True,
        # "fillFrame": True,
        "modeBarButtonsToRemove": [
            # "zoom2d"
            # "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toggleHover",
            "toggleSpikelines",
        ],
        "displaylogo": False,
    },
)


spectrum_body = html.Div(
    id="spectrum-body",
    className="v-100 my-card",
    children=[
        html.Div(
            [
                html.H4("Simulation", style={"fontWeight": "normal"}, className="pl-2"),
                toolbar,
            ],
            className="d-flex justify-content-between p-2",
        ),
        collapsible_download_menu,
        html.Div(plotly_graph),
        # help_popup,
    ],
)
