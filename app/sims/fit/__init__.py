# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from .fields import fields
from .report import report


store = [
    # fitting parameters and report dictonary data
    dcc.Store(id="params-data", storage_type="memory"),  # JSON str of lmfit obj
    dcc.Store(id="fitting-report-data", storage_type="session"),
]
storage_div = html.Div(store)


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
