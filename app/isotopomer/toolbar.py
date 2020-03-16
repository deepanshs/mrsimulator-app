# -*- coding: utf-8 -*-
# import dash
import dash_bootstrap_components as dbc

from app.custom_widgets import custom_button

# import dash_core_components as dcc
# import dash_html_components as html

# from dash.dependencies import Input
# from dash.dependencies import Output
# from dash.dependencies import State
# from app.app import app

advanced_isotopomer_editor_button = custom_button(
    icon_classname="fas fa-edit",
    id="json-file-editor-button",
    tooltip="Advanced isotopomer editor",
    active=False,
    outline=True,
    color="dark",
    style={"float": "right"},
)

advanced_isotopomer_text_area = dbc.Textarea(
    className="mb-3 p-0",
    id="json-file-editor",
    placeholder="Isotopomer editor",
    draggable="False",
    contentEditable="False",
    spellCheck="False",
    bs_size="sm",
    rows=10,
    value="",
)

advanced_isotopomer_text_area_collapsible = dbc.Collapse(
    advanced_isotopomer_text_area, id="json-file-editor-collapse"
)

add_isotopomer = custom_button(
    icon_classname="fas fa-plus-circle",
    id="add-isotopomer-button",
    tooltip="Add isotopomer",
    active=False,
    outline=True,
    color="dark",
    style={"float": "right"},
)


toolbar = dbc.ButtonGroup([add_isotopomer, advanced_isotopomer_editor_button])
