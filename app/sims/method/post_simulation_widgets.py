# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context as ctx
from dash import no_update
from dash.dependencies import ALL
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app
from app.custom_widgets import collapsable_card
from app.custom_widgets import custom_input_group

__author__ = ["Maxwell C. Venetos", "Deepansh Srivastava"]
__email__ = ["venetos.5@buckeyemail.osu.edu", "srivastava.89@osu.edu"]


def appodization_ui(index, data=None):
    def function_type(index):
        type_label = dbc.InputGroupAddon("Type", addon_type="prepend")
        val = "Exponential" if data is None else data["type"]
        type_select = dbc.Select(
            options=[
                {"label": "Gaussian", "value": "apodization-Gaussian"},
                {"label": "Lorentzian", "value": "apodization-Exponential"},
            ],
            value=f"apodization-{val}",
            id={"type": "function", "name": "apodization", "index": index},
        )
        return dbc.InputGroup([type_label, type_select], className="input-form")

    def arguments(index):
        return custom_input_group(
            prepend_label="FWHM",
            append_label="Hz",
            value=10 if data is None else data["FWHM"],
            min=0,
            id={"type": "arg", "name": "apodization", "index": index},
            debounce=True,
            pattern="[0-9]*",
        )

    def dimension_index(index):
        input_ = dbc.InputGroupAddon("Spectral dimension", addon_type="prepend")
        dim_index = dbc.Select(
            options=[{"label": f"{i}", "value": i} for i in range(1)],
            value=0 if data is None else data["dim_index"][0],
            id={"type": "dim_index", "name": "apodization", "index": index},
        )
        return dbc.InputGroup([input_, dim_index], className="input-form")

    def dependent_variable_index(index):
        input_ = dbc.InputGroupAddon("Spin System", addon_type="prepend")
        options = [{"label": f"{i}", "value": i} for i in range(10)]
        options += [{"label": "ALL", "value": "None"}]
        dv_index = dcc.Dropdown(
            options=options,
            value=["None"] if data is None else data["dv_index"],
            searchable=True,
            multi=True,
            id={"type": "dv_index", "name": "apodization", "index": index},
        )
        return dbc.InputGroup([input_, dv_index], className="input-form")

    featured = [function_type(index), arguments(index)]
    hidden = [dimension_index(index), dependent_variable_index(index)]
    # return html.Div([*featured, *hidden])
    return collapsable_card(
        text="Apodization",
        id_=f"apodization-post-sim-{index}",
        featured=featured,
        hidden=hidden,
        message="Show/Hide",
    )


def tools():
    """Add, duplcicate, or remove methods"""
    new = html.Button("add", id="add-post_sim-button")
    duplicate = html.Button("duplicate", id="duplicate-post_sim-button")
    remove = html.Button("remove", id="remove-post_sim-button")

    return html.Div(children=[new, duplicate, remove])


def get_apodization_dict(fn, arg, dim_index, dv_index):
    print(dv_index)

    if dv_index in [["None"], []]:
        dv_index = None
    fn_name, fn_type = fn.split("-")
    return {
        "dim_index": [dim_index],
        "dv_index": dv_index,
        "function": fn_name,
        "type": fn_type,
        "FWHM": f"{arg} Hz",
    }


def refresh(py_dict):
    obj = []
    print("py_dict", py_dict)
    for i, item in enumerate(py_dict["operations"]):
        if item["function"] == "apodization":
            obj.append(appodization_ui(i, item))
    return obj


@app.callback(
    [
        Output("signal-processor-data-temp", "data"),
        Output("post_sim_child", "children"),
    ],
    [
        Input("signal-processor-button", "n_clicks"),
        Input("add-post_sim-button", "n_clicks"),
        Input("select-method", "value"),
        Input("signal-processor-data", "data"),
    ],
    [
        State({"type": "function", "name": "apodization", "index": ALL}, "value"),
        State({"type": "arg", "name": "apodization", "index": ALL}, "value"),
        State({"type": "dim_index", "name": "apodization", "index": ALL}, "value"),
        State({"type": "dv_index", "name": "apodization", "index": ALL}, "value"),
        State("signal-processor-data", "data"),
        State("post_sim_child", "children"),
        State("select-method", "options"),
        State("signal-processor-data-temp", "data"),
    ],
    prevent_initial_call=True,
)
def setup_processor(
    n1,
    n2,
    method_index,
    process_data,
    ap1,
    ap2,
    ap3,
    ap4,
    data,
    post_sim_obj,
    method_options,
    existing_process_data,
):
    # print(ap1)
    # print(ap2)
    # print(ap3)
    # print(ctx.states)

    # method_index = str(method_index)
    # data = [] if data is None else data
    # print("data", data)

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if existing_process_data is None:
        existing_process_data = [{"operations": []} for _ in method_options]

    if len(existing_process_data) < len(method_options):
        n = len(method_options) - len(existing_process_data)
        existing_process_data += [{"operations": []} for _ in range(n)]

    if trigger_id == "signal-processor-data":
        local_data = ctx.states["signal-processor-data.data"]
        return [no_update, refresh(local_data[method_index])]

    if trigger_id == "signal-processor-button":

        # for fn, arg, dim in zip(s1, s2, s3):
        #     {'dim_index': dim, 'function': fn, }
        operations = [{"dim_index": [0], "function": "IFFT"}]
        operations += [
            get_apodization_dict(fn, arg, dim, dv)
            for fn, arg, dim, dv in zip(ap1, ap2, ap3, ap4)
        ]
        operations += [{"dim_index": [0], "function": "FFT"}]
        print(operations)
        processor = {"operations": operations}

        # if len(data) <= method_index:
        #     n = method_index - len(data) + 1
        #     data += [{"operations": []} for _ in range(n)]

        existing_process_data[method_index] = processor
        # print()
        print(existing_process_data)
        return [existing_process_data, no_update]

    # if method_index not in data:
    #     data[method_index] = {"operations": []}
    if trigger_id == "select-method":
        # if len(data) <= method_index:
        #     n = method_index - len(data) + 1
        #     data += [{"operations": []} for _ in range(n)]
        return [no_update, refresh(existing_process_data[method_index])]

    if trigger_id == "add-post_sim-button":
        index = len(post_sim_obj)
        print("index", index)
        post_sim_obj.append(appodization_ui(index))
        return [no_update, post_sim_obj]


def gaussian_linebroadening_widget(i):

    broadeningFunction = dcc.RadioItems(
        options=[
            {"label": "Lorentzian", "value": 0},
            {"label": "Gaussian", "value": 1},
        ],
        value=0,  # "Lorentz",
        labelStyle={"display": "inline-block", "width": "50%"},
        id=f"Apodizing_function-{i}",
    )

    # broaden_range = {
    #     0: "0 Hz",
    #     200: "200 Hz",
    #     400: "400 Hz",
    #     600: "600 Hz",
    #     800: "800 Hz",
    #     1000: "1 kHz",
    # }
    # line_broadening = custom_slider(
    #     label="Line Broadening",
    #     return_function=lambda x: f"\u03BB = {x/1000} kHz"
    #     if x > 1000
    #     else f"\u03BB = {x} Hz",
    #     min=0,
    #     max=1000,
    #     step=25,
    #     value=50,
    #     marks=broaden_range,
    #     id=f"broadening_points-{i}",
    # )
    line_broadening = custom_input_group(
        id=f"broadening_points-{i}",
        append_label="Hz",
        prepend_label="Factor",
        value=50,
        debounce=True,
    )

    return html.Div([broadeningFunction, line_broadening], className="container")

    # return [line_broadening]
