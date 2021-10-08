# -*- coding: utf-8 -*-
import os.path as path

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_extensions as de
import dash_html_components as html
import pdfkit
from dash import callback_context as ctx
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from dash_extensions.snippets import send_bytes
from lmfit import Parameters
from mrsimulator import __version__ as mrsim_v

from app import __version__ as mrapp_v
from app import app
from app.custom_widgets import custom_button


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def homepage_html_store():
    """Store element for homepage info"""
    return dcc.Store(id="homepage-html", storage_type="memory")


def header():
    """Report title"""
    kwargs = {"outline": True, "color": "dark", "size": "md"}
    report_btn = custom_button(
        text="Full Report",
        icon_classname="fas fa-file-pdf fa-lg",
        id="download-fit-report-btn",
        tooltip="Download the full fit report as a pdf",
        **kwargs,
    )
    values_btn = custom_button(
        text="Values",
        icon_classname="fas fa-file-download  fa-lg",
        id="download-fit-values-btn",
        tooltip="Download the full fit report as a pdf",
        **kwargs,
    )
    return html.Div(
        children=dbc.ButtonGroup([report_btn, values_btn]),
        className="card-header",
    )


def report():
    """Div for LMFIT report tables"""
    return html.Div(
        children="This page will automatically update after a fit.",
        id="fit-report-table-div",
    )


def download_components():
    """Dash extention compoenets to download fit data"""
    return [
        de.Download(id="download-fit-report"),
        de.Download(id="download-fit-values"),
    ]


def ui():
    page = html.Div([header(), report(), *download_components(), homepage_html_store()])
    return html.Div(className="left-card", children=page, id="fit_report-body")


fit_report_body = ui()


# Callbacks ============================================================================
app.clientside_callback(
    ClientsideFunction(namespace="report", function_name="get_fit_report_html"),
    Output("homepage-html", "data"),
    Input("download-fit-report-btn", "n_clicks"),
    prevent_initial_callback=True,
)


# clientside callback for updating info
app.clientside_callback(
    ClientsideFunction(namespace="report", function_name="updateFitReport"),
    Output("temp9", "children"),
    Input("local-simulator-data", "data"),
    prevent_initial_call=True,
)


# callback for downloading param values as a json file
@app.callback(
    Output("download-fit-values", "data"),
    Input("download-fit-values-btn", "n_clicks"),
    State("local-mrsim-data", "data"),
    State("params-data", "data"),
    prevent_initial_call=True,
)
def download_values_dict(*args):
    """Downloads a dictonary of param names and values as json file"""
    print("download fit values")
    mrsim_data = ctx.states["local-mrsim-data.data"]
    params_data = ctx.states["params-data.data"]

    if mrsim_data is None or params_data is None:
        # display error no mrsim/params data found
        raise PreventUpdate

    params = Parameters().loads(params_data)

    return dict(content=str(params.valuesdict()), filename="values.json")


# callback for downloading full report
@app.callback(
    Output("download-fit-report", "data"),
    Input("homepage-html", "modified_timestamp"),
    State("homepage-html", "modified_timestamp"),
    State("download-fit-report-btn", "n_clicks_timestamp"),
    State("homepage-html", "data"),
    State("local-mrsim-data", "data"),
    # State("info-read-only", "children"),
    prevent_initial_call=True,
)
def download_report(*args):
    """Download the html of report as a pdf"""

    def write_pdf(bytes_io):
        pdf = make_pdf()
        bytes_io.write(pdf)

    print("download fit report")

    return send_bytes(write_pdf, "report.pdf")


def make_pdf():
    """Makes a pdf of fit report"""
    mrsim_data = ctx.states["local-mrsim-data.data"]
    button_timestamp = ctx.states["download-fit-report-btn.n_clicks_timestamp"]
    report_timestamp = ctx.states["homepage-html.modified_timestamp"]

    # No report present
    if "report" not in mrsim_data or mrsim_data["report"] is None:
        raise PreventUpdate

    # Button has not been clicked yet
    if button_timestamp is None or button_timestamp == -1:
        raise PreventUpdate

    # report_timestamp is older than button_timestamp
    if report_timestamp is None or report_timestamp < button_timestamp:
        raise PreventUpdate

    # Get html string and remove click number from end
    report_html = ctx.states["homepage-html.data"]
    report_html = report_html[: report_html.rindex(">") + 1]  # remove click number

    # Get css files for pdfkit
    css = path.join(path.dirname(__file__), "../..", "assets", "report.css")

    # Set options for pdfkit
    # Headder includes timestamp, title, version of app and mrsimulator
    # For complete list of options see https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    options = {
        "page-size": "Letter",
        "orientation": "Landscape",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "header-left": f"mrsimulator-app {mrapp_v}      mrsimulator {mrsim_v}",
        "header-font-name": "Helvetica",
        "header-font-size": 9,
        "header-right": "[date] [time]",
        "header-spacing": 4,
    }

    return pdfkit.from_string(report_html, output_path=None, options=options, css=css)
