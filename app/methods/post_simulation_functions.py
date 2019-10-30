# -*- coding: utf-8 -*-
import numpy as np
from numpy.fft import fft
from numpy.fft import fftshift
from numpy.fft import ifft
from numpy.fft import ifftshift

# import csdmpy as


def line_broadening(x, amp, sigma, broadType):
    """
    This function evaluates
    ..math::

    """

    freq = x.coordinates.to("Hz")

    TimeDomain = ifft(ifftshift(amp))
    TimeDomain = np.roll(TimeDomain, int(x.count / 2))
    t = np.arange(x.count) - int(x.count / 2)

    time = t * 1 / (len(freq) * x.increment.to("Hz").value)

    if broadType == "Lorentz" and sigma != 0:
        broadSignal = np.exp(-sigma * np.abs(time))
    elif broadType == "Gaussian" and sigma != 0:
        broadSignal = np.exp(-(time / sigma) ** 2 / 2) / (np.sqrt(2 * np.pi) * sigma)
    else:
        broadSignal = 1

    appodized = np.roll(TimeDomain * broadSignal, -int(x.count / 2))

    return fftshift(fft(appodized))


def post_simulation(function, csdm_object, **kwargs):
    csdm_local = csdm_object.copy()

    x = csdm_local.dimensions[0]
    for datum in csdm_local.dependent_variables:
        y = datum.components[0]
        datum.components[0] = function(x, y, **kwargs)

    return csdm_local
    # return [

    #         function(datum, **kwargs) for datum in local_data if not isinstance(datum, list)
    # ]


if __name__ == "__main__":
    import numpy

    line_broadening(numpy.asarray([1, 2]), 2)
