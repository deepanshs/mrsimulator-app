# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from .fields import fields


store = [
    # JSON string of Parameters object
    dcc.Store(id="params-data", storage_type="session"),  # Change back to memory
    # Timestamps for triggering sim/fit in importer
    dcc.Store(id="trigger-sim", storage_type="memory"),
    dcc.Store(id="trigger-fit", storage_type="memory"),
]
storage_div = html.Div(id="fitting-store", children=store)


def fit_header():
    head = [html.H4("Fitting Parameters")]
    return html.Div(head)


def ui():
    page = [fit_header(), fields, storage_div]
    return html.Div(className="left-card", children=page, id="fit-body")


fit_body = ui()
