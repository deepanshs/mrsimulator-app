# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import MATCH
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
        " least squares algorithm. Spectrum will automatically update after and"
        " clicking the refresh button will update the values."
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
    # TODO: Table of icons and function
    return dbc.ModalBody([message1, btn_title, btn_table])


fit_info_modal = info_modal_ui()


def make_modal(key, vals):
    """Constructs single modal for given param

    Params:
        key: str title of Parameter
        vals: dict of Parameter values

    Returns:
        dbc.Modal
    """
    # param_dict: singular Parameter dict representation

    # print(type(param_dict))
    # print(param_dict)

    # key, vals = param_dict.items()
    input_args = {"type": "number", "autoComplete": "off"}
    min_id = {"name": f"{key}-min", "kind": "min"}
    max_id = {"name": f"{key}-max", "kind": "max"}
    expr_id = {"name": f"{key}-expr", "kind": "expr"}
    modal_id = {"kind": "modal", "parrent": key}

    # TODO: Adjust apperance of modal inputs using css
    min_ = html.Div(
        ["Minimum", dcc.Input(value=vals["min"], id=min_id, **input_args)],
        className="input-form fit-modal",
    )
    max_ = html.Div(
        ["Maximum", dcc.Input(value=vals["max"], id=max_id, **input_args)],
        className="input-form fit-modal",
    )
    expr = html.Div(
        ["Expression", dbc.Textarea(
            value=vals["expr"], id=expr_id, className="fit-expr-text")],
        className="input-form fit-modal fit-expr",
    )

    head = dbc.ModalHeader(html.B(key))
    body = dbc.ModalBody([min_, max_, expr])

    return dbc.Modal([head, body], id=modal_id)


# Opens/closes params modal
app.clientside_callback(
    "function (n1, is_open) { if(n1 == null) { return false; } return !is_open; }",
    Output({"kind": "modal", "parrent": MATCH}, "is_open"),
    Input({"kind": "modal-btn", "parrent": MATCH}, "n_clicks"),
    State({"kind": "modal", "parrent": MATCH}, "is_open"),
    prevent_initial_call=True,
)
