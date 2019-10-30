# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html

from .modal.file_info import file_info

colors = {"background": "#e2e2e2", "text": "#585858"}

filename_datetime = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H5(id="filename_dataset")),
                # dbc.Col(
                #     custom_button(
                #         text="",
                #         icon="fas fa-edit",
                #         id="json-file-editor-toggler",
                #         tooltip="Edit the isotopomer file.",
                #         active=False,
                #         outline=True,
                #         style={"float": "right"},
                #     )
                # ),
            ]
        ),
        file_info,
        html.H6(
            id="data_description", style={"textAlign": "left", "color": colors["text"]}
        ),
    ]
)

# text_area = (
#     dbc.Textarea(
#         className="mb-3",
#         id="json-file-editor",
#         placeholder="A Textarea",
#         draggable="False",
#         contentEditable="False",
#         bs_size="sm",
#         rows=10,
#         value="",
#     ),
# )

# text_area_collapsible = dbc.Collapse(text_area, id="json-file-editor-collapse")


# @app.callback(
#     Output("json-file-editor-collapse", "is_open"),
#     [Input("json-file-editor-toggler", "n_clicks")],
#     [State("json-file-editor-collapse", "is_open")],
# )
# def toggle_json_file_editor_collapse(n, is_open):
#     """Callback for toggling collapsible json editor."""
#     if n:
#         return not is_open
#     return is_open


# @app.callback(Output("json-file-editor", "value"), [Input("local-metadata", "data")])
# def update_json_editor_contents(data):
#     """Update JSON editor contents when a file is loaded."""
#     if data is None:
#         return ""
#     return json.dumps(data["isotopomers"], indent=2, ensure_ascii=True)


sidebar = dbc.Card(
    dbc.CardBody([filename_datetime]),
    # text_area_collapsible]),
    # slide_from_left]),
    className="h-100 my-card-sidebar",
    inverse=False,
)
