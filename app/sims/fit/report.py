# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc

from app import app


def report_header():
    return html.Div(html.H4("Fitting Report"))

def report_body():
    """Generates read-only display for fitting report"""

def ui():
    """Read only div of fitting report data"""
    return html.Div(
        children=[report_header()],
        id="fitting-report",
        # additional fields needed?
    )

report = ui()


# Callbacks ===================================================================
@app.callback(

)
def update_report():
    pass