# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.dimension.post_simulation_widgets import gaussian_linebroadening_widget
from app.dimension.simulation_widgets import coordinate_grid
from app.dimension.simulation_widgets import environment
from app.modal.advance_settings import advance_settings

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# Advance settings ------------------------------------------------------------------ #
advance_setting_button = custom_button(
    icon_classname="fas fa-cog",
    id="advance_setting",
    tooltip="Advanced settings",
    outline=True,
    color="dark",
)
dimension_toolbar = dbc.Row([dbc.Col([advance_setting_button, advance_settings])])

column_response = {"xs": "12", "sm": "12", "md": "6", "lg": "12", "xl": "12"}


# dimension parameters
def make_dimension(i):
    row1 = dbc.Row(
        [
            dbc.Col(
                custom_collapsible(
                    text="Environment",
                    identity=f"environment_id-{i}",
                    children=environment(i),
                ),
                **column_response,
            ),
            dbc.Col(
                custom_collapsible(
                    text="Coordinate grid",
                    identity=f"coordinate_grid_id-{i}",
                    children=coordinate_grid(i),
                )
            ),
        ]
    )
    row2 = dbc.Row(
        [
            dbc.Col(
                custom_collapsible(
                    text="Line broadening",
                    identity=f"post_simulation_id-{i}",
                    children=gaussian_linebroadening_widget(i),
                    hide=False,
                ),
                **column_response,
            )
        ]
    )
    dimension_contents = dbc.Tab(label=f"Index-{i}", children=[row1, row2])

    return dimension_contents


# dimension layout
dimension_body = html.Div(
    className="v-100 my-card",
    children=[
        html.Div(
            [
                html.H4("Dimensions", style={"fontWeight": "normal"}, className="pl-2"),
                dimension_toolbar,
            ],
            className="d-flex justify-content-between p-2",
        ),
        dbc.Tabs([make_dimension(i) for i in range(2)]),
    ],
    id="dimension-body",
)
