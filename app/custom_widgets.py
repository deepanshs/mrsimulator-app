# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from . import app

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


tooltip_format = {"placement": "bottom", "delay": {"show": 250, "hide": 10}}


def label_with_help_button(label="", help_text="", id=None):
    """A custom label with a help icon.

    Args:
        label: A string label
        help_text: A string message displayed as help message.
        id: The id for the label.
    """
    return html.Div(
        [
            dbc.Label(label, className="formtext pr-1"),
            custom_hover_help(message=help_text, id=f"upload-{id}-url-help"),
        ],
        className="d-flex justify-content-start align-items-center",
    )


def custom_hover_help(message="", id=None):
    """A custom help button.

    Args:
        message: A string message displayed as help message.
        id: The id for the label.
    """
    button = html.Div(
        [
            html.I(
                className="fas fa-question-circle",
                style={"color": "white", "cursor": "pointer"},
            ),
            dbc.Tooltip(message, target=id, **tooltip_format),
        ],
        id=id,
        className="align-self-start",
    )
    return button


def custom_button(
    text="",
    children="",
    icon_classname="",
    id=None,
    tooltip=None,
    module="dbc",
    **kwargs,
):
    """A custom dash bootstrap component button with added tooltip and icon option.

    Args:
        text: A string text displayed on the button.
        icon_classname: A string given as the className, for example, "fas fa-download".
                See https://fontawesome.com for strings.
        id: A string with button id.
        tooltip: A string with tooltip, diplayed when cursor hovers over the button.
        kwargs: additional keyward arguments for dash-bootstrap-component button.
    """

    label = html.Span([text, children], className="hide-label-sm pl-1")
    if icon_classname != "":
        label = html.Span(
            [html.I(className=icon_classname), label],
            className="d-flex align-items-center",
        )
    if tooltip is not None:
        if module == "dbc":
            return dbc.Button(
                [label, dbc.Tooltip(tooltip, target=id, **tooltip_format)],
                id=id,
                **kwargs,
            )
        return html.Button(
            [label, dbc.Tooltip(tooltip, target=id, **tooltip_format)], id=id, **kwargs
        )
    if module == "dbc":
        return dbc.Button(label, id=id, **kwargs)
    return html.Button(label, id=id, **kwargs)


def custom_switch(text="", icon_classname="", id=None, tooltip=None, **kwargs):
    """A custom dash bootstrap component boolean button with added tooltip and icon option.

    Args:
        text: A string text displayed on the button.
        icon_classname: A string given as the className, for example, "fas fa-download".
                See https://fontawesome.com for strings.
        id: A string with button id.
        tooltip: A string with tooltip, diplayed when cursor hovers over the button.
        kwargs: additional keyward arguments for dash-bootstrap-component button.
    """
    button = custom_button(
        text=text, icon_classname=icon_classname, id=id, tooltip=tooltip, **kwargs
    )

    @app.callback(
        Output(id, "active"),
        [Input(id, "n_clicks")],
        [State(id, "active")],
        prevent_initial_call=True,
    )
    def toggle_boolean_button(n, status):
        """Toggle decompose button."""
        if n is None:
            raise PreventUpdate
        return not status

    return button


def custom_card(text, children, id_=None):
    if id_ is None:
        return html.Div([html.H6(text), children], className="scroll-cards")
    return html.Div([html.H6(text), children], id=id_, className="scroll-cards")


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
            dcc.Slider(**kwargs, className="slider-custom"),
        ]
    )

    @app.callback(
        [Output(id_label, "children")],
        [Input(kwargs["id"], "value")],
        prevent_initial_call=True,
    )
    def update_label(value):
        if return_function is None:
            return [value]
        return [return_function(value)]

    return slider


def custom_input_group(
    prepend_label="", append_label=None, input_type="number", **kwargs
):
    """
    A custom dash bootstrap component input-group widget with a prepend-label,
    followed by an Input box, and an append-label.

    Args:
        prepend_label: A string to prepend dash-bootstrap-component Input widget.
        append_label: A string to append dash-bootstrap-component Input widget.
        kwargs: additional keyward arguments for dash-bootstrap-component Input.
    """
    append_label = append_label if append_label is not None else ""

    id_ = kwargs["id"]
    return html.Div(
        [
            html.Label(
                className="label-left", id=f"{id_}-left-label", children=prepend_label
            ),
            dcc.Input(type=input_type, autoComplete="off", **kwargs),
            html.Label(
                className="label-right", id=f"{id_}-right-label", children=append_label
            ),
        ],
        className="input-form",
    )


def custom_collapsible(
    text="", tooltip=None, identity=None, children=None, is_open=True, size="md"
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
    collapse_classname = "panel-collapse collapse in content"
    if is_open:
        collapse_classname += " show"

    layout = [
        html.Button(
            html.Div(
                [text, html.I(className="icon-action fas fa-chevron-down")],
                className="d-flex justify-content-between align-items-center",
            ),
            # tooltip=tooltip,
            # icon=icon,
            style={"color": "black"},
            **{
                "data-toggle": "collapse",
                "data-target": f"#{identity}-collapse",
                "aria-expanded": "true",
            },
            className=f"collapsible btn btn-link btn-block btn-{size}",
        ),
        html.Div(
            id=f"{identity}-collapse", children=children, className=collapse_classname
        ),
    ]

    return html.Div(layout)


def container(text, featured_fields, **kwargs):
    return custom_card(
        text=html.Div(text),
        children=html.Div(featured_fields, className="container"),
        **kwargs,
    )


def collapsable_card(text, id_, featured_fields, hidden_fields):
    # collapsable button
    icon = html.I(className="fas fa-chevron-down")
    tooltip = dbc.Tooltip("Show/Hide Euler angles", target=f"{id_}-collapse-button")
    chevron_down_btn = html.Label([icon, tooltip], id=f"{id_}-collapse-button")

    # collapsed fields
    collapsed_fields = dbc.Collapse(
        hidden_fields, id=f"{id_}-collapse-collapse", is_open=False
    )

    # featured fields
    featured_fields = html.Div(featured_fields)
    content = custom_card(
        text=html.Div([text, chevron_down_btn]),
        children=html.Div([featured_fields, collapsed_fields], className="container"),
    )
    collapsible = dbc.Collapse(content, id=f"{id_}-feature-collapse", is_open=True)

    @app.callback(
        Output(f"{id_}-collapse-collapse", "is_open"),
        [Input(f"{id_}-collapse-button", "n_clicks")],
        [State(f"{id_}-collapse-collapse", "is_open")],
        prevent_initial_call=True,
    )
    def toggle_orientation_collapsible(n, is_open):
        if n is None:
            raise PreventUpdate
        return not is_open

    return collapsible
