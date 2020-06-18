# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from .custom_widgets import custom_switch


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# Scale amplitude ------------------------------------------------------------------- #
scale_amplitude_button = custom_switch(
    # text="Normalize",
    icon_classname="fas fa-arrows-alt-v",
    id="normalize_amp",
    # size="sm",
    tooltip="Scale maximum amplitude to one.",
    outline=True,
    color="dark",
    style={"zIndex": 0},
)


# Show spectrum from individual spin systems ----------------------------------------- #
decompose_button = custom_switch(
    # text="Decompose",
    icon_classname="fac fa-decompose",
    id="decompose",
    # size="sm",
    tooltip="Show simulation from individual spin systems.",
    outline=True,
    color="dark",
    style={"zIndex": 0},
)

# # Show sum of spectrum from individual spin-systems -------------------------------- #
# compose_button = custom_switch(
#     # text="Decompose",
#     icon_classname="fac fa-compose",
#     id="compose",
#     # size="sm",
#     # tooltip="Show simulation from individual spin-systems.",
#     outline=True,
#     color="dark",
#     style={"zIndex": 0},
# )
# select method  -------------------------------------------------------------------- #
select_method = dcc.Dropdown(
    id="select-method",
    value=0,
    searchable=False,
    clearable=False,
    placeholder="View simulation from method ...",
)

# Button group ---------------------------------------------------------------------- #
toolbar = dbc.ButtonGroup([scale_amplitude_button, decompose_button])


# toolbar icons --------------------------------------------------------------------- #
toolbar_select_method = html.Div(
    [html.Label("Select simulation"), select_method],
    className="d-flex align-items-center justify-items-between toolbar",
)


# # add callback for toggling the collapse on small screens
# @app.callback(
#     Output("toolbar-collapse", "is_open"),
#     [Input("toolbar-toggler", "n_clicks")],
#     [State("toolbar-collapse", "is_open")],
# )
# def toggle_toolbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
