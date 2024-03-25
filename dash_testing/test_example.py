# -*- coding: utf-8 -*-
"""This is an example test file. This can be used as a template to write other dash
tests.
"""
import time

from dash.testing.application_runners import import_app


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


# dash_duo is a pytest fixture with Selenium and needed drivers already created.
# See https://dash.plotly.com/testing for more info.
def test_example(dash_duo):
    # import_app is required. Otherwise you have to re-defined the entire app within
    # each test method.
    app = import_app("main")
    dash_duo.start_server(app)

    # Wait for the app to open
    dash_duo.wait_for_page()

    # Allow time to see the app
    time.sleep(5)
