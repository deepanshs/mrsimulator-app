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

# Get meta tags.
with open(PATH + "meta_tags.json", "r") as f:
    meta_tags = json.load(f)

# Get splash screens for mobile devices.
with open(PATH + "splash_screen.json", "r") as f:
    links = json.load(f)

# Add splash screens to the page as <link \> in the header.
html_links = ""
for item in links:
    if "media" in item.keys():
        html_links += "<link rel='{0}' href='{1}' media='{2}'/>".format(
            item["rel"], item["href"], item["media"]
        )
    else:
        html_links += "<link rel='{0}' href='{1}'/>".format(item["rel"], item["href"])

# Initialize dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=external_scripts,
    meta_tags=[*meta_tags, *apple_meta_tags],
)
app.config.suppress_callback_exceptions = True
app.title = "Mrsimulator"


# Dash html layout string
html_head = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
"""
body_tail = """
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
app.index_string = html_head + html_links + body_tail
