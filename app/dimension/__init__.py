# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from .simulation_widgets import coordinate_grid
from .simulation_widgets import environment
from app.custom_widgets import custom_collapsible


__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


# dimension parameters
def make_dimension(i):

    # dimension parameters
    dimension_contents = dbc.Tab(
        label=f"Index-{i}",
        children=dbc.Row(
            [
                dbc.Col(
                    custom_collapsible(
                        "Environment", f"environment_id-{i}", environment(i), hide=False
                    ),
                    xs=12,
                    sm=12,
                    md=6,
                    lg=12,
                    xl=12,
                ),
                dbc.Col(
                    custom_collapsible(
                        "Coordinate grid",
                        f"coordinate_grid_id-{i}",
                        coordinate_grid(i),
                        hide=False,
                    )
                ),
                # sub_group(
                #     "Post simulation", f"post_simulation_id-{i}",
                #      post_simulation_widgets(i)
                # ),
            ],
            # style={
            #     "min-height": "65vh",
            #     "max-height": "65vh",
            #     "overflow-y": "scroll",
            #     "overflow-x": "hidden",
            # },
        ),
    )
    return dimension_contents


# submit_button = dbc.Button(
#     "Submit",
#     id="submit_query",
#     outline=True,
#     color="primary",
#     className="mr-1",
#     size="sm",
# )


# badge = dbc.Badge(
#     " ", pill=True, color="success", className="mr-1", id="indicator_status"
# )


dimension_body = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(dbc.Col(html.H4("Dimensions", className="card-title"))),
                dbc.Tabs([make_dimension(i) for i in range(1)]),
            ],
            className="w-100",
        )
    ],
    className="h-100 my-card",
)
