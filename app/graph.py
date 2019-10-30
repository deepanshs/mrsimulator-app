# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .toolbar import toolbar

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


plotly_graph = dcc.Graph(
    id="nmr_spectrum",
    figure={"data": [], "layout": {"plot_bgcolor": "rgba(0, 0, 0,0)"}},
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

# graph_item = html.Div(
#     className="item", children=[plotly_graph]
# )

spectrum_body = html.Div(
    id="spectrum_card",
    className="v-100 my-card affix",
    children=[
        dbc.NavbarSimple(
            brand="Spectrum", children=toolbar, expand="sm", light=True, fluid=True
        ),
        plotly_graph,
    ],
)
