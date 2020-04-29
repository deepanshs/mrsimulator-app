# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_button

__author__ = "Deepansh J. Srivastava"
__email__ = ["srivastava.89@osu.edu", "deepansh2012@gmail.com"]

# # button to activate a json text editor
# advanced_isotopomer_editor_button = custom_button(
#     icon_classname="fas fa-edit",
#     id="json-file-editor-button",
#     tooltip="Advanced isotopomer editor",
#     outline=True,
#     color="dark",
#     active=False,
# )

# # the json text editor area
# advanced_isotopomer_text_area = dbc.Textarea(
#     className="m-0 p-2",
#     id="json-file-editor",
#     placeholder="Isotopomer editor",
#     draggable="False",
#     spellCheck="False",
#     bs_size="sm",
#     rows=10,
#     value="",
# )


# advanced_isotopomer_text_area_collapsible = dbc.Collapse(
#     advanced_isotopomer_text_area, id="json-file-editor-collapse"
# )

# button to create a new isotopomer
new_isotopomer = custom_button(
    # text="Add",
    icon_classname="fas fa-plus-circle",
    id="add-isotopomer-button",
    tooltip="Add a new isotopomer",
    outline=True,
    color="dark",
)

# button to duplicate an isotopomer
duplicate_isotopomer = custom_button(
    # text="Duplicate",
    icon_classname="fas fa-clone",
    id="duplicate-isotopomer-button",
    tooltip="Duplicate selected isotopomer",
    outline=True,
    color="dark",
)

# button to delete an isotopomer
trash_isotopomer = custom_button(
    # text="Remove",
    icon_classname="fas fa-minus-circle",
    id="trash-isotopomer-button",
    tooltip="Remove selected isotopomer",
    outline=True,
    color="dark",
)

# button to import an isotopomer
import_isotopomer = dcc.Upload(
    custom_button(
        # text="Remove",
        icon_classname="fas fa-hdd",
        tooltip="Import isotopomers from file",
        outline=True,
        color="dark",
        id="_upload_isotopomer_button",
    ),
    id="upload-isotopomer-local-button",
)


search_isotopomer = dcc.Input(
    value="", id="search-isotopomer", placeholder="Search isotopomers", type="search"
)

edit_tools = dbc.ButtonGroup([new_isotopomer, duplicate_isotopomer, trash_isotopomer])

toolbar = html.Div(
    [edit_tools, import_isotopomer, search_isotopomer], className="toolbar"
)
