# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

__author__ = "Deepansh J. Srivastava"
__email__ = ["deepansh2012@gmail.com"]


# select method  -------------------------------------------------------------------- #
select_method = dcc.Dropdown(
    id="select-method",
    value=0,
    searchable=False,
    clearable=False,
    placeholder="View simulation from method ...",
)


# toolbar icons --------------------------------------------------------------------- #
toolbar_select_method = html.Div(select_method, style={"display": "none"})
