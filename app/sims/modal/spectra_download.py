# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash_extensions.snippets import send_bytes

from app import app
from app.custom_widgets import custom_button


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def download_btn_pack():
    """Button group for selecting type of download"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    img_btn = custom_button(
        text="imgage",
        icon_classname="far fa-file-image fa-lg",
        tooltip="Download csdf of all spectra lines",
        id="download-img",
        active=True,
        **kwargs,
    )
    csdf_btn = custom_button(
        text="csdf",
        icon_classname="far fa-file-archive fa-lg",
        tooltip="Download csdf of all spectra lines",
        id="download-csdf",
        **kwargs,
    )
    html_btn = custom_button(
        text="html",
        icon_classname="far fa-file-code fa-lg",
        tooltip="Download plot as interactive html file",
        id="download-html",
        **kwargs,
    )

    return html.Div(dbc.ButtonGroup([img_btn, csdf_btn, html_btn]), className="center")


def image_options_div():
    """User inputs for type, size, and quality of image"""

    # callback for showing div when img button clicked, hiding otherwise
    img_type = dcc.Dropdown(
        options=[
            {"label": "png", "value": "png"},
            {"label": "svg", "value": "svg"},
            {"label": "pdf", "value": "pdf"},
        ],
        value="png",
        id="image-type",
        clearable=False,
    )
    img_units = dcc.Dropdown(
        options=[
            {"label": "in", "value": "in"},
            {"label": "cm", "value": "cm"},
        ],
        value="in",
        id="image-units",
        clearable=False,
    )
    img_dpi = dbc.Input(value=100, type="Number", id="image-dpi", step="any")
    img_width = dbc.Input(value=8, type="Number", id="image-width", step="any")
    img_height = dbc.Input(value=5, type="Number", id="image-height", step="any")

    type_div = html.Div(["Type", img_type], className="center-text")
    units_div = html.Div(["Units", img_units], className="center-text")
    dpi_div = html.Div(
        [html.Div("Dots / in", id="dpi-label"), img_dpi], className="center-text"
    )
    width_div = html.Div(["Width", img_width], className="center-text")
    height_div = html.Div(["Height", img_height], className="center-text")

    return html.Div(
        [type_div, units_div, dpi_div, width_div, height_div], id="img-options-div"
    )


def description_div():
    """Div for explaining what will be dowloaded"""
    return html.Div("Download an image of the spectrum", id="download-description")


def ui():
    """The UI holding the modal and all info"""
    return dbc.Modal(
        [
            dbc.ModalHeader("Spectrum Plot Download Options"),
            dbc.ModalBody(
                [
                    download_btn_pack(),
                    description_div(),
                    image_options_div(),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button("Download", id="download-sepctrum-btn"),
                    dbc.Button("Close", id="close-download-spectra-modal"),
                ]
            ),
        ],
        id="download-spectra-modal",
        size="sm",
        className="modal-dialogue",
    )


download_modal = ui()


# Callbacks ============================================================================

# Only allow one button to be active at a time
app.clientside_callback(
    ClientsideFunction(
        namespace="download_spectrum", function_name="change_download_type"
    ),
    Output("download-img", "active"),
    Output("download-csdf", "active"),
    Output("download-html", "active"),
    Input("download-img", "n_clicks"),
    Input("download-csdf", "n_clicks"),
    Input("download-html", "n_clicks"),
    prevent_initial_call=True,
)

# Update values on units change
app.clientside_callback(
    """function (val, width, height, dpi) {
        if (val == 'cm') {      // in to cm
            width *= 2.54;
            height *= 2.54;
            dpi *= 2.54;
        } else {                // cm to in
            width /= 2.54;
            height /= 2.54;
            dpi /= 2.54;
        }
        // Round values to 3 decimal places
        width = parseFloat(width.toFixed(3));
        height = parseFloat(height.toFixed(3));
        dpi = parseFloat(dpi.toFixed(3));
        return [`Dots / ${val}`, width, height, dpi];
    }
    """,
    Output("dpi-label", "children"),
    Output("image-width", "value"),
    Output("image-height", "value"),
    Output("image-dpi", "value"),
    Input("image-units", "value"),
    State("image-width", "value"),
    State("image-height", "value"),
    State("image-dpi", "value"),
    prevent_initial_call=True,
)


@app.callback(
    Output("download-spectrum", "data"),
    Input("download-sepctrum-btn", "n_clicks"),
    State("download-img", "active"),
    State("download-csdf", "active"),
    State("download-html", "active"),
    State("local-processed-data", "data"),
    State("nmr_spectrum", "figure"),
    State("image-type", "value"),
    State("image-width", "value"),
    State("image-height", "value"),
    State("image-dpi", "value"),
    State("image-units", "value"),
    prevent_initial_call=True,
)
def plot_download(*args):
    """Callback for downloading plot logic"""
    # trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print("download plot")

    if ctx.states["download-img.active"]:
        return download_image()

    if ctx.states["download-html.active"]:
        return download_html()

    if ctx.states["download-csdf.active"]:
        return download_csdf()


def download_image():
    """Download the spectrum as an image"""
    # fmt = ctx.triggered[0]["prop_id"].split(".")[0].split("-")[-1]
    fmt = ctx.states["image-type.value"]
    fig_dict = ctx.states["nmr_spectrum.figure"]
    fig_json = json.dumps(fig_dict)

    def write_bytes(bytes_io):
        fig = plotly.io.from_json(str(fig_json))
        width, height, scale = get_plotly_dimensions()
        img_bytes = fig.to_image(format=fmt, width=width, height=height, scale=scale)
        bytes_io.write(img_bytes)

    return send_bytes(write_bytes, f"plot.{fmt}")


def download_html():
    """Download spectrum as html file"""
    fig_dict = ctx.states["nmr_spectrum.figure"]
    fig_json = json.dumps(fig_dict)
    fig = plotly.io.from_json(str(fig_json))
    html_str = fig.to_html(fig)

    return dict(content=html_str, filename="plot.html")


def download_csdf():
    """Download spectrum data as csdf file"""
    csdf_dict = ctx.states["local-processed-data.data"]

    return dict(content=json.dumps(csdf_dict), filename="spectrum.csdf")


def get_plotly_dimensions():
    """Calculates Plotly widht, height, and scale dimensions"""
    width = float(ctx.states["image-width.value"])
    height = float(ctx.states["image-height.value"])
    dpi = float(ctx.states["image-dpi.value"])
    cm_or_in = ctx.states["image-units.value"]

    # convert to inches if in centimeters
    if cm_or_in == "cm":
        width = width / 2.54
        height = height / 2.54
        dpi = dpi / 2.54

    # Plotly default dpi (scale 1) is 72
    width = width * 72
    height = height * 72
    scale = dpi / 72

    return width, height, scale


CALLBACKS = {
    "download-spectra-csdf": download_csdf,
    "download-spectra-html": download_html,
    "download-spectra-pdf": download_image,
    "download-spectra-svg": download_image,
    "download-spectra-png": download_image,
}
