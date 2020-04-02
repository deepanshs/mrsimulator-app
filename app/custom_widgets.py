# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

# import dash_daq as daq

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


def custom_button(text="", icon_classname="", id=None, tooltip=None, **kwargs):
    """A custom dash bootstrap component button with added tooltip and icon option.

    Args:
        text: A string text displayed on the button.
        icon_classname: A string given as the className, for example, "fas fa-download".
                See https://fontawesome.com for strings.
        id: A string with button id.
        tooltip: A string with tooltip, diplayed when cursor hovers over the button.
        kwargs: additional keyward arguments for dash-bootstrap-component button.
    """

    label = html.Span(text, className="hide-label-sm pl-1")
    if icon_classname != "":
        label = html.Span(
            [html.I(className=icon_classname), label],
            className="d-flex align-items-center",
        )
    if tooltip is not None:
        return dbc.Button(
            [label, dbc.Tooltip(tooltip, target=id, **tooltip_format)], id=id, **kwargs
        )
    return dbc.Button(label, id=id, **kwargs)


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

    @app.callback(Output(id, "active"), [Input(id, "n_clicks")], [State(id, "active")])
    def toggle_boolean_button(n, status):
        """Toggle decompose button."""
        if n is None:
            raise PreventUpdate
        return not status

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
            dcc.Slider(**kwargs, className="slider-custom"),
        ]
    )

    @app.callback([Output(id_label, "children")], [Input(kwargs["id"], "value")])
    def update_label(value):
        if return_function is None:
            return [value]
        else:
            return [return_function(value)]

    return slider


# def custom_input_group(prepend_label="", append_label=None, **kwargs):
#     """
#         A custom dash bootstrap component input-group widget with a prepend-label,
#         followed by an Input box, and an append-label.

#         Args:
#             prepend_label: A string to prepend dash-bootstrap-component Input widget.
#             append_label: A string to append dash-bootstrap-component Input widget.
#             kwargs: additional keyward arguments for dash-bootstrap-component Input.
#     """
#     append_label = append_label if append_label is not None else ""

#     group = [
#         dcc.Input(
#             type="number",
#             autoComplete="off",
#             name="name",
#             pattern="?[0-9]*\\.?[0-9]",
#             className="",
#             required="required",
#             **kwargs,
#         ),
#         html.Label(
#             className="label-name",
#             htmlFor="name",
#             children=html.Span(prepend_label, className="content-name"),
#         ),
#         html.Label(
#             className="label-name-after",
#             htmlFor="name",
#             children=html.Span(append_label, className="content-name-after"),
#         ),
#     ]
#     return html.Div(group, className="input-form")


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

    return html.Div(
        [
            html.Label(className="label-left", children=prepend_label),
            dcc.Input(type=input_type, autoComplete="off", **kwargs),
            html.Label(className="label-right", children=append_label),
        ],
        className="input-form-2",
    )


# def custom_input_group(prepend_label="", append_label=None, **kwargs):
#     """
#         A custom dash bootstrap component input-group widget with a prepend-label,
#         followed by an Input box, and an append-label.

#         Args:
#             prepend_label: A string to prepend dash-bootstrap-component Input widget.
#             append_label: A string to append dash-bootstrap-component Input widget.
#             kwargs: additional keyward arguments for dash-bootstrap-component Input.
#     """
#     # if pattern == "pos_dec_only":
#     #     pattern_re = r"^[0-9]\d*(\.\d+)?$"
#     # elif pattern == "pos_neg_dec":
#     #     pattern_re = r"^-?[0-9]\d*(\.\d+)?$"
#     # elif pattern == "scientific":
#     #     pattern_re = r"(^[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$"
#     #     # pattern_re = r"/[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?/"
#     # else:
#     #     pattern_re = pattern

#     group = [
#         html.Div(
#             html.Span(prepend_label, className="input-group-text"),
#             className="input-group-prepend",
#         ),
#         dcc.Input(
#             type="number",
#             # pattern="?[0-9]*\\.?[0-9]",
#             className="form-control",
#             **kwargs,
#         ),
#     ]

#     # @app.callback(Output(kwargs["id"], "step"), [Input(kwargs["id"], "value")])
#     # def update_steps(value):
#     #     if not isinstance(value, (float, int)):
#     #         raise PreventUpdate
#     #     val = str(value).split(".")
#     #     if len(val) == 1:
#     #         return 1
#     #     return 10 ** -len(val[1])

#     if append_label is not None:
#         return html.Div(
#             [
#                 *group,
#                 html.Div(
#                     html.Span(append_label, className="input-group-text"),
#                     className="input-group-append",
#                 ),
#             ],
#             className="input-group input-group-sm d-flex",
#         )
#     else:
#         return html.Div(group, className="input-group input-group-sm d-flex")


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
    options = {"data-toggle": "collapse", "data-target": f"#{identity}-collapse"}
    options["aria-expanded"] = str(is_open)

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

label_dictionary = {
    "isotope": "Isotope",
    "shielding_symmetric": "Symmetric Shielding",
    "quadrupolar": "Quadrupolar",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "zeta": "Anisotropy (ζ)",
    "eta": "Asymmetry (η)",
    "isotropic_chemical_shift": "Isotropic shift (δ)",
    "Cq": "Coupling constant (Cq)",
}
default_unit = {
    "isotope": "",
    "isotropic_chemical_shift": "ppm",
    "Cq": "MHz",
    "zeta": "ppm",
    "eta": "",
    "alpha": "deg",
    "beta": "deg",
    "gamma": "deg",
}


def attribute_value_pair(key, value, space):
    return html.Div(
        f"{label_dictionary[key]}: {value} {default_unit[key]}",
        className=f"pl-{space}"
        # [html.Div(label_dictionary[key]), html.Div(f"{value} {default_unit[key]}"),],
        # className=f"pl-{space} d-flex justify-content-between",
    )


def print_info(json_data):
    output = []
    keys = json_data.keys()

    if "isotopomers" not in keys:
        return html.Div()

    for i, isotopomer in enumerate(json_data["isotopomers"]):
        local = [html.Br()]
        name = "" if "name" not in isotopomer else isotopomer["name"]

        local.append(html.H5(f"Isotopomer {i}: {name}", className=""))

        if "sites" in isotopomer:
            for site in isotopomer["sites"]:
                for site_attribute, val in site.items():
                    if isinstance(val, dict):
                        local.append(
                            html.Div(
                                f"{label_dictionary[site_attribute]}", className="pl-2"
                            )
                        )
                        for key, value in val.items():
                            if value is not None:
                                value = value * 1e-6 if key == "Cq" else value
                                local.append(attribute_value_pair(key, value, 4))
                    else:
                        local.append(attribute_value_pair(site_attribute, val, 2))
        local.append(html.Br())
        output.append(html.Li(local))

    return html.Div(html.Ul(output), className="display-form")
