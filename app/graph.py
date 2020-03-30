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
    html.I(className="fas fa-question-circle pl-1"),
    id="pop-up-simulation-button",
    style={"cursor": "pointer"},
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


DEFAULT_FIGURE = {
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
            autorange=True,
            rangemode="tozero",
        ),
        autosize=True,
        transition={"duration": 300, "easing": "quad", "ordering": "traces first"},
        margin={"l": 60, "b": 45, "t": 5, "r": 5},
        legend={"x": 0, "y": 1},
        hovermode="closest",
        paper_bgcolor="rgba(255,255,255,0.1)",
        plot_bgcolor="rgba(255,255,255,0.3)",
        template="none",
        clickmode="event+select",
    ),
}

#  ['linear', 'quad', 'cubic', 'sin', 'exp', 'circle',
#             'elastic', 'back', 'bounce', 'linear-in', 'quad-in',
#             'cubic-in', 'sin-in', 'exp-in', 'circle-in', 'elastic-in',
#             'back-in', 'bounce-in', 'linear-out', 'quad-out',
#             'cubic-out', 'sin-out', 'exp-out', 'circle-out',
#             'elastic-out', 'back-out', 'bounce-out', 'linear-in-out',
#             'quad-in-out', 'cubic-in-out', 'sin-in-out', 'exp-in-out',
#             'circle-in-out', 'elastic-in-out', 'back-in-out',
#             'bounce-in-out']

plotly_graph = dcc.Graph(
    id="nmr_spectrum",
    figure=DEFAULT_FIGURE,
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
            # "zoomIn2d",
            # "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toggleHover",
            # "toggleSpikelines",
        ],
        "displaylogo": False,
    },
)

className = "align-items-center"
spectrum_body = html.Div(
    id="spectrum-body",
    className="my-card",
    children=dcc.Upload(
        [
            html.Div(
                [html.H4(["Simulation", button], className="title-with-help"), toolbar],
                className="card-header toolbar toolbar-header",
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
