# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


BUTTONS = {
    # Simulate
    "fac fa-spectrum fa-lg": (
        "Simulates spectrum using values within feature tables. "
        "Will update values in other tabs."
    ),
    # Fit
    "fac fa-chi-squared fa-lg": (
        "Fits simulated spectra to the experimental data and updates parameter values. "
        "Initial values will be those present in the feature tables. "
        "The algorithm used is non-linear least sqaures fit from the LMFIT library."
    ),
    # More Settings
    "fas fa-sliders-h": (
        "Opens advanced options menu for each parameter. "
        "Here the min and max of the parameter can be set as well as an expression "
        "based on the values of other parameters. "
        "For more info on these fields see the LMFIT documentation."
    ),
    # Checkbox
    "fas fa-check-square": (
        "When unchecked, the paraeter will remain constant or be evaluated based on "
        "its given expression under more settings during the fit. "
        "Otherwise the value will vary freely between min and max."
    ),
}


def get_info_row(icon, description):
    return html.Div([html.I(className=icon), html.Div(description)])


def info_modal_ui():
    """Info about features interface"""
    head = dbc.ModalHeader("Least Squares Fitting Interface Info")
    body = info_body()
    foot = dbc.ModalFooter(dbc.Button(id="features-info-modal-close", children="Close"))

    app.clientside_callback(
        "function (n1, n2, is_open) { return !is_open; }",
        Output("features-info-modal", "is_open"),
        Input("features-info-modal-button", "n_clicks"),
        Input("features-info-modal-close", "n_clicks"),
        State("features-info-modal", "is_open"),
        prevent_initial_call=True,
    )

    return dbc.Modal(id="features-info-modal", children=[head, body, foot])


def info_body():
    """Params info modal body"""
    message1 = dcc.Markdown(
        """
        The **mrsimulator** library generates parameter names using the following
        rules:

        ```sys[i].sites[j].attribute1.attribute2```

        will generate the name

        ```sys_i_site_j_attribute1_attribute2```

        where `sys` and `sites` are lists of **Spin System** and **Site** objects,
        respectively.

        More can be found on the [mrsimulator documentation page][1]


        [1]: https://mrsimulator.readthedocs.io/en/latest/api_py/fitting.html
    """
    )
    btn_title = html.B("Button Functions")
    btn_info = html.Div(
        children=[get_info_row(k, v) for k, v in BUTTONS.items()],
        className="modal-body-item",
    )
    return dbc.ModalBody([message1, btn_title, btn_info])


info_modal = info_modal_ui()
