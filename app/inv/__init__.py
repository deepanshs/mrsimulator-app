# -*- coding: utf-8 -*-
import base64
import json
from urllib.request import urlopen

import csdmpy as cp
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from celery.result import AsyncResult
from dash import callback_context as ctx
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from mrinversion.kernel.nmr import ShieldingPALineshape
from mrinversion.linear_model import TSVDCompression

from .layout import page
from .tasks import query
from app import app
from app.sims.importer import load_csdm
from app.utils import slogger

# from mrinversion.linear_model import SmoothLassoLS

# from mrinversion.linear_model import SmoothLasso

SmoothLassoLS = None


# class Worker:
#     def __init__(self, filename='semaphore.txt'):
#         self.filename = filename
#         with open(self.filename, 'w') as f:
#             f.write('done')

#     def lock(self):
#         with open(self.filename, 'w') as f:
#             f.write('working')

#     def unlock(self):
#         with open(self.filename, 'w') as f:
#             f.write('done')

#     def is_locked(self):
#         return open(self.filename, 'r').read() == 'working'

mrinv = html.Div(
    [
        dbc.Navbar(
            html.Div(
                dcc.Link(
                    dbc.NavbarBrand("MRInversion", style={"color": "#d6d6d6"}), href="/"
                ),
                className="nav-burger",
            ),
            color=None,
            dark=None,
            expand="md",
        ),
        page,
        html.Div(id="task-id", children="none"),
        html.Div(id="task-status", children="task-status"),
        # This is an Interval div and determines the initial app refresh rate.
        # The current settings should be ok for all applications.
        # Don't put it below a Data Table:
        dcc.Interval(
            id="task-interval", interval=250, n_intervals=0  # in milliseconds
        ),
    ],
    className="inv-page",
    # **{"data-app-link": ""},
)


@app.callback(
    [Output("INV-spectrum", "figure"), Output("INV-input-data", "data")],
    [
        Input("INV-upload-from-graph", "contents"),
        Input("INV-transpose", "n_clicks"),
        Input("url-search", "href"),
    ],
    [State("INV-spectrum", "figure"), State("INV-input-data", "data")],
    prevent_initial_call=True,
)
def update_input_graph(contents, tr_val, url, figure, data):
    # if contents is None:
    #     raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "url-search":
        slogger("url", url)
        if url in [None, ""]:
            raise PreventUpdate

        response = urlopen(url[3:])
        content = json.loads(response.read())
        exp_data = cp.parse_dict(content)
        pre_figure(exp_data, figure)
        return [figure, exp_data.real.dict()]

    if trigger_id == "INV-upload-from-graph":
        content = contents.split(",")[1]

        decoded = base64.b64decode(content)
        success, exp_data, _ = load_csdm(decoded)

        if not success:
            raise PreventUpdate

        pre_figure(exp_data, figure)
        return [figure, exp_data.real.dict()]

    if trigger_id == "INV-transpose":
        if data is None:
            raise PreventUpdate
        data = cp.parse_dict(data).T

        figure["data"][0]["x"] = data.x[0].coordinates.value
        figure["data"][0]["y"] = data.x[1].coordinates.value
        figure["data"][0]["z"] = data.y[0].components[0]
        return [figure, data.dict()]


def pre_figure(exp_data, figure):
    [item.to("ppm", "nmr_frequency_ratio") for item in exp_data.x]
    x, y = [item.coordinates.value for item in exp_data.x]
    z = exp_data.y[0].components[0].real
    trace = go.Heatmap(x=x, y=y, z=z, colorscale="jet")
    figure["data"][0] = trace

    layout = figure["layout"]
    layout["xaxis"]["autorange"] = "reversed"
    layout["yaxis"]["autorange"] = "reversed"

    label = exp_data.x[0].label
    label = label if label not in [None, ""] else "frequency"
    layout["xaxis"]["title"] = f"{label} / ppm"

    label = exp_data.x[1].label
    label = label if label not in [None, ""] else "frequency"
    layout["yaxis"]["title"] = f"{label} / ppm"


@app.callback(
    Output("INV-data-range", "data"),
    [Input("INV-spectrum", "relayoutData")],
    [State("INV-spectrum", "figure")],
    prevent_initial_call=True,
)
def display_relayout_data(relayoutData, fig):
    if relayoutData is None:
        raise PreventUpdate

    keys = relayoutData.keys()

    if "yaxis.range[0]" in keys:
        y = np.asarray(fig["data"][0]["y"])
        index_min = np.where(y > relayoutData["yaxis.range[0]"])[0][0]
        index_max = np.where(y < relayoutData["yaxis.range[1]"])[0][-1]
        range_zoom_y = np.sort([index_min, index_max])

    if "xaxis.range[0]" in keys:
        x = np.asarray(fig["data"][0]["x"])
        index_min = np.where(x > relayoutData["xaxis.range[0]"])[0][0]
        index_max = np.where(x < relayoutData["xaxis.range[1]"])[0][-1]
        range_zoom_x = np.sort([index_min, index_max])

    if "yaxis.range[0]" in keys and "xaxis.range[0]" in keys:
        print(range_zoom_x, range_zoom_y)
        return [range_zoom_x, range_zoom_y]

    if "yaxis.range[0]" in keys and "xaxis.range[0]" not in keys:
        print([0, -1], range_zoom_y)
        return [[0, -1], range_zoom_y]

    if "yaxis.range[0]" not in keys and "xaxis.range[0]" in keys:
        print(range_zoom_x, [0, -1])
        return [range_zoom_x, [0, -1]]

    if "xaxis.autorange" in keys:
        return [0, -1]

    raise PreventUpdate


@app.callback(
    Output("INV-kernel-rotor_angle", "value"),
    [Input("INV-kernel-type", "value")],
    prevent_initial_call=True,
)
def update_number_of_sidebands(k_typ):
    if k_typ == "sideband-correlation":
        return 54.735
    if k_typ == "MAF":
        return 90


@app.callback(
    Output("INV-kernel", "data"),
    [Input("INV-generate-kernel", "n_clicks")],
    [
        State("INV-input-data", "data"),
        State("INV-dimension-0-count", "value"),
        State("INV-dimension-0-increment", "value"),
        State("INV-dimension-1-count", "value"),
        State("INV-dimension-1-increment", "value"),
        State("INV-kernel-channel", "value"),
        State("INV-kernel-flux", "value"),
        State("INV-kernel-rotor_angle", "value"),
        State("INV-supersampling", "value"),
        State("INV-data-range", "data"),
        State("INV-kernel-type", "value"),
    ],
    prevent_initial_call=True,
)
def generate_kernel(
    n, data, count0, inc0, count1, inc1, channel, B0, theta, n_su, d_range, k_typ
):
    if data is None:
        raise PreventUpdate

    if d_range is None:
        d_range = [[0, -1], [0, -1]]

    data = cp.parse_dict(data)

    anisotropic_dimension = data.dimensions[0]
    inverse_dimensions = [
        cp.LinearDimension(count=count0, increment=f"{inc0} Hz", label="x"),
        cp.LinearDimension(count=count1, increment=f"{inc1} Hz", label="y"),
    ]

    vr = 0
    ns = 1

    if k_typ == "sideband-correlation":
        vr = anisotropic_dimension.increment.to("Hz")
        ns = anisotropic_dimension.count

    if k_typ == "MAF":
        vr = "1 GHz"
        ns = 1

    K = ShieldingPALineshape(
        anisotropic_dimension=anisotropic_dimension,
        inverse_dimension=inverse_dimensions,
        channel=channel,
        magnetic_flux_density=f"{B0} T",
        rotor_angle=f"{theta} °",
        rotor_frequency=f"{vr}",
        number_of_sidebands=ns,
    ).kernel(supersampling=int(n_su))

    ranges = slice(d_range[1][0], d_range[1][1], None)
    data_truncated = data[:, ranges]

    new_system = TSVDCompression(K, data_truncated)
    compressed_K = new_system.compressed_K
    compressed_s = new_system.compressed_s

    return {
        "kernel": compressed_K,
        "signal": compressed_s.dict(),
        "inverse_dimensions": [item.dict() for item in inverse_dimensions],
    }


@app.callback(
    Output("task-id", "children"),
    [Input("INV-solve", "n_clicks")],
    [
        State("task-id", "children"),  # <--- task-id must always be first
        # State("year_menu", "value"),
        State("INV-l1", "value"),
        State("INV-l2", "value"),
        State("INV-kernel", "data"),
        # State("INV-output", "figure"),
    ],
    prevent_initial_call=True,
)
def start_task_callback(n_clicks, task_id, l1, l2, data):
    """This callback is triggered by  clicking the submit button click event.  If the
    button was really pressed (as opposed to being self-triggered when the app is
    launch) it checks if the user input is valid then puts the query on the Celery
    queue.  Finally it returns the celery task ID to the invisible div called 'task-id'.
    """
    print("inside", n_clicks)
    # Don't touch this:
    slogger(
        "start_task_callback",
        f"n_clicks={n_clicks}, task_id={task_id}, l1={l1}, l2={l2}",
    )
    if n_clicks is None or n_clicks == 0:
        return "none"

    # Validate the user input.  If invalid return 'none' to task-id and don't queue
    # anything.
    if l1 is None:
        # invalid input
        slogger("start_task_callback", "user has not selected any year")
        return "none"
    else:
        # valid, so proceed
        slogger("start_task_callback", f"l1={l1} l2={l2}")

    # Put search function in the queue and return task id
    # (arguments must always be passed as a list)
    slogger("start_task_callback", "query accepted and applying to Celery")
    task = query.apply_async([l1, l2, data])
    # don't touch this:
    slogger("start_Task_callback", f"query is on Celery, task-id={task.id}")
    return str(task.id)


# Don't touch this:
@app.callback(
    Output("task-interval", "interval"),
    [Input("task-id", "children"), Input("task-status", "children")],
)
def toggle_interval_speed(task_id, task_status):
    """This callback is triggered by changes in task-id and task-status divs. It
    switches the page refresh interval to fast (1 sec) if a task is running, or slow
    (24 hours) if a task is pending or complete."""
    if task_id == "none":
        slogger("toggle_interval_speed", "no task-id --> slow refresh")
        return 24 * 60 * 60 * 1000
    if task_id != "none" and (task_status in ["SUCCESS", "FAILURE"]):
        slogger(
            "toggle_interval_speed",
            "task-id is {} and status is {} --> slow refresh".format(
                task_id, task_status
            ),
        )
        return 24 * 60 * 60 * 1000
    else:
        slogger(
            "toggle_interval_speed",
            "task-id is {} and status is {} --> fast refresh".format(
                task_id, task_status
            ),
        )
        return 5000


# Don't touch this:
@app.callback(
    Output("spinner", "style"),
    [Input("task-interval", "n_intervals"), Input("task-status", "children")],
)
def show_hide_spinner(n_intervals, task_status):
    """This callback is triggered by then Interval clock and checks the task progress
    via the invisible div 'task-status'.  If a task is running it will show the spinner,
    otherwise it will be hidden."""
    if task_status == "PROGRESS":
        slogger("show_hide_spinner", "show spinner")
        return None
    else:
        slogger(
            "show_hide_spinner",
            "hide spinner because task_status={}".format(task_status),
        )
        return {"display": "none"}


# Don't touch this:
@app.callback(
    Output("task-status", "children"),
    [Input("task-interval", "n_intervals"), Input("task-id", "children")],
    update_initial_call=False,
)
def update_task_status(n_intervals, task_id):
    """This callback is triggered by the Interval clock and task-id. It checks the task
    status in Celery and returns the status to an invisible div"""
    return str(AsyncResult(task_id).state)


@app.callback(
    [
        Output("INV-output", "figure"),
        Output("INV-l1", "value"),
        Output("INV-l2", "value"),
    ],
    [Input("task-status", "children")],
    [State("task-id", "children")],
)
def get_results(task_status, task_id):
    """This callback is triggered by task-status. It checks the task status, and if the
    status is 'SUCCESS' it retrieves results, defines the results form and returns it,
    otherwise it returns [] so that nothing is displayed"""
    if task_status == "SUCCESS":
        # Fetch results from Celery and forget the task
        slogger(
            "get_results", "retrieve results for task-id {} from Celery".format(task_id)
        )
        result = AsyncResult(task_id).result  # fetch results
        AsyncResult(task_id).forget()  # delete from Celery
        # Display a message if their were no hits
        if result == [{}]:
            return ["We couldn't find any results.  Try broadening your search."]
        # Otherwise return the populated DataTable
        return result
    else:
        # don't display any results
        raise PreventUpdate
