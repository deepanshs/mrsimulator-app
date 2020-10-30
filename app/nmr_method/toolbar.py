# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_button

__author__ = ["Deepansh J. Srivastava"]
__email__ = ["deepansh2012@gmail.com"]


button = custom_button(
    icon_classname="fas fa-cube",
    outline=True,
    color="dark",
    disabled=True,
    id="__method__",
)

# button to create a new method
new_method = custom_button(
    # text="Add",
    icon_classname="fas fa-plus-circle",
    id="add-method-button",
    tooltip="Add a method",
    outline=True,
    color="dark",
)

# button to duplicate an method
duplicate_method = custom_button(
    # text="Duplicate",
    icon_classname="fas fa-clone",
    id="duplicate-method-button",
    tooltip="Duplicate selected method",
    outline=True,
    color="dark",
)

# button to delete an method
trash_method = custom_button(
    # text="Remove",
    icon_classname="fas fa-minus-circle",
    id="remove-method-button",
    tooltip="Remove selected method",
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

method_edit_tools = html.Div(
    children=[button, new_method, duplicate_method, trash_method],
    style={"display": "none"},
)
# method_toolbar = html.Div([search_method], className="toolbar")
