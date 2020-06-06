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


def get_spin_system_index_containing_this_isotope(spin_systems, isotope):
    index = []
    for i, item in enumerate(spin_systems):
        for site in item["sites"]:
            if site["isotope"] == isotope:
                index.append(i)
                break
    return index


def filter_spin_system_list(spin_systems, isotope):
    index = get_spin_system_index_containing_this_isotope(spin_systems, isotope)
    spin_system_list = [spin_systems[item] for item in index]
    return spin_system_list


def get_spin_system_dropdown_options(spin_systems, isotope):
    index = get_spin_system_index_containing_this_isotope(spin_systems, isotope)

    spin_system_dropdown_options = []
    for i, item in enumerate(index):
        isotope_list = "-".join(
            [site["isotope"] for site in spin_systems[item]["sites"]]
        )
        spin_system_dropdown_options.append(
            {"label": f"Spin system-{item} ({isotope_list})", "value": i}
        )
    return spin_system_dropdown_options


def get_all_spin_system_dropdown_options(spin_systems):
    spin_system_dropdown_options = [None for _ in range(len(spin_systems))]
    for i, item in enumerate(spin_systems):
        isotope_list = "-".join([site["isotope"] for site in item["sites"]])
        spin_system_dropdown_options[i] = {
            "label": f"Spin system-{i} ({isotope_list})",
            "value": i,
        }

    return spin_system_dropdown_options


def attribute_value_pair(key, value, space):
    if not isinstance(value, str):
        value = round(value, 10)
    return html.Div(
        f"{label_dictionary[key]}: {value} {default_unit[key]}",
        className=f"pl-{space}"
        # [html.Div(label_dictionary[key]), html.Div(f"{value} {default_unit[key]}"),],
        # className=f"pl-{space} d-flex justify-content-between",
    )


title = html.H5("Load spin systems or start creating")
icon = html.Span(
    [html.I(className="fac fa-spin-systems fa-4x"), html.H6("Create spin-systems")],
    id="open-edit_spin_system",
)
section1 = html.Div([title, icon])


@app.callback(
    Output("add-spin-system-button", "n_clicks_timestamp"),
    [Input("open-edit_spin_system", "n_clicks")],
    [State("add-spin-system-button", "n_clicks_timestamp")],
    prevent_initial_call=True,
)
def open_edit_spin_system(_, n):
    if _ is None:
        raise PreventUpdate
    return int(datetime.now().timestamp() * 1000)


blank_display = html.Div([section1], className="blank-spin-system-display")


def update_spin_system_info(json_data):
    """Return a html for rendering the display in the read-only spin-system section."""
    output = []

    for i, spin_system in enumerate(json_data):
        local = []

        name_div = html.B(f"Spin system {i}", className="")
        if "name" in spin_system:
            if spin_system["name"] not in ["", None]:
                name_div = html.B(spin_system["name"], className="")

        local.append(name_div)

        if "description" in spin_system:
            if spin_system["description"] not in ["", None]:
                local.append(
                    html.Div(spin_system["description"][:25] + " ... ", className="")
                )

        abundance = (
            "100" if "abundance" not in spin_system else spin_system["abundance"]
        )
        local.append(html.Div(f"Abundance: {abundance} %", className=""))

        if "sites" in spin_system:
            for site in spin_system["sites"]:
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
                            #     id={"type": "initiate-remove-spin-system", "index": i},
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
#     Output("remove-spin-system-button", "n_clicks_timestamp"),
#     [Input({"type": "initiate-remove-spin-system", "index": ALL}, "n_clicks")],
#     [State("remove-spin-system-button", "n_clicks_timestamp")],
# )
# def initiate_remove_spin_system(_, n):
#     print("initiate", _, n)
#     if _.count(None) == len(_):
#         raise PreventUpdate
#     print("remove spin-system", n, int(datetime.now().timestamp() * 1000))
#     return int(datetime.now().timestamp() * 1000)


app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="on_spin_systems_load"),
    Output("temp2", "children"),
    [Input("spin-system-read-only", "children")],
    [State("config", "data")],
    prevent_initial_call=True,
)
