# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app.app import app
from app.modal.help import simulation_help
from app.toolbar import toolbar

# from app.toolbar import collapsible_download_menu

# from app.custom_widgets import custom_hover_help

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


button = html.Div(
    html.I(className="fas fa-question-circle pl-1"), id="pop-up-simulation-button"
)


@app.callback(
    Output("modal-simulation-help", "is_open"),
    [Input("pop-up-simulation-button", "n_clicks")],
    [State("modal-simulation-help", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


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
                title="frequency ratio / ppm",
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
            margin={"l": 60, "b": 45, "t": 5, "r": 5},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            paper_bgcolor="rgba(255,255,255,0.1)",
            plot_bgcolor="rgba(255,255,255,0.3)",
            template="none",
            clickmode="event+select",
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
            "toImage",
            # "zoom2d"
            # "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            # "autoScale2d",
            "resetScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toggleHover",
            "toggleSpikelines",
        ],
        "displaylogo": False,
    },
)

className = "d-flex align-items-center"
spectrum_body = html.Div(
    id="spectrum-body",
    className="v-100 my-card",
    children=dcc.Upload(
        [
            html.Div(
                [
                    html.H4(
                        ["Simulation", button],
                        style={"fontWeight": "normal"},
                        className=f"pl-2 {className} justify-content-center",
                    ),
                    toolbar,
                ],
                className=f"p-2 justify-content-between {className}",
            ),
            html.Div(plotly_graph),
            simulation_help,
        ],
        id="upload-from-graph",
        disable_click=True,
        # accept="application/json, text/plain, .csdf",
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
            "borderRadius": "0.8em",
        },
        # style_reject={
        #     "border": "1px solid rgb(196, 78, 78)",
        #     "backgroundColor": "rgb(255, 225, 225)",
        #     "opacity": "0.75",
        #     "borderRadius": "0.8em",
        # },
    ),
)
