# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import callback_context as ctx
from dash import dcc

from app.custom_widgets import container
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group
from app.sims.utils import update_processor_ui

__author__ = "Deepansh Srivastava"
__email__ = "srivastava.89@osu.edu"


def ui(index, data=None, n_dim=1, n_dv=1, **kwargs):
    def function_type(index):
        type_label = dbc.InputGroupText("Type")
        val = "Exponential" if data is None else data["type"]
        type_select = dbc.Select(
            options=[
                {"label": "Gaussian", "value": "Gaussian"},
                {"label": "Lorentzian", "value": "Exponential"},
            ],
            value=val,
            id={"function": "apodization", "args": "type", "index": index},
        )
        return dbc.InputGroup([type_label, type_select], className="input-form")

    def arguments(index):
        return custom_input_group(
            prepend_label="FWHM",
            append_label="Hz",
            value=10 if data is None else data["FWHM"].split(" ")[0],
            min=0,
            id={"function": "apodization", "args": "FWHM", "index": index},
            debounce=True,
            pattern="[0-9]*",
        )

    def dimension_index(index):
        input_ = dbc.InputGroupText("Spectral dimension indexes")

        value = [0]
        if data is not None:
            value = [0] if "dim_index" not in data else data["dim_index"]

        dim_index = dcc.Dropdown(
            options=[{"label": f"{i}", "value": i} for i in range(n_dim)],
            value=value,
            multi=True,
            id={"function": "apodization", "args": "dim_index", "index": index},
        )
        return dbc.InputGroup([input_, dim_index], className="input-form")

    def dependent_variable_index(index):
        input_ = dbc.InputGroupText("Spin System indexes")
        options = [{"label": f"{i}", "value": i} for i in range(n_dv)]
        options += [{"label": "ALL", "value": "None"}]

        value = ["None"]
        if data is not None:
            value = ["None"] if "dv_index" not in data else data["dv_index"]

        dv_index = dcc.Dropdown(
            options=options,
            value=value,
            searchable=True,
            multi=True,
            id={"function": "apodization", "args": "dv_index", "index": index},
        )
        return dbc.InputGroup([input_, dv_index], className="input-form")

    featured = [function_type(index), arguments(index)]
    hidden = [dimension_index(index), dependent_variable_index(index)]
    return container(
        text=[
            "Convolution",
            custom_button(
                icon_classname="fas fa-times",
                id={"type": "remove-post_sim-functions", "index": index},
                className="icon-button",
                module="html",
                tooltip="Remove convolution module.",
            ),
        ],
        featured=[*featured, *hidden],
    )


def refresh():
    """If index is none, add an entry else remove the entry at index"""
    post_sim_obj = ctx.states["post_sim_child.children"]
    existing_data = ctx.states["local-mrsim-data.data"]
    method_index = ctx.inputs["select-method.value"]

    n_dim = len(
        existing_data["simulator"]["methods"][method_index]["spectral_dimensions"]
    )
    n_dv = len(existing_data["simulator"]["spin_systems"])

    index = len(post_sim_obj)
    post_sim_obj.append(ui(index, n_dim=n_dim, n_dv=n_dv))

    return update_processor_ui(post_sim_obj)


page = ui(0)


def get_dict(i):
    states = ctx.states
    keys = ["dim_index", "dv_index", "type", "FWHM"]
    val = [
        states[f'{{"args":"{k}","function":"apodization","index":{i}}}.value']
        for k in keys
    ]

    if val[0] in [["None"], []]:
        val[0] = None
    if val[1] in [["None"], []]:
        val[1] = None

    return {
        "dim_index": val[0],
        "dv_index": val[1],
        "function": "apodization",
        "type": val[2],
        "FWHM": f"{val[3]} Hz",
    }
