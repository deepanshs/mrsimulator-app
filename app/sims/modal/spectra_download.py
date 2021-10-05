# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash_extensions.snippets import send_bytes

from app import app
from app.custom_widgets import custom_button


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"

# TODO: Figure out how to get plotly static image export binaries onto server (kaleido)
# TODO: Figure out how to get wptohtml onto heroku server
# TODO: Correct x-axis on downloaded csdf files


def download_as_csdf_pack():
    """Div with info and buttons for downloading data as csdf file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    headder = html.Div(html.B("Download spectrum data as csdf file"))
    doc_link = html.P(
        [
            "See the ",
            html.A(
                " csdf documentation page",
                href="https://csdmpy.readthedocs.io/en/v0.4.1/index.html",
            ),
            " for more info.",
        ]
    )
    csdf_btn = custom_button(
        text="csdf",
        icon_classname="far fa-file-archive fa-lg",
        tooltip="Download csdf of all spectra lines",
        id="download-spectra-csdf",
        **kwargs,
    )

    return html.Div([headder, doc_link, csdf_btn])


def download_as_html_pack():
    """Div with info and buttons for dowloading graph as interactive html file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    headder = html.Div(html.B("Download spectrum as as interactive Plotly html"))
    html_btn = custom_button(
        text="html",
        icon_classname="far fa-file-code fa-lg",
        tooltip="Download plot as interactive html file",
        id="download-spectra-html",
        **kwargs,
    )

    return html.Div([headder, html_btn])


def download_image_dimensions():
    """Inputs to adjust width and height of downloaded image"""
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Width", className="center-text left-align"),
                    dbc.Input(value=750, type="Number", id="download-image-width"),
                ]
            ),
            html.Div(
                [
                    html.Div("Height", className="center-text left-align"),
                    dbc.Input(value=400, type="Number", id="download-image-height"),
                ]
            ),
            html.Div(
                [
                    html.Div("Scale", className="center-text left-align"),
                    dbc.Input(value=2, type="Number", id="download-image-scale"),
                    html.Div(
                        "larger values mean higher resolution", className="center-text"
                    ),
                ]
            ),
        ],
        className="modal-body-item",
    )


def download_img_buttons():
    """Buttons for downloading graph image"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    pdf = custom_button(
        text="pdf",
        icon_classname="far fa-file-pdf fa-lg",
        tooltip="Download spectra as a pdf file",
        id="download-spectra-pdf",
        **kwargs,
    )
    svg = custom_button(
        text="svg",
        icon_classname="far fa-file-image fa-lg",
        tooltip="Download spectra as an svg image",
        id="download-spectra-svg",
        **kwargs,
    )
    png = custom_button(
        text="png",
        icon_classname="far fa-file-image fa-lg",
        tooltip="Download csdf of all spectra lines",
        id="download-spectra-png",
        **kwargs,
    )

    return html.Div([pdf, svg, png], className="modal-block")


def download_as_img_pack():
    """Div holding fields for downloading spectrum as image"""
    headder = html.Div(html.B("Download the spectrum as an image"))

    return html.Div([headder, download_image_dimensions(), download_img_buttons()])


def ui():
    """The UI holding the modal and all info"""
    return dbc.Modal(
        [
            dbc.ModalHeader("Spectrum Plot Download Options"),
            dbc.ModalBody(
                [
                    download_as_csdf_pack(),
                    download_as_html_pack(),
                    download_as_img_pack(),
                ]
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-download-spectra-modal")),
        ],
        id="download-spectra-modal",
        size="md",
        className="modal-dialogue",
    )


download_modal = ui()


# Callbacks ============================================================================


@app.callback(
    Output("download-spectrum", "data"),
    Input("download-spectra-csdf", "n_clicks"),
    Input("download-spectra-html", "n_clicks"),
    Input("download-spectra-pdf", "n_clicks"),
    Input("download-spectra-svg", "n_clicks"),
    Input("download-spectra-png", "n_clicks"),
    # State("local-mrsim-data", "data"),  # maybe need states for csdf download
    State("local-processed-data", "data"),
    State("nmr_spectrum", "figure"),
    State("download-image-width", "value"),
    State("download-image-height", "value"),
    State("download-image-scale", "value"),
    prevent_initial_call=True,
)
def plot_download(*args):
    """Callback for downloading plot logic"""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("download plot", trigger_id)

    return CALLBACKS[trigger_id]()


def download_csdf():
    """Download spectrum data as csdf file"""
    csdf_dict = ctx.states["local-processed-data.data"]

    return dict(content=json.dumps(csdf_dict), filename="spectrum.csdf")


def download_html():
    """Download spectrum as html file"""
    fig_dict = ctx.states["nmr_spectrum.figure"]
    fig_json = json.dumps(fig_dict)
    fig = plotly.io.from_json(str(fig_json))
    html_str = fig.to_html(fig)

    return dict(content=html_str, filename="plot.html")


def download_image():
    """Download the spectrum as an image"""
    fmt = ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
    width = ctx.states["download-image-width.value"]
    height = ctx.states["download-image-height.value"]
    scale = ctx.states["download-image-scale.value"]
    fig_dict = ctx.states["nmr_spectrum.figure"]
    fig_json = json.dumps(fig_dict)

    def write_bytes(bytes_io):
        fig = plotly.io.from_json(str(fig_json))
        img_bytes = fig.to_image(format=fmt, width=width, height=height, scale=scale)
        bytes_io.write(img_bytes)

    return send_bytes(write_bytes, f"plot.{fmt}")


CALLBACKS = {
    "download-spectra-csdf": download_csdf,
    "download-spectra-html": download_html,
    "download-spectra-pdf": download_image,
    "download-spectra-svg": download_image,
    "download-spectra-png": download_image,
}
