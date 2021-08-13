# -*- coding: utf-8 -*-
"""This test preforms the following actions
  1. Opens mrsimulator-app to the landing page
  2. Clicks on 'Open App'
  3. Clicks on 'File' > 'Open...'
  4. Uploads a spesified test file
  5. Ensures file has loaded correctly
"""
import os

from dash.testing.application_runners import import_app

from dash_testing.utils import get_element_value
from dash_testing.utils import wait_for_and_click


__author__ = "Matthew D. Giammar"
__email__ = "giammar.7@osu.edu"


DIRNAME = os.path.dirname(__file__)


def test_none(dash_duo):
    app = import_app("main")
    dash_duo.start_server(app)
    dash_duo.wait_for_page()

    wait_for_and_click(dash_duo, "#simulator-app")
    wait_for_and_click(dash_duo, ".master-toolbar li:nth-child(1)")

    # Upload file
    abs_path = os.path.join(DIRNAME, "./files/upload_test.mrsim")
    upload = dash_duo.driver.find_element_by_xpath(
        "//*[@id='open-mrsimulator-file']/div/input"
    )
    upload.send_keys(abs_path)

    # Home page
    dash_duo.wait_for_contains_text(
        "#info-read-only > div > div:nth-child(1) > h4", text="Test"
    )
    desc = dash_duo.find_element("#info-read-only > div > div.card > div").text
    n_mth = dash_duo.find_element("#info-read-only > div > div:nth-child(4) > div").text
    n_sys = dash_duo.find_element("#info-read-only > div > div:nth-child(6) > div").text
    assert desc == "This is a test file."
    assert n_mth == "Number of methods: 1"
    assert n_sys == "Number of spin systems: 2"

    # Method
    dash_duo.multiple_click("#view-methods", 1)
    assert dash_duo.find_element("#method-title").text == "BlochDecaySpectrum"
    assert get_element_value(dash_duo, "#magnetic_flux_density") == "14.1"
    assert get_element_value(dash_duo, "#rotor_frequency") == "10"
    assert get_element_value(dash_duo, "#rotor_angle") == "54.7356103172"

    assert get_element_value(dash_duo, "#count-0") == "1024"
    assert get_element_value(dash_duo, "#spectral_width-0") == "30"
    assert get_element_value(dash_duo, "#reference_offset-0") == "0"

    # Spin system 0
    dash_duo.multiple_click("#view-spin_systems", 1)
    assert dash_duo.find_element("#spin-system-title").text == "7Li test 0"
    assert get_element_value(dash_duo, "#spin-system-abundance") == "65"
    assert get_element_value(dash_duo, "#isotope") == "7Li"
    assert get_element_value(dash_duo, "#isotropic_chemical_shift") == "-5"
    assert get_element_value(dash_duo, "#shielding_symmetric-zeta") == "12"
    assert get_element_value(dash_duo, "#shielding_symmetric-eta") == "0.3"
    assert get_element_value(dash_duo, "#quadrupolar-Cq") == "2"
    assert get_element_value(dash_duo, "#quadrupolar-eta") == "0.1"

    # Spin system 1
    dash_duo.multiple_click("#spin-system-read-only > div > ul > li:nth-child(2)", 1)
    assert dash_duo.find_element("#spin-system-title").text == "7Li test 1"
    assert get_element_value(dash_duo, "#spin-system-abundance") == "35"
    assert get_element_value(dash_duo, "#isotope") == "7Li"
    assert get_element_value(dash_duo, "#isotropic_chemical_shift") == "-10"
    assert get_element_value(dash_duo, "#shielding_symmetric-zeta") == "15"
    assert get_element_value(dash_duo, "#shielding_symmetric-eta") == "0.1"
    assert get_element_value(dash_duo, "#quadrupolar-Cq") == "3"
    assert get_element_value(dash_duo, "#quadrupolar-eta") == "0.5"
