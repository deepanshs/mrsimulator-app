# -*- coding: utf-8 -*-
import dash_html_components as html


def header():
    """Report title"""
    return html.H4("Fitting Report", className="card-header")


def report():
    """LMFIT report html div"""
    return html.Iframe(id="fit-report-iframe", sandbox="", hidden=True)


def ui():
    page = html.Div([header(), report()])
    return html.Div(className="left-card", children=page, id="fit_report-body")


fit_report_body = ui()
