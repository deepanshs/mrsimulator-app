# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from . import importer
from . import navbar
from .graph import spectrum_body
from .info import sample_info
from .menubar import file_menu
from .modal.advance_settings import advance_settings
from .nmr_method import dimension_body
from .nmr_method.toolbar import method_edit_tools
from .spin_system import spin_system_body
from .spin_system.toolbar import spin_system_edit_tools

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# storage data
storage_div = html.Div(
    [
        # memory for holding the spin systems data
        dcc.Store(id="local-mrsim-data", storage_type="session"),
        dcc.Store(id="local-simulator-data", storage_type="memory"),
        # memory for holding the exp data
        dcc.Store(id="local-exp-external-data", storage_type="memory"),
        # memory for holding the computationally expensive computed data.
        dcc.Store(id="local-computed-data", storage_type="memory"),
        # memory for holding the computed + processed data. Processing over the
        # computed data is less computationally expensive.
        dcc.Store(id="local-processed-data", storage_type="memory"),
        # memory for holding the nmr_method data
        dcc.Store(id="local-method-data", storage_type="memory"),
        # a mapping of spin system index to local spin-system index
        dcc.Store(id="local-spin-system-index-map", storage_type="memory"),
        # dcc.Store(id="local-nmr_method-max-index", storage_type="memory"),
        dcc.Store(id="new-spin-system", storage_type="memory"),
        dcc.Store(id="new-method", storage_type="memory"),
        # store a bool indicating if the data is from an external file
        dcc.Store(id="config", storage_type="memory"),
        # method-template data
        dcc.Store(id="method-from-template", storage_type="memory"),
        dcc.Store(id="user-config", storage_type="local"),
    ]
)

nav_group = html.Div(
    [
        navbar.navbar_group,
        html.Div(
            [importer.spin_system_import_layout, importer.spectrum_import_layout],
            id="drawers-import",
        ),
        dbc.Alert(
            id="alert-message-simulation",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
        dbc.Alert(
            id="alert-message-import",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
        dbc.Alert(
            id="alert-message-spectrum",
            color="danger",
            dismissable=True,
            fade=True,
            is_open=False,
        ),
    ]
)

tips = ["Home", "Spin Systems", "Methods", "Settings"]
targets = ["view-info", "view-spin-systems", "view-methods", "advance_setting"]
tooltips = html.Div(
    [
        dbc.Tooltip(tip, target=target, placement="right")
        for tip, target in zip(tips, targets)
    ]
)

view_tools1 = html.Ul(
    [
        html.Div(html.Ul(file_menu, className="menu"), className="master-toolbar"),
        html.Br(),
        html.Li(
            html.Span(html.I(className="fas fa-home fa-lg")),
            id="view-info",
            className="active",
            **{"data-tab-target": "info-body"}
        ),
        html.Li(
            html.Span(html.I(className="fac fa-spin-systems fa-lg")),
            id="view-spin-systems",
            **{"data-tab-target": "spin-system-body"}
        ),
        html.Li(
            html.Span(html.I(className="fas fa-cube fa-lg")),
            id="view-methods",
            **{"data-tab-target": "method-body"}
        ),
        tooltips,
    ],
    className="sidebar",
)
view_tools2 = html.Ul(
    [
        html.Li(html.Span(html.I(className="fas fa-cog fa-lg")), id="advance_setting"),
        advance_settings,
    ],
    className="sidebar button",
)

view_tools = html.Div([view_tools1, view_tools2], className="view-tools")

sidebar = html.Div(
    [view_tools, method_edit_tools, spin_system_edit_tools],
    className="sidebar-master",
)

app_1 = html.Div(
    [
        html.Div(id="temp1"),
        html.Div(id="temp2"),
        html.Div(id="temp3"),
        html.Div(id="temp4"),
        html.Div(id="temp5"),
        html.Div(id="temp6"),
        # html.Div(
        #     [
        #         html.Li(html.A("In", href="#info-body")),
        #         html.Li(html.A("Is", href="#spin-system-body")),
        #         html.Li(html.A("Me", href="#method-body")),
        #         html.Li(html.A("Sp", href="#spectrum-body")),
        #     ],
        #     className="nav-token",
        # ),
        html.Div(
            [sample_info, spin_system_body, dimension_body, spectrum_body],
            className="mobile-scroll",
        ),
        storage_div,
        navbar.navbar_bottom,
    ],
    className="app-1",
)
