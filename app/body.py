# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from . import navbar
from .graph import spectrum_body
from .home import default_home_page
from .nmr_method import dimension_body
from .spin_system import spin_system_body

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# storage data
storage_div = html.Div(
    [
        # memory for holding the spin systems data.
        dcc.Store(id="local-mrsim-data", storage_type="session"),
        # memort for storing local simulator data.
        dcc.Store(id="local-simulator-data", storage_type="memory"),
        # memory for storing the experimental data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for storing the local computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the nmr_method data
        dcc.Store(id="local-method-data", storage_type="memory"),
        dcc.Store(id="new-spin-system", storage_type="memory"),
        dcc.Store(id="new-method", storage_type="memory"),
        # store a bool indicating if the data is from an external file
        dcc.Store(id="config", storage_type="memory"),
        # method-template data
        dcc.Store(id="add-method-from-template", storage_type="memory"),
        dcc.Store(id="user-config", storage_type="local"),
    ]
)

simulation_alert = dbc.Alert(
    id="alert-message-simulation",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

import_alert = dbc.Alert(
    id="alert-message-import",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

graph_alert = dbc.Alert(
    id="alert-message-spectrum",
    color="danger",
    dismissable=True,
    fade=True,
    is_open=False,
)

nav_group = html.Div([navbar.navbar_top, simulation_alert, import_alert, graph_alert])


app_1 = html.Div(
    [
        html.Div(id="temp1"),
        html.Div(id="temp2"),
        html.Div(id="temp3"),
        html.Div(id="temp4"),
        html.Div(id="temp5"),
        html.Div(id="temp6"),
        html.Div(
            [default_home_page, spin_system_body, dimension_body, spectrum_body],
            className="mobile-scroll",
        ),
        storage_div,
        navbar.navbar_bottom,
    ],
    className="app-1",
)
