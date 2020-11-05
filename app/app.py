# -*- coding: utf-8 -*-
import datetime
import json

import dash_bootstrap_components as dbc
from dash import Dash

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]

now = datetime.datetime.now()
year = now.year

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
with open(PATH + "splash_screen_links.json", "r") as f:
    splash_screen_links = json.load(f)

# Get external links for mobile devices.
with open(PATH + "external_links.json", "r") as f:
    external_links = json.load(f)


def create_links(link_dict):
    html_string = ""
    for item in link_dict:
        if "media" in item.keys():
            html_string += "<link rel='{0}' href='{1}' media='{2}'/>".format(
                item["rel"], item["href"], item["media"]
            )
        else:
            html_string += "<link rel='{0}' href='{1}'/>".format(
                item["rel"], item["href"]
            )
    return html_string


html_link_str = ""
# Add splash screen links to the page as <link \> in the header.
html_link_str += create_links(splash_screen_links)

# Add external links to the page as <link \> in the header.
html_link_str += create_links(external_links)

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
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-L6STWPJCHV">
    </script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-L6STWPJCHV');
    </script>
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
app.index_string = html_head + html_link_str + body_tail
