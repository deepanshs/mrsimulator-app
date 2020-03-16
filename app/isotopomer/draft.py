# -*- coding: utf-8 -*-
import dash_core_components as dcc

# set up isotopomer dropdown
isotopomer_set = dcc.Dropdown(
    id="isotopomer-dropdown", options=[], value=0, multi=False
)


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
    isotopomer_dropdown_options = [None] * len(isotopomers)
    for i, item in enumerate(isotopomers):
        isotope_list = "-".join([site["isotope"] for site in item["sites"]])
        isotopomer_dropdown_options[i] = {
            "label": f"Isotopomer-{i} ({isotope_list})",
            "value": i,
        }

    return isotopomer_dropdown_options
