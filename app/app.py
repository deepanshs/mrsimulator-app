# -*- coding: utf-8 -*-
import json

import dash_bootstrap_components as dbc
from dash import Dash

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

PATH = "config/"

# Get external java scripts from JSON file.
with open(PATH + "external_scripts.json", "r") as f:
    external_scripts = json.load(f)

# Get apple ios configuration from JSON file.
with open(PATH + "apple_ios_tags.json", "r") as f:
    apple_meta_tags = json.load(f)

with open(PATH + "meta_tags.json", "r") as f:
    meta_tags = json.load(f)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=external_scripts,
    meta_tags=[*meta_tags, *apple_meta_tags],
)
app.config.suppress_callback_exceptions = True
app.title = "Mrsimulator"

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"/>
        <link rel="apple-touch-startup-image" href="/assets/launch.png">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
