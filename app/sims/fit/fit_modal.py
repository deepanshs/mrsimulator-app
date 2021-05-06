# -*- coding: utf-8 -*-
# import json
# from datetime import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app

# from dash import callback_context as ctx
# from dash import no_update
# from dash.dependencies import ALL
# from dash.exceptions import PreventUpdate
# from lmfit import Parameters
# from mrsimulator import parse
# from mrsimulator.utils.spectral_fitting import make_LMFIT_params


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
        More info on the [mrsimulator documentation page][1]


        [1]: https://mrsimulator.readthedocs.io/en/latest/api_py/fitting.html
    """
    )
    btn_title = html.B("Button Functions")
    # Table of icons and function
    return dbc.ModalBody([message1, btn_title])


fit_info_modal = info_modal_ui()
