# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .modal.help import simulation_help
from .modal.spectra_download import download_modal
from app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_switch

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"


default_data = go.Scatter(
    x=[-1.2, 0, 1.2],
    y=[0, 0, 0],
    mode="lines",
    line={"color": "black", "width": 1.2},
)

default_layout = go.Layout(
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
    ),
    autosize=True,
    # transition={"duration": 175, "easing": "sin-out", "ordering": "traces first"},
    transition={
        "duration": 300,
        "easing": "quad-in-out",
        "ordering": "traces first",
    },
    margin={"l": 60, "b": 45, "t": 10, "r": 10},
    legend={"x": 0, "y": 1},
    hovermode="closest",
    # paper_bgcolor="rgba(255,255,255,0.1)",
    # plot_bgcolor="rgba(255,255,255,0.3)",
    template="none",
    clickmode="event+select",
    # dragmode="drawrect",
)

default_fig_config = {
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
        # "autoScale2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "toggleHover",
        # "toggleSpikelines",
    ],
    "modeBarButtonsToAdd": [
        "drawline",
        # "drawopenpath",
        # "drawclosedpath",
        # "drawcircle",
        "drawrect",
        "eraseshape",
    ],
    "displaylogo": False,
}

DEFAULT_FIGURE = {
    "data": [default_data],
    "layout": default_layout,
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


def generate_graph_instance(id_=""):
    return dcc.Graph(id=id_, figure=DEFAULT_FIGURE, config=default_fig_config)


def graph_ui():
    plotly_graph = generate_graph_instance(id_="nmr_spectrum")

    # initialize app with graph instance
    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="initialize"),
        Output("temp1", "children"),
        [Input("nmr_spectrum", "figure")],
    )

    return dcc.Loading(plotly_graph, type="dot")


def tools():
    def download_spectra():
        """Button for opening spectra downloads modal"""
        kwargs = {"outline": True, "color": "dark", "size": "md"}
        download_btn = custom_button(
            icon_classname="fas fa-download fa-lg",
            tooltip="Download Simulation from selected method.",
            id="open-download-spectra-modal",
            **kwargs,
        )

        app.clientside_callback(
            """function (n1, n2, is_open) { return !is_open; }""",
            Output("download-spectra-modal", "is_open"),
            Input("open-download-spectra-modal", "n_clicks"),
            Input("close-download-spectra-modal", "n_clicks"),
            State("download-spectra-modal", "is_open"),
            prevent_initial_call=True,
        )

        return download_btn

    def graph_tool_pack():
        """Normalize to one and spectral decompose buttons"""
        kwargs = dict(
            outline=True,
            color="dark",
            style={"zIndex": 0},
            size="md",
        )
        normalize_button = custom_switch(
            # text="Normalize",
            icon_classname="fas fa-arrows-alt-v",
            id="normalize_amp",
            # size="sm",
            tooltip="Scale maximum amplitude to one.",
            **kwargs,
        )

        decompose_spectrum_button = custom_switch(
            # text="Decompose",
            icon_classname="fac fa-decompose",
            id="decompose_spectrum",
            # size="sm",
            tooltip="Decompose spectrum from individual spin systems.",
            **kwargs,
        )
        return dbc.ButtonGroup([normalize_button, decompose_spectrum_button])

    return html.Div([graph_tool_pack(), download_spectra()])


def header():
    icon = html.I(className="fac fa-spectrum fa-lg")

    # help button and associated callback
    help_button = html.Div(
        html.I(className="fas fa-question-circle pl-1 fa-lg", title="Show help"),
        id="pop-up-simulation-button",
        style={"cursor": "pointer"},
    )
    app.clientside_callback(
        "function (n, is_open) { return !is_open; }",
        Output("modal-simulation-help", "is_open"),
        Input("pop-up-simulation-button", "n_clicks"),
        State("modal-simulation-help", "is_open"),
        prevent_initial_call=True,
    )

    title = html.H4(["Simulation", help_button], className="title-with-help")
    head = html.Div([icon, title])

    return html.Div([head, tools()], className="card-header")


def download_element():
    """Dash extentions download element for downloading the plot"""
    return dcc.Download(id="download-spectrum")


def layout():
    return [header(), graph_ui(), simulation_help, download_modal, download_element()]


def ui():
    experiment_drop_upload = dcc.Upload(
        layout(),
        id="upload-measurement-from-graph",
        disable_click=True,
        # accept="application/json, text/plain, .csdf",
        style_active={
            "border": "1px solid rgb(78, 196, 78)",
            "backgroundColor": "rgb(225, 255, 225)",
            "opacity": "0.75",
        },
        # style_reject={
        #     "border": "1px solid rgb(196, 78, 78)",
        #     "backgroundColor": "rgb(255, 225, 225)",
        #     "opacity": "0.75",
        #     "borderRadius": "0.8em",
        # },
    )

    return html.Div(
        id="spectrum-body",
        className="left-card",
        children=experiment_drop_upload,
    )


spectrum_body = ui()


def one_d_multi_trace(data, x0, dx, maximum, name=None):
    """Use for multi line plots. When decompose is true"""
    return [
        dict(
            type="scatter",
            x0=x0,
            dx=dx,
            y=datum.components[0] / maximum,
            mode="lines",
            opacity=0.6,
            line={"width": 1},
            fill="tozeroy",
            name=name if datum.name == "" else datum.name,
        )
        for datum in data
    ]


def one_d_single_trace(data, x0, dx, maximum, name=""):
    """Use for single line plot"""
    line = (
        {"color": "black", "width": 1}
        if name == "simulation"
        else {"color": "#706f1c", "width": 1}
        if name == "residual"
        else {"color": "#7e0a7e", "width": 1}
    )
    return [
        dict(
            type="scatter",
            x0=x0,
            dx=dx,
            y=data[0].components[0] / maximum,
            mode="lines",
            line=line,
            name=name,
        )
    ]


def plot_1D_trace(data, normalized=False, decompose=False, name=""):
    x = data.x[0].coordinates.value
    x0 = x[0]
    dx = x[1] - x[0]
    maximum = max([yi.components.max() for yi in data.y]) if normalized else 1.0

    args = (data.y, x0, dx, maximum, name)
    return one_d_multi_trace(*args) if decompose else one_d_single_trace(*args)


def plot_2D_trace(data, normalized=False, decompose=False):
    plot_trace = []

    x, y = [item.coordinates.value for item in data.x]

    if decompose:
        maximum = max([yi.components.max() for yi in data.y]) if normalized else 1.0

        for datum in data.y:
            name = None if datum.name == "" else datum.name
            plot_trace.append(
                go.Contour(
                    dx=x[1] - x[0],
                    dy=y[1] - y[0],
                    x0=x[0],
                    y0=y[0],
                    z=datum.components[0] / maximum,
                    fillcolor=False,
                    # type="heatmap",
                    showscale=False,
                    # mode="lines",
                    opacity=0.6,
                    colorscale="dense",
                    # line={"width": 1.2},
                    # fill="tozeroy",
                    name=name,
                )
            )
        return plot_trace

    y_data = 0
    for datum in data.split():
        y_data += datum
    if normalized:
        y_data /= y_data.max()

    plot_trace += [
        dict(
            dx=x[1] - x[0],
            dy=y[1] - y[0],
            x0=x[0],
            y0=y[0],
            z=y_data.y[0].components[0],
            type="heatmap",
            showscale=False,
            # line_smoothing=0,
            # contours_coloring="lines",
            # line_width=1.2,
            # mode="lines",
            # line={"color": "black", "width": 1.2},
            colorscale="dense",
            # "tempo", "curl", "armyrose", "dense",  # "electric_r",
            # zmid=0,
            name="simulation",
        )
    ]
    return plot_trace
