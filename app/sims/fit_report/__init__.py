# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


def header():
    """Report title"""
    return html.H4("Fitting Report", className="card-header")


def report():
    """LMFIT report html div"""
    return html.Iframe(id="fit-report-iframe", hidden=True)


def ui():
    page = html.Div([header(), report()])
    return html.Div(className="left-card", children=page, id="fit_report-body")


fit_report_body = ui()


# Callbacks ============================================================================
@app.callback(
    Output("fit-report-iframe", "srcDoc"),  # html string
    Output("fit-report-iframe", "hidden"),  # bool
    Input("view-fit_report", "n_clicks"),
    State("local-mrsim-data", "data"),
)
def populate_fit_report(n1, data):
    return ["", True] if "report" not in data else [data["report"], False]
