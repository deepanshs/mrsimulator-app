# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app.toolbar import collapsible_download_menu
from app.toolbar import toolbar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


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
        dbc.NavbarSimple(
            brand="Simulation",
            children=toolbar,
            expand="xs",
            light=True,
            fluid=True,
            className="my-card-header",
        ),
        collapsible_download_menu,
        html.Div(plotly_graph),
    ],
)
