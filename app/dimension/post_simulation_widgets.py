# -*- coding: utf-8 -*-
from app.custom_widgets import custom_slider


__author__ = ["Maxwell Venetos"]
__email__ = ["venetos.5@buckeyemail.osu.edu"]


def gaussian_linebroadening_widget(i):
    broaden_range = {0: "0", 2: "2", 4: "4", 6: "6", 8: "8", 10: "10"}
    line_broadening = custom_slider(
        label="Line Broadening",
        return_function=lambda x: f"{x}  ppm",
        min=0,
        max=10,
        step=1,
        value=0,
        marks=broaden_range,
        id=f"broadening_points-{i}",
    )

    return [line_broadening]
