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

# <div class="item ">
#       <img src="http://placehold.it/600x350">
#       <h2>Title</h2>
#       <p> Text</p>
#       <div class="overlay"> </div>
#    < / div >

graph_item = html.Div(
    className="item", children=[plotly_graph, html.Div(className="overlay")]
)

spectrum_body = html.Div(
    id="spectrum_card",
    className="v-100 my-card",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.H4("Spectrum", style={"padding-top": 12, "padding-left": 20})
                ),
                html.Div(
                    toolbar,
                    style={"padding-top": 0, "padding-right": 10, "padding-left": 10},
                ),
            ]
        ),
        graph_item,
    ],
    style={"width": "100%"},
)
