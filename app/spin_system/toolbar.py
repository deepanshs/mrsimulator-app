# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_button

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]

# # button to activate a json text editor
# advanced_spin_system_editor_button = custom_button(
#     icon_classname="fas fa-edit",
#     id="json-file-editor-button",
#     tooltip="Advanced spin-system editor",
#     outline=True,
#     color="dark",
#     active=False,
# )

# # the json text editor area
# advanced_spin_system_text_area = dbc.Textarea(
#     className="m-0 p-2",
#     id="json-file-editor",
#     placeholder="Spin system editor",
#     draggable="False",
#     spellCheck="False",
#     bs_size="sm",
#     rows=10,
#     value="",
# )


# advanced_spin_system_text_area_collapsible = dbc.Collapse(
#     advanced_spin_system_text_area, id="json-file-editor-collapse"
# )

button = custom_button(
    icon_classname="fac fa-spin-systems",
    outline=True,
    color="dark",
    disabled=True,
    id="__spin_system__",
)

# button to create a new spin-system
new_spin_system = custom_button(
    # text="Add",
    icon_classname="fas fa-plus-circle",
    id="add-spin-system-button",
    tooltip="Add a new spin system",
    outline=True,
    color="dark",
)

# button to duplicate an spin-system
duplicate_spin_system = custom_button(
    # text="Duplicate",
    icon_classname="fas fa-clone",
    id="duplicate-spin-system-button",
    tooltip="Duplicate selected spin system",
    outline=True,
    color="dark",
)

# button to delete an spin-system
trash_spin_system = custom_button(
    # text="Remove",
    icon_classname="fas fa-minus-circle",
    id="remove-spin-system-button",
    tooltip="Remove selected spin system",
    outline=True,
    color="dark",
)


search_spin_system = dcc.Input(
    value="", id="search-spin-system", placeholder="Search spin systems", type="search"
)

spin_system_edit_tools = html.Div(
    [button, new_spin_system, duplicate_spin_system, trash_spin_system],
    style={"display": "none"},
)
