# -*- coding: utf-8 -*-
# import json
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
import dash_html_components as html

# from app import app

# from dash import callback_context as ctx
# from dash.dependencies import ALL
# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.dependencies import State
# from dash.exceptions import PreventUpdate


def report_header():
    return html.Div(html.H4("Fitting Report"))


def report_body():
    return html.Div(id="params-report-div", children=[])


def ui():
    """Read only div of fitting report data"""
    return html.Div(
        children=[report_header(), report_body()],
        id="fitting-report",
        # additional fields needed?
    )


report = ui()


# Callbacks ===================================================================
# @app.callback(
#     Output("params-report-div", "children"),
#     Input("fitting-report-data", "data"),
# )
# def update_report(data):
#     """Updates report div when fitting data is changed"""
#     # Can this use the built in fuction 'lmfit.printfuncs.fitreport_html_table'
#     # where fitting-report-data is just a html string?
#     # Alternative is formatting into custom layout
#     pass
