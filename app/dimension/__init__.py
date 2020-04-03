# -*- coding: utf-8 -*-
import dash_html_components as html

from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.dimension.post_simulation_widgets import gaussian_linebroadening_widget
from app.dimension.simulation_widgets import coordinate_grid
from app.dimension.simulation_widgets import environment
from app.modal.advance_settings import advance_settings

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# Advanced settings ----------------------------------------------------------------- #
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
    """Create a spectral dimension interface."""
    row1 = html.Div(
        [
            # create environment => widgets for
            # 1) isotope,
            # 2) magnetic flux density,
            # 3) rotor frequency, and
            # 4) rotor angle
            custom_collapsible(
                text="Environment",
                identity=f"environment_id-{i}",
                children=environment(i),
            ),
            # create line broadening => widgets for
            # 1) apodization function and
            # 2) apodization factor,
            custom_collapsible(
                text="Line broadening",
                identity=f"post_simulation_id-{i}",
                children=gaussian_linebroadening_widget(i),
            ),
            # create coordinate grid => widgets for
            # 1) number of points,
            # 2) spectral width, and
            # 3) reference offset
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
                dimension_toolbar,
            ],
            className="card-header",
        ),
        html.Div(className="color-gradient-2"),
        html.Div(children=[make_dimension(i) for i in range(1)], id="dimension-tabs"),
    ],
    id="dimension-body",
)

dimension_body_card = html.Div(dimension_body, id="dimension-card-body")
