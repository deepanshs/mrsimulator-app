# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from .app import app
from .custom_widgets import custom_button
from .custom_widgets import custom_switch
from .modal.advance_settings import advance_settings


__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

# Scale amplitude ------------------------------------------------------------------- #
scale_amplitude_button = custom_switch(
    icon="fas fa-arrows-alt-v",
    id="normalize_amp",
    tooltip="Normalize amplitudes to one.",
    outline=True,
    color="dark",
)

# Info ------------------------------------------------------------------------------ #
info_button = custom_button(
    icon="fas fa-info-circle",
    id="indicator_status",
    tooltip="Info",
    outline=True,
    color="dark",
)

# Advance settings ------------------------------------------------------------------ #
setting_button = custom_button(
    icon="fas fa-cog",
    id="advance_setting",
    tooltip="Advance setting",
    outline=True,
    color="dark",
)

# Show spectrum from individual isotopomers ----------------------------------------- #
decompose_button = custom_switch(
    # text="decompose",
    icon="fas fa-chart-area",
    id="decompose",
    tooltip="Show simulation from individual isotopomers.",
    outline=True,
    color="dark",
)


# # decompose button callback method
# @app.callback(
#     Output("decompose", "active"),
#     [Input("decompose", "n_clicks")],
#     [State("decompose", "active")],
# )
# def toggle_decompose_button(n1, status):
#     "Toggle decompose button."
#     if n1 is None:
#         raise PreventUpdate

#     new_status = True
#     if bool(status):
#         new_status = False
#     return new_status


# Button group 0 -------------------------------------------------------------------- #
group_0_buttons = dbc.ButtonGroup(
    [scale_amplitude_button],
    # className="btn-group mr-2",
)

# Button group 1 -------------------------------------------------------------------- #
group_1_buttons = dbc.ButtonGroup(
    [decompose_button, info_button, setting_button, advance_settings],
    # className="btn-group mr-2",
)


# Download dataset ------------------------------------------------------------------ #
dropdown_download_items = [
    dbc.DropdownMenuItem("CSDM", href="", id="download_csdm"),
    dbc.DropdownMenuItem("CSV", id="dropdown-csv-item"),
]

dropdown_downloadables = dbc.DropdownMenu(
    dropdown_download_items,
    # label="Download",
    # className="fas fa-download",
    right=True,
    addon_type="prepend",
    group=True,
    # outline=True,
    color="dark",
)

# # As CSDM
# csdm_button = custom_button(
#     icon="fas fa-download", id="download_csdm_button",
#     tooltip="Download file as .csdf"
# )


# # download buttons callback method
# @app.callback(
#     Output("download_csdm_button", "disabled"),
#     [Input("nmr_spectrum", "figure")],
#     [State("filename_dataset", "children")],
# )
# def toggle_download_buttons(value, filename_dataset):
#     """Toggle download buttons."""
#     if filename_dataset in [None, ""]:
#         return True
#     return False


# Button group 1 -------------------------------------------------------------------- #
group2_buttons = dbc.ButtonGroup([dropdown_downloadables])


# toolbar icons --------------------------------------------------------------------- #
toolbar = dbc.Row(
    [dbc.Col(group_0_buttons), dbc.Col(group_1_buttons), dbc.Col(group2_buttons)]
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("toolbar-collapse", "is_open"),
    [Input("toolbar-toggler", "n_clicks")],
    [State("toolbar-collapse", "is_open")],
)
def toggle_toolbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
