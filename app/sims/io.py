# -*- coding: utf-8 -*-
import base64
import json
import os
from urllib.request import urlopen

import mrsimulator as mrsim
from csdmpy.dependent_variable.download import get_absolute_url_path
from dash import callback_context as ctx
from dash.exceptions import PreventUpdate

from .utils import assemble_data
from .utils import on_fail_message

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
PATH = os.path.split(__file__)[0]


def load_file_from_url(url):
    """Load the data from url."""
    url_path = get_absolute_url_path(url, PATH)
    response = urlopen(url_path)
    contents = json.loads(response.read())
    return parse_file_contents(contents, url_path.endswith(".mrsys"))


def load_local_file(contents):
    """Parse contents from the spin-systems file."""
    content_string = contents.split(",")[1]
    decoded = base64.b64decode(content_string)
    contents = json.loads(str(decoded, encoding="UTF-8"))
    return parse_file_contents(contents, isinstance(contents, list))


def import_file_from_url():
    """Import .mrsim file from url."""
    url_search = ctx.inputs["url-search.href"]
    print("url_search", url_search)
    if url_search in [None, ""]:
        raise PreventUpdate
    return load_file_from_url(url_search[3:])


def import_mrsim_file():
    """Import .mrsim file from local file system."""
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    contents = ctx.inputs[f"{trigger_id}.contents"]
    if contents is None:
        raise PreventUpdate
    return load_local_file(contents)


def parse_file_contents(content, spin_sys=False):
    content = {"spin_systems": content} if spin_sys else content

    try:
        data = fix_missing_keys(content)
        return assemble_data(parse_data(data))
    except Exception as e:
        message = f"FileReadError: {e}"
        return on_fail_message(message)


def fix_missing_keys(json_data):
    """Fill in missing data fields with default values."""
    default_data = {
        "name": "Sample",
        "description": "Add a description ...",
        "spin_systems": [],
        "methods": [],
        "config": {
            "integration_density": 70,
            "integration_volume": "octant",
            "number_of_sidebands": 64,
            "decompose_spectrum": "none",
        },
    }
    default_data.update(json_data)
    return default_data


def parse_data(data):
    """Parse units from the data and return a Simulator dict."""
    sim, signal_processors, params = mrsim.parse(data, parse_units=True)
    for item in sim.methods:
        item.simulation = None

    sim = sim.json(units=True)

    sim["signal_processors"] = [{"operations": []} for _ in sim["methods"]]
    if signal_processors is not None:
        _ = [
            item.update(obj.json())
            for item, obj in zip(sim["signal_processors"], signal_processors)
        ]

    sim["params"] = params.dumps() if params is not None else None

    return sim
