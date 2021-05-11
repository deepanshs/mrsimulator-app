# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


BUTTONS = {
    # Refresh Button
    "fas fa-sync-alt": (
        "Refreshes the values in fit tables from input values within other tabs of the"
        " app."
    ),
    # Simulate Button
    "far fa-chart-bar": (
        "Simulates the spectrum(s) for the given set of input parameters."
    ),
    # Run Fit Button
    "fas fa-compress-alt": (
        "Fits the parameters of the simulated spectrum to the experiment data using the"
        " least squares algorithm. Spectrum and values will automatically update after"
        " the fitting routine and a report will appear below."
    ),
}


def get_info_row(icon, description):
    return html.Tr([html.Td(html.I(className=icon)), html.Td(description)])


def info_modal_ui():
    """Info about fitting interface"""
    head = dbc.ModalHeader("Least Squares Fitting Interface Info")
    body = info_body()
    foot = dbc.ModalFooter(dbc.Button(id="fit-info-modal-close", children="Close"))

    app.clientside_callback(
        "function (n1, n2, is_open) { return !is_open; }",
        Output("fit-info-modal", "is_open"),
        Input("fit-info-modal-button", "n_clicks"),
        Input("fit-info-modal-close", "n_clicks"),
        State("fit-info-modal", "is_open"),
        prevent_initial_call=True,
    )

    return dbc.Modal(id="fit-info-modal", children=[head, body, foot])


def info_body():
    """Params info modal body"""
    message1 = dcc.Markdown(
        """
        The **mrsimulator** library generates parameter names using the following
        syntax:

        ```sys_i_site_j_attribute1_attribute2```

        is equivalent to

        ```sys[i].sites[j].attribute1.attribute2```

        where `sys` represents a **Spin System** object.
        More info is on the [mrsimulator documentation page][1]


        [1]: https://mrsimulator.readthedocs.io/en/latest/api_py/fitting.html
    """
    )
    btn_title = html.B("Button Functions")
    btn_table = html.Table([get_info_row(k, v) for k, v in BUTTONS.items()])
    # Table of icons and function
    return dbc.ModalBody([message1, btn_title, btn_table])


fit_info_modal = info_modal_ui()
