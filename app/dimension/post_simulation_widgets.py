# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from app.custom_widgets import custom_input_group

__author__ = ["Maxwell C. Venetos"]
__email__ = ["venetos.5@buckeyemail.osu.edu"]


def gaussian_linebroadening_widget(i):

    broadeningFunction = dcc.RadioItems(
        options=[
            {"label": "Lorentzian", "value": 0},
            {"label": "Gaussian", "value": 1},
        ],
        value=0,  # "Lorentz",
        labelStyle={"display": "inline-block", "width": "50%"},
        id=f"Apodizing_function-{i}",
    )

    # broaden_range = {
    #     0: "0 Hz",
    #     200: "200 Hz",
    #     400: "400 Hz",
    #     600: "600 Hz",
    #     800: "800 Hz",
    #     1000: "1 kHz",
    # }
    # line_broadening = custom_slider(
    #     label="Line Broadening",
    #     return_function=lambda x: f"\u03BB = {x/1000} kHz"
    #     if x > 1000
    #     else f"\u03BB = {x} Hz",
    #     min=0,
    #     max=1000,
    #     step=25,
    #     value=50,
    #     marks=broaden_range,
    #     id=f"broadening_points-{i}",
    # )
    line_broadening = custom_input_group(
        id=f"broadening_points-{i}",
        append_label="Hz",
        prepend_label="Factor",
        value=10,
        debounce=True,
    )

    return html.Div(
        [broadeningFunction, line_broadening], className="collapsible-body-control form"
    )

    # return [line_broadening]
