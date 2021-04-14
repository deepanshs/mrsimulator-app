# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from lmfit.printfuncs import fitreport_html_table

from app import app
# from mrsimulator import Simulator


css_str = '*{font-family:"Helvetica",sans-serif;}td{padding: 0 8px}'


def ui():
    body = html.Div(id="params-report-div", children=[])
    return html.Div(children=[body], id="fitting-report")


def make_html_string(result, css):
    """Constructs the html string with proper formatting for fit report iframe
    Params:
        result: Minimizer object
        css: css string
    """
    html_str = fitreport_html_table(result)
    style_str = f"<html><head><style>{css}</style></head>"
    return style_str + html_str + "</html>"


report = ui()


# Callbacks ===================================================================
# Fitting callback triggered by 'run-fitting-button'
# Simulation callback triggered by 'simulate-button'
@app.callback(
    Output("params-report-div", "children"),
    Output("params-report-div", "hidden"),
    Input("fitting-report-data", "data"),
    prevent_initial_call=True,
)
def update_report(data):
    """Updates report div when fitting data is changed"""
    if data is None:
        return "", True

    frame = html.Iframe(sandbox="", srcDoc=data, className="fit-report-iframe")
    return frame, False


# Not being used since dash-ext is not working
# @app.callback(
#     Output("fitting-report-data", "data"),
#     Input("run-fitting-button", "n_clicks"),
#     State("params-data", "data"),
# )
# def run_spectrum_fitting(n1, params_data):
#     """Runs fitting routine and _____"""
#     # 1) Run Fitting Routine
#     # 2) Plot fitted spectrum?
#     # 3) Other things here
#     #
#     # Currently only returns a test string
#     return make_html_string(None, css_str)
