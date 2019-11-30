# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html


def get_icon_with_description(icon, description):
    return html.Tr(
        [html.Td(html.I(className=icon)), html.Td(description)],
        # className="d-flex align-items-center justify-content-between p-1",
    )


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
            "fac fa-decompose", "Show spectrum from individual isotopomers."
        ),
        get_icon_with_description(
            "fas fa-download", "Download dataset as `.csdf` or `.csv` format."
        ),
    ]
)

message_1 = (
    "You may additionally load an isotopomers or .csdf file by dragging ",
    "and dropping the respective file on to this area.",
)

simulation_help = dbc.Modal(
    [
        dbc.ModalHeader("Simulation"),
        dbc.ModalBody(
            [
                html.P("The result of the line-shape simulation is shown here."),
                html.P(message_1),
                html.P("Clicking/tapping the icons does the following"),
                help_message,
            ]
        ),
    ],
    id="modal-simulation-help",
    role="document",
    className="modal-dialog",
)
