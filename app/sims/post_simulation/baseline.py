# -*- coding: utf-8 -*-
from dash import callback_context as ctx

from app.custom_widgets import container
from app.custom_widgets import custom_button
from app.custom_widgets import custom_input_group
from app.sims.utils import update_processor_ui

__author__ = "Deepansh Srivastava"
__email__ = "srivastava.89@osu.edu"


def ui(index, data=None, **kwargs):
    offset = custom_input_group(
        prepend_label="Offset",
        value=0 if data is None else data["offset"],
        id={"function": "baseline", "args": "offset", "index": index},
        debounce=True,
    )

    return container(
        text=[
            "Constant Baseline Offset",
            custom_button(
                icon_classname="fas fa-times",
                id={"type": "remove-post_sim-functions", "index": index},
                className="icon-button",
                module="html",
                tooltip="Remove baseline offset module.",
            ),
        ],
        featured=offset,
    )


def refresh():
    post_sim_obj = ctx.states["post_sim_child.children"]
    index = len(post_sim_obj)
    post_sim_obj.append(ui(index))

    return update_processor_ui(post_sim_obj)


page = ui(0)


def get_dict(i):
    states = ctx.states
    val = states[f'{{"args":"offset","function":"baseline","index":{i}}}.value']

    return {"offset": val, "function": "baseline", "type": "ConstantOffset"}
