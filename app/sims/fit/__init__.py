# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .fields import fields
from .fit_modal import fit_info_modal
from app.custom_widgets import custom_button


store = [
    # JSON string of Parameters object
    dcc.Store(id="params-data", storage_type="memory"),
    # Timestamps for triggering fitting callbacks
    dcc.Store(id="trigger-sim", storage_type="memory"),
    dcc.Store(id="trigger-fit", storage_type="memory"),
    # dcc.Store(id="trigger-table-update", storage_type="memory"),
]
storage_div = html.Div(id="fitting-store", children=store)


def buttons():
    """Static user interface buttons"""
    kwargs = {"outline": True, "color": "dark", "size": "md"}
    refresh = custom_button(
        id="refresh-button",
        # text="Reset",
        icon_classname="fas fa-sync-alt",
        tooltip="Refresh parameter values.",
        **kwargs
    )
    simulate = custom_button(
        id="simulate-button",
        # text="Simulate",
        icon_classname="far fa-chart-bar",
        tooltip="Simulate a spectrum using the current values.",
        **kwargs
    )
    fit = custom_button(
        id="run-fitting-button",
        # text="Fit",
        icon_classname="fas fa-compress-alt",
        tooltip="Run least-squares minimization.",
        **kwargs
    )
    return dbc.ButtonGroup([refresh, simulate, fit])


def table_select():
    """Radio buttons for selecting spin system and method tables"""
    sys_page_btns = html.Div(
        children=[
            html.Button("Left", id="page-sys-left-btn"),
            html.Button("Right", id="page-sys-right-btn"),
        ]
    )
    mth_page_btns = html.Div(
        children=[
            html.Button("Left", id="page-mth-left-btn"),
            html.Button("Right", id="page-mth-right-btn"),
        ]
    )

    sys_slct_btns = dbc.RadioItems(
        id={"key": "table-select-btn", "title": "Spin System"},
        className="table-select btn-group",
        labelClassName="btn btn-secondary",
        labelCheckedClassName="active",
        labelStyle={"display": "inline-block"},
        options=[{"label": 0, "value": 0}],
        value=0,
    )
    mth_slct_btns = dbc.RadioItems(
        id={"key": "table-select-btn", "title": "Method"},
        className="table-select btn-group",
        labelClassName="btn btn-secondary",
        labelCheckedClassName="active",
        labelStyle={"display": "inline-block"},
        options=[{"label": 0, "value": 0}],
        value=0,
    )
    # TODO: Implement total pages and page index
    sys_head = html.Div(
        [html.H6("Spin Systems"), sys_page_btns, sys_slct_btns], className="card-header"
    )
    mth_head = html.Div(
        [html.H6("Methods"), mth_page_btns, mth_slct_btns], className="card-header"
    )
    return html.Div([sys_head, mth_head])


def fit_header():
    """Header for fitting tab"""
    help_button = html.Div(
        html.I(className="fas fa-question-circle pl-1 fa-lg"),
        id="fit-info-modal-button",
        style={"cursor": "pointer"},
    )
    icon = html.I(className="fas fa-bullseye fa-lg")
    text = html.H4("Features", className="hide-label-sm")
    title = html.Div([icon, text, help_button])
    return html.Div([title, buttons()], className="card-header")


def ui():
    page = html.Div([fit_header(), table_select(), fields, fit_info_modal, storage_div])
    return html.Div(className="left-card", children=page, id="fit-body")


fit_body = ui()
