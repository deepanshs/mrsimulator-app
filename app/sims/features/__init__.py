# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .fields import features_modal
from .fields import fields
from .fit_modal import fit_info_modal
from app.custom_widgets import custom_button


store = [
    # JSON string of Parameters object
    dcc.Store(id="params-data", storage_type="memory"),
    # Timestamps for triggering fitting callbacks
    dcc.Store(id="trigger-sim", storage_type="memory"),
    dcc.Store(id="trigger-fit", storage_type="memory"),
    dcc.Store(id="trigger-params-update", storage_type="memory"),
    # String for deciding which workflow to run
    dcc.Store(id="which-workflow", storage_type="memory"),
    # # Bool for choosing to update tables to new values
    # dcc.Store(id="update-vals", storage_type="memory"),
    # # Bool for triggering table update only after fit
    # dcc.Store(id="anticipate-table-update", storage_type="memory", data=False),
]
storage_div = html.Div(id="fitting-store", children=store)


def buttons():
    """Static user interface buttons"""
    kwargs = {"outline": True, "color": "dark", "size": "md"}
    sim = custom_button(
        text="Simulate",
        icon_classname="fac fa-spectrum fa-lg",
        id="sim-button",
        tooltip="Simulate spectrum with current parameters",
        **kwargs
    )
    fit = custom_button(
        text="Fit",
        icon_classname="fac fa-chi-squared fa-lg",
        id="fit-button",
        tooltip="Run a least-squared fitting analysis",
        **kwargs
    )
    return dbc.ButtonGroup([sim, fit])


def feature_select():
    """Radio buttons for selecting spin system and method tables"""
    sys_select_div = html.Div(id="sys-feature-select", className="feature-select")
    mth_select_div = html.Div(id="mth-feature-select", className="feature-select")

    sys_page_left = html.Span(
        "<", id="page-sys-feature-left", className="btn-link hidden"
    )
    sys_page_right = html.Span(
        ">", id="page-sys-feature-right", className="btn-link hidden"
    )
    mth_page_left = html.Span(
        "<", id="page-mth-feature-left", className="btn-link hidden"
    )
    mth_page_right = html.Span(
        ">", id="page-mth-feature-right", className="btn-link hidden"
    )

    sys_btns = html.Div(
        [sys_page_left, sys_select_div, sys_page_right], className="feature-buttons"
    )
    mth_btns = html.Div(
        [mth_page_left, mth_select_div, mth_page_right], className="feature-buttons"
    )

    sys_head = html.Div([html.H6("Spin Systems"), sys_btns], className="feature-select")
    mth_head = html.Div([html.H6("Methods"), mth_btns], className="feature-select")
    return html.Div([sys_head, mth_head], id="feature-select-div")


def features_header():
    """Header for features tab"""
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
    page = html.Div(
        [
            features_header(),
            feature_select(),
            fields,
            fit_info_modal,
            features_modal,
            storage_div,
        ]
    )
    return html.Div(className="left-card", children=page, id="features-body")


features_body = ui()
