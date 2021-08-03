# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html


def get_icon_with_description(icon, description):
    return html.Tr([html.Td(html.I(className=icon)), html.Td(description)])


help_message = html.Table(
    [
        get_icon_with_description(
            "fas fa-arrows-alt-v",
            (
                "Scales the maximum amplitude to one, applies to both the ",
                "simulation and external data (if present).",
            ),
        ),
        get_icon_with_description(
            "fac fa-decompose", "Show spectrum from individual spin systems."
        ),
    ]
)

message_1 = (
    "You may additionally load and compare experimental data by dragging and dropping ",
    "the respective .csdf file on to this graph area.",
)

simulation_help = dbc.Modal(
    [
        dbc.ModalHeader("Simulation"),
        dbc.ModalBody(
            [
                html.P("The simulations are shown here."),
                html.P(message_1),
                html.B("Button Functions"),
                help_message,
            ]
        ),
    ],
    id="modal-simulation-help",
    role="document",
    className="modal-dialog",
)
