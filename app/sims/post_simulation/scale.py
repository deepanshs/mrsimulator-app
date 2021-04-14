# -*- coding: utf-8 -*-
from dash import callback_context as ctx
from dash import no_update

from app.custom_widgets import custom_input_group
from app.sims.utils import expand_output

__author__ = "Deepansh Srivastava"
__email__ = "srivastava.89@osu.edu"

# {"factor": 1, "function": "Scale"}


def ui(index, data=None):
    return custom_input_group(
        prepend_label="Scaling Factor",
        value=1 if data is None else data["factor"],
        min=0,
        id={"function": "scale", "args": "factor", "index": index},
        debounce=True,
        pattern="[0-9]*",
    )


def refresh():
    post_sim_obj = ctx.states["post_sim_child.children"]
    index = len(post_sim_obj)
    print("index", index)
    post_sim_obj.append(ui(index))

    out = {
        "alert": ["", False],
        "mrsim": [no_update, no_update],
        "children": [no_update] * 3,
        "mrsim_config": [no_update] * 4,
        "processor": [post_sim_obj],
    }

    return expand_output(out)


page = ui(0)


def get_scale_dict(i):
    states = ctx.states
    val = states[f'{{"args":"factor","function":"scale","index":{i}}}.value']

    return {"factor": val, "function": "Scale"}
