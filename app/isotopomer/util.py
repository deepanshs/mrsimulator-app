# -*- coding: utf-8 -*-
import math
from datetime import datetime

import dash_html_components as html
from dash.dependencies import ClientsideFunction
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate

from app.app import app

__author__ = ["Deepansh J. Srivastava", "Maxwell C. Venetos"]
__email__ = ["srivastava.89@osu.edu", "venetos.5@buckeyemail.osu.edu"]

label_dictionary = {
    "isotope": "Isotope",
    "shielding_symmetric": "Symmetric Shielding",
    "quadrupolar": "Quadrupolar",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "zeta": "ζ",
    "eta": "η",
    "isotropic_chemical_shift": "Shift (δ)",
    "Cq": "Cq",
}
default_unit = {
    "isotope": "",
    "isotropic_chemical_shift": "ppm",
    "Cq": "MHz",
    "zeta": "ppm",
    "eta": "",
    "alpha": "°",
    "beta": "°",
    "gamma": "°",
}


def get_isotopomer_index_containing_this_isotope(isotopomers, isotope):
    index = []
    for i, item in enumerate(isotopomers):
        for site in item["sites"]:
            if site["isotope"] == isotope:
                index.append(i)
                break
    return index


def filter_isotopomer_list(isotopomers, isotope):
    index = get_isotopomer_index_containing_this_isotope(isotopomers, isotope)
    isotopomer_list = [isotopomers[item] for item in index]
    return isotopomer_list


def get_isotopomer_dropdown_options(isotopomers, isotope):
    index = get_isotopomer_index_containing_this_isotope(isotopomers, isotope)

    isotopomer_dropdown_options = []
    for i, item in enumerate(index):
        isotope_list = "-".join(
            [site["isotope"] for site in isotopomers[item]["sites"]]
        )
        isotopomer_dropdown_options.append(
            {"label": f"Isotopomer-{item} ({isotope_list})", "value": i}
        )
    return isotopomer_dropdown_options


def get_all_isotopomer_dropdown_options(isotopomers):
    isotopomer_dropdown_options = [None for _ in range(len(isotopomers))]
    for i, item in enumerate(isotopomers):
        isotope_list = "-".join([site["isotope"] for site in item["sites"]])
        isotopomer_dropdown_options[i] = {
            "label": f"Isotopomer-{i} ({isotope_list})",
            "value": i,
        }

    return isotopomer_dropdown_options


def attribute_value_pair(key, value, space):
    if not isinstance(value, str):
        value = round(value, 10)
    return html.Div(
        f"{label_dictionary[key]}: {value} {default_unit[key]}",
        className=f"pl-{space}"
        # [html.Div(label_dictionary[key]), html.Div(f"{value} {default_unit[key]}"),],
        # className=f"pl-{space} d-flex justify-content-between",
    )


title = html.H5("Load isotopomers or start creating")
icon = html.Span(
    [html.I(className="fac fa-isotopomers fa-4x"), html.H6("Create isotopomers")],
    id="open-edit_isotopomer",
)
section1 = html.Div([title, icon])


@app.callback(
    Output("add-isotopomer-button", "n_clicks_timestamp"),
    [Input("open-edit_isotopomer", "n_clicks")],
    [State("add-isotopomer-button", "n_clicks_timestamp")],
)
def open_edit_isotopomer(_, n):
    if _ is None:
        raise PreventUpdate
    return int(datetime.now().timestamp() * 1000)


# section2 = html.Section(examples)
blank_display = html.Div([section1], className="blank-isotopomer-display")


def print_isotopomer_info(json_data):
    """Return a html for rendering the display in the read-only isotopomer section."""
    output = []

    for i, isotopomer in enumerate(json_data):
        local = []

        name_div = html.B(f"Isotopomer {i}", className="")
        if "name" in isotopomer:
            if isotopomer["name"] not in ["", None]:
                name_div = html.B(isotopomer["name"], className="")

        local.append(name_div)

        if "description" in isotopomer:
            if isotopomer["description"] not in ["", None]:
                local.append(
                    html.Div(isotopomer["description"][:25] + " ... ", className="")
                )

        abundance = "100" if "abundance" not in isotopomer else isotopomer["abundance"]
        local.append(html.Div(f"Abundance: {abundance} %", className=""))

        if "sites" in isotopomer:
            for site in isotopomer["sites"]:
                for site_attribute, val in site.items():
                    if isinstance(val, dict):
                        local.append(
                            html.Div(
                                f"{label_dictionary[site_attribute]}", className="pl-2"
                            )
                        )
                        for key, value in val.items():
                            if value is not None:
                                value = (
                                    math.degrees(value)
                                    if key in ["alpha", "beta", "gamma"]
                                    else value
                                )
                                value = value * 1e-6 if key == "Cq" else value
                                local.append(attribute_value_pair(key, value, 4))
                    else:
                        local.append(attribute_value_pair(site_attribute, val, 2))

        # local.append(html.Br())
        output.append(
            html.Li(
                [
                    html.H6(i),
                    html.Div(
                        [
                            html.A(local),
                            # dbc.Button(
                            #     "X",
                            #     color="danger",
                            #     block=True,
                            #     id={"type": "initiate-remove-isotopomer", "index": i},
                            # ),
                        ]
                    ),
                ],
                # draggable="true",
                className="list-group-item",
            )
        )

    # output.append(html.Li(icon))

    return html.Div([html.Ul(output, className="list-group")], className="display-form")


# @app.callback(
#     Output("remove-isotopomer-button", "n_clicks_timestamp"),
#     [Input({"type": "initiate-remove-isotopomer", "index": ALL}, "n_clicks")],
#     [State("remove-isotopomer-button", "n_clicks_timestamp")],
# )
# def initiate_remove_isotopomer(_, n):
#     print("initiate", _, n)
#     if _.count(None) == len(_):
#         raise PreventUpdate
#     print("remove isotopomer", n, int(datetime.now().timestamp() * 1000))
#     return int(datetime.now().timestamp() * 1000)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_isotopomers_load"),
    Output("temp2", "children"),
    [Input("isotopomer-read-only", "children")],
    [State("config", "data")],
)
