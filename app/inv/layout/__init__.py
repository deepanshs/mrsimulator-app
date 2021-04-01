# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from .input import input_layer

storage_div = html.Div(
    [
        dcc.Store(id="INV-input-data", storage_type="memory"),
        dcc.Store(id="INV-kernel", storage_type="memory"),
        dcc.Store(id="INV-data-range", storage_type="memory"),
        # dcc.Store(id="INV-output-residue", storage_type="memory"),
    ]
)

page = html.Div([input_layer, storage_div])
