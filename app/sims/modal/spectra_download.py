# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_widgets import custom_button

# import dash_core_components as dcc
# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.dependencies import State
# from app import app


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def download_datasets():
    """Buttons and descriptions pertaining to downloading the datasets of spectrum"""
    # TODO: Allow user to download only selected lines with checkboxes
    # TODO: Decide if icon is good enough
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    download_btn = custom_button(
        text="csdf",
        icon_classname="far fa-file-archive fa-3x",
        tooltip="Download csdf of all spectra lines",
        id="download-spectra-csdf",
        **kwargs,
    )
    # TODO: Add checkboxes for lines (either custom_switch or html/dbc.checkbox)
    # Need to check if experiment found + residual
    # check_boxes = html.Div("")
    info_text = html.Div(
        (
            "Download the experiment, simulation or residual as a csdf file. "
            "Use the selection buttons to the left to choose which datasets to include."
        )
    )

    return html.Div([download_btn, info_text], className="spectra-download-type")


def download_plot_as_html():
    """UI for downloading the plot as interactive html file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    download_btn = custom_button(
        text="html",
        icon_classname="far fa-file-code fa-3x",
        tooltip="Download plot as interactive html file",
        id="download-spectra-html",
        **kwargs,
    )
    info_text = html.Div(
        (
            "Donwload the spectra as fully functional Plotly graph in an html file. "
            "This file can be opened in a web browser and interacted with like any "
            "other Plotly graph."
        )
    )

    return html.Div([download_btn, info_text], className="spectra-download-type")


def download_plot_as_pdf():
    """UI for downloading the plot as a pdf file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    download_btn = custom_button(
        text="pdf",
        icon_classname="far fa-file-pdf fa-3x",
        tooltip="Download spectra as a pdf file",
        id="download-spectra-pdf",
        **kwargs,
    )
    info_text = html.Div(
        (
            "Download the spectra as a pdf file. "
            "The image will be drawn in a vector format on a full landscape page."
        )
    )

    return html.Div([download_btn, info_text], className="spectra-download-type")


def download_plot_as_svg():
    """UI for downloading the plot as an svg file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    download_btn = custom_button(
        text="svg",
        icon_classname="far fa-file-image fa-3x",
        tooltip="Download spectra as an svg image",
        id="download-spectra-svg",
        **kwargs,
    )
    info_text = html.Div(
        (
            "Download the spectra as an svg image. "
            "Svg images are a vector format and can scale to any size without losing "
            "resolution. "
        )
    )

    return html.Div([download_btn, info_text], className="spectra-download-type")


def download_plot_as_png():
    """UI for downloading the plot as a png file"""
    kwargs = {"outline": True, "color": "dark", "size": "lg"}
    download_btn = custom_button(
        text="png",
        icon_classname="far fa-file-image fa-3x",
        tooltip="Download csdf of all spectra lines",
        id="download-spectra-png",
        **kwargs,
    )
    info_text = html.Div(
        (
            "Download the spectra as a png image. "
            "Png images are smaller than an svg or pdf but offer a limited resoluton. "
            "This is the best option for quickly sharing the graph"
        )
    )

    return html.Div([download_btn, info_text], className="spectra-download-type")


def ui():
    """The UI holding the modal and all info"""
    return dbc.Modal(
        [
            dbc.ModalHeader("Download Options"),
            dbc.ModalBody(
                [
                    download_datasets(),
                    download_plot_as_html(),
                    download_plot_as_pdf(),
                    download_plot_as_svg(),
                    download_plot_as_png(),
                ]
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-download-spectra-modal")),
        ],
        id="download-spectra-modal",
        size="lg",
        className="modal-dialogue",
    )


download_modal = ui()


# Callbacks ============================================================================
