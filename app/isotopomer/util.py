# -*- coding: utf-8 -*-
import math

import dash_html_components as html

label_dictionary = {
    "isotope": "Isotope",
    "shielding_symmetric": "Symmetric Shielding",
    "quadrupolar": "Quadrupolar",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "zeta": "Anisotropy (ζ)",
    "eta": "Asymmetry (η)",
    "isotropic_chemical_shift": "Isotropic shift (δ)",
    "Cq": "Coupling constant (Cq)",
}
default_unit = {
    "isotope": "",
    "isotropic_chemical_shift": "ppm",
    "Cq": "MHz",
    "zeta": "ppm",
    "eta": "",
    "alpha": "deg",
    "beta": "deg",
    "gamma": "deg",
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
    return html.Div(
        f"{label_dictionary[key]}: {value} {default_unit[key]}",
        className=f"pl-{space}"
        # [html.Div(label_dictionary[key]), html.Div(f"{value} {default_unit[key]}"),],
        # className=f"pl-{space} d-flex justify-content-between",
    )


def blank_display():
    title = html.H5("Load an isotopomer or create your own")
    icon = html.Span(
        html.I(className="fac fa-isotopomers fa-4x"), id="open-load_isotopomer"
    )
    return html.Div([title, icon], className="blank-isotopomer-display")


def print_info(json_data):
    """Return a html for rendering the display in the read-only isotopomer section."""
    output = []
    keys = json_data.keys()

    if "isotopomers" not in keys:
        return blank_display()

    for i, isotopomer in enumerate(json_data["isotopomers"]):
        local = [html.Br()]
        name = "" if "name" not in isotopomer else isotopomer["name"]

        local.append(html.H5(f"Isotopomer {i}: {name}", className=""))

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
        local.append(html.Br())
        output.append(html.Li(local))

    return html.Div(html.Ul(output), className="display-form")
