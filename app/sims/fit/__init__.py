# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.dependencies import ALL
from dash.dependencies import MATCH

from .fields import fields
from .report import report
from app import app
from app.custom_widgets import custom_button


store = [
    # fitting parameters and report dictonary data
    dcc.Store(id="stored-parameters-data", storage_type="session"),
    dcc.Store(id="visible-parameters-data", storage_type="memory"),
    dcc.Store(id="fitting-report-data", storage_type="session"),
]
storage_div = html.Div(store)


# def load_parameters_ui():
#     # Link/request for download?
#     load_button = custom_button(
#         icon_classname="fas fa-pencil-alt",  # Change to appropriate icon
#         tooltip="Load Fitting Parameters",
#         id="load-params-button",
#         className="icon-button",
#         module="html",  # Correct module?
#     )
#     # Clientside callback
#     return html.Div([load_button])

def fit_header():
    head = [
        html.H4("Fitting Parameters"),
        # Additional elements here
    ]
    return html.Div(head)  # Add styling if needed


def ui():
    page = [
        fit_header(),
        fields,
        report,
        storage_div,
    ]

    return html.Div(
        className="left-card",
        children=page,
        id="fit-body",
    )


fit_body = ui()
