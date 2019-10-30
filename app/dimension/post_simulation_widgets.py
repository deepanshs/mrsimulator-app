# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group
from app.custom_widgets import custom_slider


__author__ = ["Maxwell Venetos"]
__email__ = ["venetos.5@buckeyemail.osu.edu"]


def gaussian_linebroadening_widget(i):
    broaden_range = {0: "0", 200: "200", 400: "400", 600: "600", 800: "800", 1000: "1000"}

    broadeningFunction = dcc.RadioItems(
        options=[
            {"label": "Lorentzian", "value": "Lorentz"},
            {"label": "Gaussian", "value": "Gaussian"},
        ],
        value="Lorentz",
        # labelStyle={'display': 'inline'}
        id=f"Apodizing_function-{i}",
    )

    line_broadening = custom_slider(
        label="Line Broadening",
        return_function=lambda x: f"\u03BB = {x/1000} kHz",
        # if broadeningFunction.value == 'Lorentz':
        min=0,
        max=1000,
        step=25,
        # elif broadeningFunction.value == 'Gaussian':
        # min=0,
        # max=10,
        # step=1,
        value=0,
        marks=broaden_range,
        id=f"broadening_points-{i}",
    )

    # return [broadeningFunction, line_broadening]
    return [line_broadening]


# @app.callback(
#     dash.dependencies.Output('Apodization', 'children'),
#     [dash.dependencies.Input('Apodizing_function-0', 'value')])
# def Apodization_label(value):
#     return value
