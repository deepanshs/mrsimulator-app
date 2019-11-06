# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


tooltip_format = {"placement": "bottom", "delay": {"show": 250, "hide": 10}}


def label_with_help_button(label="", help_text="", id=None):
    return html.Div(
        [
            dbc.Label(label, className="formtext"),
            custom_hover_help(message=help_text, id=f"upload-{id}-url-help"),
        ],
        className="d-flex justify-content-start",
    )


def custom_hover_help(message="", id=None):
    button = html.Div(
        [
            html.I(className="fas fa-question-circle", style={"color": "white"}),
            dbc.Tooltip(message, target=id, **tooltip_format),
        ],
        id=id,
        className="align-self-start",
    )
    return button


def custom_button(text="", icon="", id=None, tooltip=None, **kwargs):
    """A custom dash bootstrap component button with added tooltip and icon option.

    Args:
        text: A string text displayed on the button.
        icon: A string given as the className, for example, "fas fa-download".
                See https://fontawesome.com for strings.
        id: A string with button id.
        tooltip: A string with tooltip, diplayed when cursor hovers over the button.
        kwargs: additional keyward arguments for dash-bootstrap-component button.
    """
    if icon == "":
        label = html.Span(text, className="d-flex justify-content-between")
    else:
        if isinstance(text, list):
            label = html.Span(
                [html.I(className=icon), *text],
                className="d-flex justify-content-between",
            )
        else:
            label = html.Span(
                [html.I(className=icon), text],
                className="d-flex justify-content-between",
            )

    if tooltip is not None:
        return dbc.Button(
            [label, dbc.Tooltip(tooltip, target=id, **tooltip_format)], id=id, **kwargs
        )
    else:
        return dbc.Button(label, id=id, **kwargs)


def custom_switch(text="", icon="", id=None, tooltip=None, **kwargs):
    """A custom dash bootstrap component boolean button with added tooltip and icon option.

    Args:
        text: A string text displayed on the button.
        icon: A string given as the className, for example, "fas fa-download".
                See https://fontawesome.com for strings.
        id: A string with button id.
        tooltip: A string with tooltip, diplayed when cursor hovers over the button.
        kwargs: additional keyward arguments for dash-bootstrap-component button.
    """
    button = custom_button(text=text, icon=icon, id=id, tooltip=tooltip, **kwargs)

    # decompose button callback method
    @app.callback(
        Output(f"{id}", "active"),
        [Input(f"{id}", "n_clicks")],
        [State(f"{id}", "active")],
    )
    def toggle_boolean_button(n, status):
        """Toggle decompose button."""
        if n is None:
            raise PreventUpdate

        new_status = True
        if bool(status):
            new_status = False
        return new_status

    return button


def custom_slider(label="", return_function=None, **kwargs):
    """
        A custom dash bootstrap component slider with added components-
        slider-label, slider-bar, and a slider-text reflecting the current value
        of the slider.

        Args:
            label: A string with the label.
            return_function: This function will be applied to the current
                value of the slider before updating the slider-text.
            kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    id_label = kwargs["id"] + "_label"
    slider = html.Div(
        [
            html.Div(
                [label, dbc.FormText(id=id_label)],
                className="d-flex justify-content-between",
            ),
            html.Div([dcc.Slider(**kwargs), html.P()], style={"paddingBottom": "10px"}),
        ],
        className="my-auto d-flex flex-column",
    )

    @app.callback([Output(id_label, "children")], [Input(kwargs["id"], "value")])
    def update_label(value):
        if return_function is None:
            return [value]
        else:
            return [return_function(value)]

    return slider


def custom_input_group(prepend_label="", append_label="", **kwargs):
    """
        A custom dash bootstrap component input-group widget with a prepend-label,
        followed by an Input box, and an append-label.

        Args:
            prepend_label: A string to prepend dash-bootstrap-component Input widget.
            append_label: A string to append dash-bootstrap-component Input widget.
            kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    group = [
        html.Div(
            html.Span(prepend_label, className="input-group-text"),
            className="input-group-prepend",
        ),
        dcc.Input(
            type="number",
            # pattern="?[0-9]*\\.?[0-9]",
            className="form-control",
            **kwargs,
        ),
    ]
    if append_label != "":
        return html.Div(
            [
                *group,
                html.Div(
                    html.Span(append_label, className="input-group-text"),
                    className="input-group-append",
                ),
            ],
            className="input-group d-flex",
        )
    else:
        return html.Div(group, className="input-group p1 d-flex")


def custom_collapsible(
    text="",
    tooltip=None,
    # icon="",
    identity=None,
    children=None,
    is_open=True,
    size="md",
    button_classname="collapsible-handle ripple",
    collapse_classname="",
    **kwargs,
):
    """
        A custom collapsible widget with a title and a carret dropdown icon.

        Args:
            text: A string with the title of the collapsible widget.
            identity: An id for the widget.
            children: A dash-bootstrap componets or a list of components.
            is_open: Boolean. If false, the widget is collapsed on initial render.
            size: String, "sm, md, lg".
            button_classname: String. css classnames for button toggler.
            collapse_classname: String. css classnames for collapsible.
    """
    layout = [
        custom_button(
            text=[text, html.I(className="icon-action fas fa-chevron-down")],
            tooltip=tooltip,
            # icon=icon,
            color="link",
            size=size,
            id=f"{identity}-button",
            block=True,
            style={"color": "black"},
            className=button_classname,
        ),
        dbc.Collapse(
            id=f"{identity}-collapse",
            children=children,
            is_open=is_open,
            className=collapse_classname,
        ),
    ]

    @app.callback(
        Output(f"{identity}-collapse", "is_open"),
        [Input(f"{identity}-button", "n_clicks")],
        [State(f"{identity}-collapse", "is_open")],
    )
    def toggle_frame(n, is_open):
        if n:
            return not is_open
        return is_open

    return html.Div(layout)


# def custom_dropdown():
#     layout = html.Div(
#         className="btn-group",
#         children=[
#             html.A(
#                 type="button", color="primary",
#                 className="dropdown-toggle waves-light"
#             ),
#             html.Div(
#                 className="dropdown-menu dropdown-primary",
#                 children=[
#                     html.A("CSDM", className="dropdown-item", href="#"),
#                     html.A("CSV", className="dropdown-item", href="#"),
#                 ],
#             ),
#         ],
#     )
#     return layout
