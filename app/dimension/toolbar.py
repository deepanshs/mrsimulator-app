# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_button

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]

# button to create a new method
new_method = custom_button(
    # text="Add",
    icon_classname="fas fa-plus-circle",
    id="add-method-button",
    tooltip="Add",
    outline=True,
    color="dark",
)

# button to duplicate an method
duplicate_method = custom_button(
    # text="Duplicate",
    icon_classname="fas fa-clone",
    id="duplicate-method-button",
    tooltip="Duplicate",
    outline=True,
    color="dark",
)

# button to delete an method
trash_method = custom_button(
    # text="Remove",
    icon_classname="fas fa-minus-circle",
    id="trash-method-button",
    tooltip="Remove",
    outline=True,
    color="dark",
)

# # button to import an method
# import_method = dcc.Upload(
#     custom_button(
#         # text="Remove",
#         icon_classname="fas fa-hdd",
#         tooltip="Import",
#         outline=True,
#         color="dark",
#         id="_upload_method_button",
#     ),
#     id="upload-method-local-button",
# )


search_method = dcc.Input(
    value="", id="search-method", placeholder="Search methods", type="search"
)

edit_tools = dbc.ButtonGroup([new_method, duplicate_method, trash_method])
method_toolbar = html.Div([edit_tools, search_method], className="toolbar")
