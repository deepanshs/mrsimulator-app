# -*- coding: utf-8 -*-
# import dash_bootstrap_components as dbc
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
dimension_toolbar = html.Div([advance_setting_button, advance_settings])


# dimension parameters
def make_dimension(i):
    row1 = html.Div(
        [
            custom_collapsible(
                text="Environment",
                identity=f"environment_id-{i}",
                children=environment(i),
            ),
            custom_collapsible(
                text="Line broadening",
                identity=f"post_simulation_id-{i}",
                children=gaussian_linebroadening_widget(i),
            ),
            custom_collapsible(
                text="Coordinate grid",
                identity=f"coordinate_grid_id-{i}",
                children=coordinate_grid(i),
            ),
        ],
        id=f"dimension-tab-scroll-{i}",
    )
    dimension_contents = html.Div(children=[row1])

    return dimension_contents


# dimension layout
dimension_body = html.Div(
    className="my-card",
    children=[
        html.Div(
            [
                html.H4("Spectral Dimension", id="dimension-card-title"),
                # dbc.Button("+", id="add-dimension"),
                dimension_toolbar,
            ],
            className="card-header",
        ),
        html.Div(className="color-gradient-2"),
        html.Div(children=[make_dimension(i) for i in range(1)], id="dimension-tabs"),
    ],
    id="dimension-body",
)

dimension_body_card = html.Div(
    dimension_body, id="dimension-card-body", className="h-100"
)


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
