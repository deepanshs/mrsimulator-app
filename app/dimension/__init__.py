# -*- coding: utf-8 -*-
import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output

from .toolbar import method_toolbar
from app.app import app
from app.custom_widgets import custom_button
from app.custom_widgets import custom_collapsible
from app.dimension.post_simulation_widgets import gaussian_linebroadening_widget
from app.dimension.simulation_widgets import coordinate_grid
from app.dimension.simulation_widgets import environment

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


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
            # html.Div(["Environment", environment(i)]),
            # create coordinate grid => widgets for
            # 1) number of points,
            # 2) spectral width, and
            # 3) reference offset
            custom_collapsible(
                text="Coordinate grid",
                identity=f"coordinate_grid_id-{i}",
                children=coordinate_grid(i),
            ),
            # create line broadening => widgets for
            # 1) apodization function and
            # 2) apodization factor,
            custom_collapsible(
                text="Line broadening",
                identity=f"post_simulation_id-{i}",
                children=gaussian_linebroadening_widget(i),
            ),
        ],
        id=f"dimension-tab-scroll-{i}",
    )
    dimension_contents = html.Div(children=[row1])
    return dimension_contents


# method-title
method_title = html.Div(
    [
        html.Label(id="method-title"),
        custom_button(text="Submit", id="apply-method-changes", color="primary"),
    ],
    className="isotopomer-title",
)

# method contents
method_contents = html.Div(
    children=[make_dimension(i) for i in range(1)], id="dimension-tabs"
)
# method editor

method_editor = html.Div([method_title, method_contents], id="method-editor-content")

# method read only section
method_read_only = html.Div(id="method-read-only")

# slides
method_slide_1 = html.Div(method_read_only, className="slider1")
method_slide_2 = html.Div(method_editor, className="slider2")
method_slide = html.Div(
    [method_slide_1, method_slide_2], id="met-slide", className="met-slide-offset"
)


# dimension layout
dimension_body = html.Div(
    className="my-card hide-window",
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.I(className="fas fa-cube fa-2x"),
                        html.H4("Methods", className="hide-label-sm pl-3"),
                    ],
                    id="dimension-card-title",
                    className="d-flex justify-items-around align-items-center",
                )
            ],
            className="card-header",
        ),
        # html.Div(className="color-gradient-2"),
        html.Div(method_toolbar),
        method_slide,
    ],
    id="dimension-body",
)

# callback code section =======================================================


# @app.callback(
#     Output("new-method-json", "data"),
#     [
#         Input("apply-method-changes", "n_clicks_timestamp"),
#         Input("add-method-button", "n_clicks_timestamp"),
#         Input("duplicate-method-button", "n_clicks_timestamp"),
#     ],
#     [
#         State("channel", "value"),
#         State("count-0", "value"),
#         State("spectral_width-0", "value"),
#         State("reference_offset-0", "value"),
#         State("magnetic_flux_density-0", "value"),
#         State("rotor_frequency-0", "value"),
#         State("rotor_angle-0", "value"),
#         State("local-isotopomers-data", "data"),
#     ],
# )
# def get_method_dict(*args):
#     if not ctx.triggered:
#         raise PreventUpdate

#     trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     existing_data = ctx.states["local-isotopomers-data.data"]
#     data = (
#         existing_data
#         if existing_data is not None
#         else {"name": "", "description": "", "isotopomers": [], "methods": []}
#     )
#     method_length = len(data["methods"])

#     data = {}
#     if trigger_id == "add-method-button":
#         data["data"] = BlochDecayFT(
#             dimensions=[{"count": 2048, "spectral_width": 25000}], channel="1H"
#         ).dict()
#         data["data"]["channel"] = data["data"]["channel"]["symbol"]
#         data["operation"] = "add"
#         data["index"] = method_length + 1

#     if trigger_id == "apply-method-changes":
#         states = ctx.states

#         count = states["count-0.value"]
#         spectral_width = states["spectral_width-0.value"]
#         reference_offset = states["reference_offset-0.value"]
#         magnetic_flux_density = states["magnetic_flux_density-0.value"]
#         rotor_frequency = states["rotor_frequency-0.value"]
#         rotor_angle = states["rotor_angle-0.value"]
#         channel = states["channel.value"]

#         data["data"] = BlochDecayFT(
#             dimensions=[
#                 {
#                     "count": count,
#                     "spectral_width": spectral_width * 1e3,
#                     "reference_offset": reference_offset * 1e3,
#                 }
#             ],
#             channel=channel,
#             magnetic_flux_density=magnetic_flux_density,
#             rotor_frequency=rotor_frequency * 1e3,
#             rotor_angle=rotor_angle * np.pi / 180,
#         ).dict()
#         data["data"]["channel"] = data["data"]["channel"]["symbol"]
#         data["operation"] = "modify"
#         data["index"] = method_length
#     return data


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="create_method_json"),
    Output("new-method-json", "data"),
    [
        Input("apply-method-changes", "n_clicks_timestamp"),
        Input("add-method-button", "n_clicks_timestamp"),
        Input("duplicate-method-button", "n_clicks_timestamp"),
        Input("trash-method-button", "n_clicks_timestamp"),
    ],
)
