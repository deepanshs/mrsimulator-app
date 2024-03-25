# -*- coding: utf-8 -*-
import datetime
import os

import dash_bootstrap_components as dbc
from celery import Celery
from dash import Dash
from dash import dcc
from dash import html

from .head import head_config
from .utils import slogger

__author__ = "Deepansh J. Srivastava"
__email__ = "srivastava.89@osu.edu"
__version__ = "v0.4.0dev1"

now = datetime.datetime.now()
year = now.year


redis_url = os.environ.get("REDIS_URL", "")
slogger("tasks.py", f"declare celery_app: redis_url={redis_url}")
celery_app = Celery("query", backend=redis_url, broker=redis_url)
slogger("tasks.py", "celery_app declared successfully")

print("NAME", __name__)

# Initialize dash app
app = Dash(
    __name__,
    title="Mrsimulator",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    **head_config,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        # html.Div(id="placeholder"),
        html.A(id="url-search", href=""),
    ],
    className="main",
)
