# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output

from .app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


def custom_slider(label="", return_function=None, **kwargs):
    """Custom slider consists of three block -
        1) A label for the slider
        2) Slider bar
        3) A label reflecting the current value of the slider position

        Args:
            label: String with label
            return_function: This function will be applied to the current
                slider value before updating the label.
            kwargs: keyward arguments for dash bootstrap component Input
    """
    id_label = kwargs["id"] + "_label"
    slider = dbc.FormGroup(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Label(label, color="dark", style={"float": "left"}), width=9
                    ),
                    dbc.Col(dbc.FormText(id=id_label, style={"float": "right"})),
                ]
            ),
            dcc.Slider(**kwargs),
        ]
    )

    @app.callback([Output(id_label, "children")], [Input(kwargs["id"], "value")])
    def update_label(value):
        if return_function is None:
            return [value]
        else:
            return [return_function(value)]

    return slider


def custom_input_group(prepend_label="", append_label="", **kwargs):
    """Custom input group consists of three block -
        1) A prepend label
        2) An Input box
        3) A append label

        Args:
            prepend_label: String to prepend
            append_label: String to append
            kwargs: keyward arguments for dash bootstrap component Input
    """
    if "step" not in kwargs.keys():
        kwargs["step"] = 1e-5
    return dbc.InputGroup(
        [
            dbc.InputGroupAddon(prepend_label, addon_type="prepend"),
            dbc.Input(
                # inputMode="latin",
                type="number",
                # pattern="?[0-9]*\\.?[0-9]",
                **kwargs,
            ),
            dbc.InputGroupAddon(append_label, addon_type="append"),
        ],
        # size="sm",
    )


def custom_collapsible(text, id, children=None, hide=True):
    if hide:
        classname = "filter-content collapse hide"
    else:
        classname = "filter-content collapse show"

    return html.Div(
        [
            html.Div(
                html.A(
                    [
                        html.H6(
                            [text, html.I(className="icon-action fas fa-chevron-down")]
                        )
                    ],
                    href="#",
                    **{
                        "data-toggle": "collapse",
                        "data-target": f"#{id}",
                        "aria-expanded": True,
                    },
                    style={"color": "black"},
                ),
                className="my-subcard",
                style={
                    "padding-top": 4,
                    "padding-bottom": 1,
                    "padding-left": 10,
                    "padding-right": 6,
                },
            ),
            html.Div(
                className=classname,
                id=id,
                children=html.Div([*children, html.P()]),
                # style={"padding-bottom": 10},
            ),
        ],
        style={
            "border-bottom": "1px solid rgb(214, 214, 214)",
            # "background": "#fdfdfd54",
        },
    )
