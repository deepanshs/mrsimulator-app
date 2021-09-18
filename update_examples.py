# -*- coding: utf-8 -*-
import json
import sys

import requests
from bs4 import BeautifulSoup


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@buckeyemail.osu.edu"


URL = "http://www.ssnmr.org/measurements"
ROOT_HREF_DIR = "http://www.ssnmr.org"
DEFAULT_JSON_PATH = "./app/assets/example_link.json"


# TODO: Implement modes of sorting examples into sections
# TODO: Add more ways to group/


def help_message():
    """Help message for command line usage"""
    return (
        "Update Examples JSON.\n"
        "\n"
        "Usage:\n"
        "  python update_examples.py -h | --help\n"
        "  python update_examples.py -a | --all\n"
        "  python update_examples.py --update <name>... \n"
        "  python update_examples.py --exclude <name>... \n"
        "  python update_examples.py --file <path> \n"
        "  python update_examples.py --group ('isotope' | 'method') \n"
        "\n"
        "Options:\n"
        "  -h --help        Show this screen.\n"
        "  -a --all         Update all examples except excluded. Defaults to --all.\n"
        "  --update         Update or add single example or list of examples.\n"
        "  --exclude        Exclude example or list of examples by name.\n"
        "  --file           json file [default: /app/assets/examples_link.json].\n"
        "  --group          Group examples by (default: no groups).\n"
        "\n"
    )


def get_names_and_links():
    """Open URL and parse table for names and links of examples

    Returns:
        (List) names: list of example names
        (List) links: list of url strings for examples page
    """
    # Request and load html into BeautifulSoup object
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())

    # Find measurements table
    table = soup.find_all("table")[0]

    # Remove table header and newline charcters
    table.contents = [x for x in table.contents if x != "\n"]
    table.contents.pop(0)

    # Create list of sample names
    names = table.find_all("td", class_="views-field views-field-field-sample-name")
    names = [name.string.strip() for name in names]

    # Create list of sample page links
    links = table.find_all("td", class_="views-field views-field-view-node")
    links = [next(link.children)["href"] for link in links]

    return names, links


def open_example_link(link):
    """Opens the page contents from ROOT_HREF_DIR + 'link' and returns list of str items
    needed for examples json. Will return None if no specified item is found.

    Args:
        (str) link: suffix of page link for example

    Returns:
        (str) descr: description for example thumbnail.
        (str) mrsim_link: url link to .mrsim file for example.
        (str) img_link: url link to .svg (or other ext) file for thumbnail.
    """
    # NOTE: Could add more metadata returned for finer groupings (future)

    # Open example link
    page = requests.get(ROOT_HREF_DIR + link)
    soup = BeautifulSoup(page.content, "html.parser")

    # Locate and grab example description (title of example)
    descr = soup.find("h1", class_="page-header").get_text().strip()

    # Locate and grab example .mrsim link
    file_links = [fl.find("a") for fl in soup.find_all("span", class_="file-link")]
    is_mrsim = [fl.get_text().split(".")[-1] == "mrsim" for fl in file_links]
    mrsim_link = None
    if sum(is_mrsim) == 1:
        mrsim_link = file_links[is_mrsim.index(True)]["href"]

    # Locate and grab example image thumbnail link
    images = soup.find_all(
        "div",
        class_="field field--name-field-image field--type-image field--label-above",
    )
    is_thumbnail = [im.get_text().strip() == "Thumbnail Image" for im in images]
    img_link = None
    if sum(is_thumbnail) == 1:
        img_link = ROOT_HREF_DIR + images[is_thumbnail.index(True)].find("img")["src"]

    # Add more metadata grabbing here

    return descr, mrsim_link, img_link


def make_example_list(names, links, exclude):
    """Creates list of example dictonaries to be seralized into json.

    Args:
        (List) names: list of example names
        (List) links: list of example links
        (List) exclude: optional set of names to exclude

    Returns:
        (List) examples_list: list of dictonaries
    """
    examples_list = []

    for name, link in zip(names, links):
        # Do not include excluded examples
        if name in exclude:
            print(f"skipping {name}")
            continue

        descr, mrsim_link, img_link = open_example_link(link)

        # Do not add if no .mrsim file
        if mrsim_link is None:
            print(f"skipping {name} (has no .mrsim file)")
            continue

        examples_list.append(
            {
                "label": name,
                "value": mrsim_link,
                "img": img_link,
                "description": descr,
            }
        )

        # Log that example has been added
        log_str = f"added {name}"
        if img_link is None:
            log_str = log_str.ljust(35) + " (no img)"
        print(log_str)

    return examples_list


def apply_groupings(examples_list, grouping=""):
    """Creates multiple groups from a list of examples based on desired grouping method.

    Args:
        (List) examples_list: list of examples dictonaries.

    Returns:
        (Dictonary) examples_dict: key is name of group & val is list of examples.
    """
    # TODO: Implement different types of groupings

    return {"All Examples": examples_list}


def remove_groupings(examples_dict):
    """Removes groupings from examples_dict and returns examples_list"""
    examples_list = []
    for group in examples_dict.values():
        examples_list += group

    return examples_list


def update_all_examples(exclude):
    """Makes new example list from valid examples on ssnmr.org excluding examples in
    exclude

    Args:
        (List) exclude: list of names to exculde

    Returns:
        (List) examples_list: new list of all examples
    """
    print("Updating all examples")

    names, links = get_names_and_links()

    print(f"Found {len(names)} measurements")

    return make_example_list(names, links, exclude)


def update_spesific_examples(update, json_file, exclude):
    """Updates only named examples in update, adding them to examples if they do not
    already exist

    Args:
        (List) update: list of examples to update/add
        (str) json_file: path to json file holding links
        (List) exclude: list of examples to exclude

    Returns:
        (List) examples_list: new list of all examples
    """
    print(f"Updating {len(update)} examples")
    print("Fetching new data. This may take some time...\n")

    with open(json_file, "a+") as f:
        try:
            examples_list = remove_groupings(json.load(f))
        except json.decoder.JSONDecodeError:
            examples_list = []

    names, links = get_names_and_links()
    known_examples = [ex["label"] for ex in examples_list]

    # Loop through examples to update
    for up_name in update:
        if up_name not in names:
            print(f"{up_name} not found")
            continue

        if up_name in exclude:
            print(f"skipping {up_name}")
            continue

        descr, mrsim_link, img_link = open_example_link(links[names.index(up_name)])

        # Do not add if no .mrsim file
        if mrsim_link is None:
            print(f"skipping {up_name} (has no .mrsim file)")
            continue

        if up_name in known_examples:
            examples_list[known_examples.index(up_name)]["value"] = mrsim_link
            examples_list[known_examples.index(up_name)]["img"] = img_link
            examples_list[known_examples.index(up_name)]["description"] = descr
            log_str = f"update {up_name}"
        else:
            examples_list.append(
                {
                    "label": up_name,
                    "value": mrsim_link,
                    "img": img_link,
                    "description": descr,
                }
            )
            log_str = f"added  {up_name}"

        if img_link is None:
            log_str = log_str.ljust(35) + " (no img)"
        print(log_str)

    return examples_list


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print(help_message())
        exit(0)

    # parse optional json path
    json_file = DEFAULT_JSON_PATH
    if "--file" in sys.argv:
        json_file = sys.argv[sys.argv.index("--file") + 1]

    # parse option exclude examples
    exclude = []
    if "--exclude" in sys.argv:
        start = sys.argv.index("--exclude") + 1
        end = start
        while end < len(sys.argv) and not sys.argv[end].startswith("-"):
            end = end + 1
        exclude = sys.argv[start:end]

    # parse optional update examples
    update = []
    if "--update" in sys.argv:
        start = sys.argv.index("--update") + 1
        end = start
        while end < len(sys.argv) and not sys.argv[end].startswith("-"):
            end = end + 1
        update = sys.argv[start:end]

    if "-a" in sys.argv or "--all" in sys.argv or update == []:
        examples_list = update_all_examples(exclude)
    else:
        examples_list = update_spesific_examples(update, json_file, exclude)

    # Apply groupings
    group = ""
    if "--group" in sys.argv:
        group = sys.argv[sys.argv.index("--group") + 1]

    examples_dict = apply_groupings(examples_list, group)

    with open(json_file, "w+") as f:
        json.dump(examples_dict, f, indent=4)

    print()
    print(f"Updated examples have been written to {json_file}")
