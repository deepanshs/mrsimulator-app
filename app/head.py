# -*- coding: utf-8 -*-
import json


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

# Get external links for mobile devices.
with open(PATH + "external_links.json", "r") as f:
    external_links = json.load(f)


def create_links(link_dict):
    html_string = ""
    for item in link_dict:
        string = " ".join([f"{k}='{v}'" for k, v in item.items()])
        html_string += f"<link {string}/>"
    return html_string


# Add external links to the page as <link \> in the header.
html_links = create_links(external_links)


# html head layout
html_head = """
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
"""

# html body tags
html_body = """
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
      <!-- Global site tag (gtag.js) - Google Analytics -->
      <script async src="https://www.googletagmanager.com/gtag/js?id=G-L6STWPJCHV">
      </script>
      <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-L6STWPJCHV');
      </script>
    </footer>
  </body>
</html>
"""
index_string = "".join([html_head, html_links, html_body])

head_config = {
    "external_scripts": external_scripts,
    "meta_tags": [*meta_tags, *apple_meta_tags],
    "index_string": index_string,
}
