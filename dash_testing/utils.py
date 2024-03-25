# -*- coding: utf-8 -*-
"""Useful functions to use with dash tests"""


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


def wait_for_and_click(dash_duo, selector, clicks=1, timeout=3):
    """Wait for element by selector and click spesified number of times"""
    dash_duo.wait_for_element(selector, timeout=timeout)
    dash_duo.multiple_click(selector, clicks=clicks)


def get_element_value(dash_duo, selector):
    """Return the value attribute of specified element by selector"""
    return dash_duo.find_element(selector).get_attribute("value")
