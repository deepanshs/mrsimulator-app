# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.dimension.post_simulation_widgets import gaussian_linebroadening_widget
from app.dimension.simulation_widgets import coordinate_grid
from app.dimension.simulation_widgets import environment
from app.modal.advance_settings import advance_settings

# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.dependencies import State
# from dash.exceptions import PreventUpdate
# from app.app import app


__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# Advance settings ------------------------------------------------------------------ #
advance_setting_button = custom_button(
    icon_classname="fas fa-cog",
    id="advance_setting",
    tooltip="Advanced setting",
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
                [
                    custom_collapsible(
                        text="Line broadening",
                        identity=f"post_simulation_id-{i}",
                        children=gaussian_linebroadening_widget(i),
                        hide=False,
                    ),
                    custom_collapsible(
                        text="Coordinate grid",
                        identity=f"coordinate_grid_id-{i}",
                        children=coordinate_grid(i),
                        is_open=False,
                    ),
                ],
                **column_response,
            ),
        ]
    )
    dimension_contents = dbc.Tab(label=f"Index-{i}", children=[row1])

    return dimension_contents


# dimension layout
dimension_body = html.Div(
    className="v-100 my-card",
    children=[
        html.Div(
            [
                html.H4(
                    "Dimensions",
                    style={"fontWeight": "normal"},
                    className="pl-2",
                    id="dimension-card",
                ),
                # dbc.Button("+", id="add-dimension"),
                dimension_toolbar,
            ],
            className="d-flex justify-content-between p-2",
        ),
        dbc.Tabs(children=[make_dimension(i) for i in range(1)], id="dimension-tabs"),
    ],
    id="dimension-body",
)

dimension_body_card = html.Div(dimension_body, id="dimension-body-card")


# @app.callback(
#     [Output("dimension-tabs", "children"),
#      Output("local-dimension-max-index", "data")],
#     [Input("add-dimension", "n_clicks")],
#     [State("dimension-tabs", "children"),
#      State("local-dimension-max-index", "data")],
# )
# def add_dimension_tab(n, children, max_index):
#     if max_index == 1:
#         raise PreventUpdate

#     if max_index is None:
#         max_index = 0

#     if n:
#         children.append(make_dimension(max_index + 1))
#         return [children, max_index + 1]

#     return [children, max_index]
