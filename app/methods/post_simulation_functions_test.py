# -*- coding: utf-8 -*-
import csdmpy as cp
import numpy as np
from numpy.fft import fft
from numpy.fft import fftshift
from numpy.fft import ifft
from numpy.fft import ifftshift

from app.methods.post_simulation_functions import line_broadening
from app.methods.post_simulation_functions import post_simulation


def test_1():
    data = cp.new(description="A new test dataset")

    amplitude = np.zeros(4096)

    amplitude[2048] = 10

    d0 = {
        "type": "linear",
        "description": "This is a linear dimension",
        "count": 4096,
        "increment": "0.1 Hz",
        "origin_offset": "0 Hz",
        "quantity_name": "frequency",
        "complex_fft": True,
        "reciprocal": {"quantity_name": "time"},
    }

    d1 = {
        "type": "internal",
        "numeric_type": "float64",
        "quantity_type": "scalar",
        "description": "This is an internal scalar dependent variable",
        "components": [amplitude],
    }

    data.add_dimension(d0)
    data.add_dependent_variable(d1)

    x = data.dimensions[0]
    y = data.dependent_variables[0].components[0]

    sigma = 2
    Lorentz = (sigma / 2) / (np.pi * (x.coordinates.value ** 2 + (sigma / 2) ** 2))
    Lorentz_apodization = line_broadening(x, y, sigma, 0)
    assert np.allclose(
        Lorentz_apodization[2048].real, Lorentz[2048], atol=1e-04
    ), "Lorentzian appodization amplitude failed"


def test_2():
    data = cp.new(description="A new test dataset")

    amplitude = np.zeros(4096)

    amplitude[2048] = 10

    d0 = {
        "type": "linear",
        "description": "This is a linear dimension",
        "count": 4096,
        "increment": "0.1 Hz",
        "origin_offset": "0 Hz",
        "quantity_name": "frequency",
        "complex_fft": True,
        "reciprocal": {"quantity_name": "time"},
    }

    d1 = {
        "type": "internal",
        "numeric_type": "float64",
        "quantity_type": "scalar",
        "description": "This is an internal scalar dependent variable",
        "components": [amplitude],
    }

    data.add_dimension(d0)
    data.add_dependent_variable(d1)

    x = data.dimensions[0]
    y = data.dependent_variables[0].components[0]
    sigma = 2
    Gauss = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
        -((x.coordinates.value / sigma) ** 2) / 2
    )
    Gauss_apodization = line_broadening(x, y, sigma, 1)
    assert np.allclose(
        Gauss_apodization[2048].real, Gauss[2048], atol=1e-04
    ), "Gaussian appodization amplitude failed"
