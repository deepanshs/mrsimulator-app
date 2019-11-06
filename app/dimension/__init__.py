# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.dimension.post_simulation_widgets import gaussian_linebroadening_widget
from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.dimension.simulation_widgets import coordinate_grid
from app.dimension.simulation_widgets import environment
from app.modal.advance_settings import advance_settings

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# Advance settings ------------------------------------------------------------------ #
advance_setting_button = custom_button(
    icon="fas fa-cog",
    id="advance_setting",
    tooltip="Advance setting",
    outline=True,
    color="dark",
)
dimension_toolbar = dbc.Row([dbc.Col([advance_setting_button, advance_settings])])


# dimension parameters
def make_dimension(i):
    # dimension parameters
    dimension_contents = dbc.Tab(
        label=f"Index-{i}",
        children=[dbc.Row(
            [
                dbc.Col(
                    custom_collapsible(
                        text="Environment",
                        identity=f"environment_id-{i}",
                        children=environment(i),
                    ),
                    xs=12,
                    sm=12,
                    md=6,
                    lg=12,
                    xl=12,
                ),
                dbc.Col(
                    custom_collapsible(
                        text="Coordinate grid",
                        identity=f"coordinate_grid_id-{i}",
                        children=coordinate_grid(i),
                    )
                ),
                # sub_group(
                #     "Post simulation", f"post_simulation_id-{i}",
                #      post_simulation_widgets(i)
                # ),
            ],),
            dbc.Row([dbc.Col(
                    custom_collapsible(
                        text="Line broadening",
                        identity=f"post_simulation_id-{i}",
                        children=gaussian_linebroadening_widget(i),
                        hide=False,
                    ),
                    xs=12,
                    sm=12,
                    md=6,
                    lg=12,
                    xl=12,
                ),])]
            # style={
            #     "min-height": "65vh",
            #     "max-height": "65vh",
            #     "overflow-y": "scroll",
            #     "overflow-x": "hidden",
            # },
    )
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
        dbc.Tabs([make_dimension(i) for i in range(1)]),
    ],
    id="dimension-body",
)
