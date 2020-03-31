# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_widgets import custom_button


advanced_isotopomer_editor_button = custom_button(
    icon_classname="fas fa-edit",
    id="json-file-editor-button",
    tooltip="Advanced isotopomer editor",
    outline=True,
    color="dark",
    active=False,
)

advanced_isotopomer_text_area = dbc.Textarea(
    className="m-0 p-2",
    id="json-file-editor",
    placeholder="Isotopomer editor",
    draggable="False",
    spellCheck="False",
    bs_size="sm",
    rows=10,
    value="",
)

advanced_isotopomer_text_area_collapsible = dbc.Collapse(
    advanced_isotopomer_text_area, id="json-file-editor-collapse"
)

new_isotopomer = custom_button(
    icon_classname="fas fa-plus-circle",
    id="add-isotopomer-button",
    tooltip="Add",
    outline=True,
    color="dark",
)

duplicate_isotopomer = custom_button(
    icon_classname="fas fa-clone",
    id="duplicate-isotopomer-button",
    tooltip="Duplicate",
    outline=True,
    color="dark",
)

trash_isotopomer = custom_button(
    icon_classname="fas fa-trash",
    id="trash-isotopomer-button",
    tooltip="Remove",
    outline=True,
    color="dark",
)

group_one = dbc.ButtonGroup([new_isotopomer, duplicate_isotopomer, trash_isotopomer])
group_two = dbc.ButtonGroup([advanced_isotopomer_editor_button])
toolbar = html.Div([group_one, group_two], className="toolbar")
