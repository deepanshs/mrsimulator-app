# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output

from app import app


def header():
    """Report title"""
    return html.Div(
        [
            html.H4("Fitting Report"),
            html.Button("Download Report", id="download-fit-report"),
        ],
        className="card-header",
    )


# def report():
#     """LMFIT report html div"""
#     return html.Div(
#         html.Iframe(id="fit-report-iframe", hidden=True), className="flex-div"
#     )


def report():
    """Div for LMFIT report tables"""
    return html.Div(
        children="This page will automatically update after a fit.",
        id="fit-report-table-div",
    )


def ui():
    page = html.Div([header(), report()])
    return html.Div(className="left-card", children=page, id="fit_report-body")


fit_report_body = ui()


# Callbacks ============================================================================
# @app.callback(
#     Output("fit-report-iframe", "srcDoc"),  # html string
#     Output("fit-report-iframe", "hidden"),  # bool
#     Input("view-fit_report", "n_clicks"),
#     State("local-mrsim-data", "data"),
# )
# def populate_fit_report(n1, data):
#     # TODO: Is this callback needed?
#     # TODO: Better formatting on report display in app?
#     # TODO: Display fit report on load of file with report
#     return ["", True] if "report" not in data else [data["report"], False]


# clientside callback for updating info
# May need to trigger from local-processed data if local-mrsim-data does not work
app.clientside_callback(
    ClientsideFunction(namespace="report", function_name="updateFitReport"),
    Output("temp9", "children"),
    Input("local-mrsim-data", "data"),
    prevent_initial_call=True,
)

# callback for downloading report
